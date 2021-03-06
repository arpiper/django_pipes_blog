from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
from django.core.files.base import ContentFile

from PIL import Image as PIL_Image
from io import BytesIO
from urllib.parse import quote


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=255)
    slug = models.SlugField(blank=True, null=True)
    tags = models.TextField(blank=True, null=True)
    published = models.BooleanField(default=False)
    date_published = models.DateTimeField(blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    text = models.TextField(blank=True, null=True)
    mdtext = models.TextField(blank=True, null=True)

    def __str__(self):
        if self.user:
            return '%s - %s' %(self.user.username, self.title)
        return self.title

    def save(self, *args, **kwargs):
        super(Post, self).save(*args, **kwargs)
        if self.published and not self.date_published:
            self.date_published = now()
        self.slug = quote('%s-%d' %('_'.join(self.title.split(' ')), self.pk))      
        super(Post, self).save(*args, **kwargs)


class TextBlock(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    block_title = models.CharField(max_length=512, blank=True, null=True)
    text = models.TextField()
    
    def __str__(self):
        return '%d_%d' %(self.pk, self.post.pk)


class PostImage(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    name = models.CharField(max_length=255, null=True, blank=True)
    image = models.ImageField(upload_to='pipes_blog_images/')
    small = models.ImageField(upload_to='pipes_blog_images/small/', null=True, blank=True)
    small_dims = models.IntegerField(default=250)
    medium = models.ImageField(upload_to='pipes_blog_images/medium/', blank=True, null=True)
    medium_dims = models.IntegerField(default=600)
    large = models.ImageField(upload_to='pipes_blog_images/large/', blank=True, null=True)
    large_dims = models.IntegerField(default=900)

    def __str__(self):
        return self.image.name

    def resize(self, size, obj, *args, **kwargs):
        if not self.image:
            return self

        if self.image.width / self.image.height > 2:
            x = (self.image.width / self.image.height) * size
            SIZE = (x, size)
        else:
            SIZE = (size, size)

        TYPE = self.image.name.split('.')[-1].lower()

        if TYPE == 'jpg' or TYPE == 'jpeg':
            PIL_TYPE = 'jpeg'
            #FILE_EXT = 'jpg'
            #CONTENT_TYPE = 'image/jpg'
        elif TYPE == 'png':
            PIL_TYPE = 'png'
            #FILE_EXT = 'png'
            #CONTENT_TYPE = 'image/png'
        elif TYPE == 'gif':
            PIL_TYPE = 'gif'

        # open original image with PIL.Image
        self.image.open() # open the image first in order to read it.
        img = PIL_Image.open(BytesIO(self.image.read()))

        temp_handle = BytesIO() # issues here with bytes vs strings python3 uses BytesIO 

        # create thumbnail with PIL.Image convenience function
        img.thumbnail(SIZE, PIL_Image.ANTIALIAS)
        # save the thumbnail.
        img.save(temp_handle, PIL_TYPE)
        temp_handle.seek(0)

        # save the thumbnail to the thumbnail field.
        name = "%s" %(self.image.name.split('/')[-1])
        obj.save(name, ContentFile(temp_handle.read()), save=False)
        # delete the img. otherwise clutters the root folder.
        self.image.close()

    def save(self, *args, **kwargs):
        super(PostImage, self).save(*args, **kwargs)
        # check if objects exists and main image hasnt changed.
        if self.pk is not None:
            og = PostImage.objects.get(pk=self.pk)
            if not self.small or og.small != self.small:
                self.resize(self.small_dims, self.small)
            if not self.medium or og.medium != self.medium:
                self.resize(self.medium_dims, self.medium)
            if not self.large or og.large != og.large:
                self.resize(self.large_dims, self.large)
            if not self.name:
                self.name = self.image.name.split('/')[-1].split('.')[0]
        else:
            if not self.name:
                self.name = self.image.name.split('/')[-1].split('.')[0]
        super(PostImage, self).save(*args, **kwargs)
