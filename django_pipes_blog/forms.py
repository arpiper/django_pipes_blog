from django.forms import ModelForm, inlineformset_factory, Textarea
from django.utils.translation import gettext_lazy

from .models import Post, TextBlock, PostImage

class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'published', 'tags', 'text']
        widgets = {
            'tags': Textarea(attrs={'rows': 3, 'cols': 40}),
            'text': Textarea(attrs={'rows': 40, 'cols': 40}),
        }
        help_texts = {
            'tags': gettext_lazy('Space seperated list of tags relevant to the post.'),
        }


class TextBlockForm(ModelForm):
    class Meta:
        model = TextBlock
        fields = ['block_title', 'text']
        '''
        widgets = {
            'text': Textarea(attrs={'rows': 20}),
        }
        '''


class ImageForm(ModelForm):
    class Meta:
        model = PostImage
        fields = ['image', 'small_dims', 'medium_dims', 'large_dims']
        help_texts = {
            'image': gettext_lazy('Image will be saved with multiple sizes based on the following dimensions:'),
        }


TextBlockFormSet = inlineformset_factory(Post, TextBlock, form=TextBlockForm, extra=1)
ImageFormSet = inlineformset_factory(Post, PostImage, form=ImageForm, extra=1)
