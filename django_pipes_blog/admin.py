from django.contrib import admin
from django.db import models
from django.forms import Textarea, ModelForm
from apps.django_pipes_blog.models import Post, PostImage, TextBlock


class PostImageInline(admin.StackedInline):
    model = PostImage
    fieldsets = (
        (None, {
            'fields': ('image', 'small_dims', 'medium_dims', 'large_dims')
        }),
    )
    extra = 1


class TextBlockInline(admin.StackedInline):
    model = TextBlock
    extra = 1
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'cols': 80, 'rows': 3})},
    }


class PostAdminForm(ModelForm):
    class Meta:
        model = Post
        widgets = {
            'tags': Textarea(attrs={'cols': 80, 'rows': 2}),
            'text': Textarea(attrs={'cols': 80, 'rows': 20}),
        }
        fields = '__all__'


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'user', 'published', 'date_published', 'date_created')
    list_display_links = ('pk', 'title')
    list_filter = ['date_published', 'date_created']
    search_fields = ['title', 'date_published', 'date_created']
    ordering = ('-date_created',)
    readonly_fields = ('slug', 'date_published')
    inlines = [TextBlockInline, PostImageInline,]
    fieldsets = [
        ("Blog Post", {'fields': ['title', 'slug', 'user', 'tags', 'published', 'text']}),
    ]
    form = PostAdminForm


@admin.register(PostImage)
class PostImageAdmin(admin.ModelAdmin):
    list_display = ('pk', 'thumbnail', 'post')
    list_display_links = ('pk', 'thumbnail',)
    readonly_fields = ('small', 'medium', 'large')

    def thumbnail(self, obj):
        if obj.image:
            return '<img src="%s" style="height:50px;width:auto;">' % (obj.img.url)
        else:
            "no image"


@admin.register(TextBlock)
class TextBlockAdmin(admin.ModelAdmin):
    list_display = ('pk', 'post')



