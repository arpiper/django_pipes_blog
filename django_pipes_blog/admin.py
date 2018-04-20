from django.contrib import admin
from django.db import models
from django.forms import Textarea, ModelForm
from django.utils.safestring import mark_safe
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
            'mdtext': Textarea(attrs={'cols': 80, 'rows': 20}),
        }
        fields = '__all__'


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'user', 'published', 'date_published', 'date_created')
    list_display_links = ('pk', 'title')
    list_filter = ['date_published', 'date_created']
    search_fields = ['title', 'date_published', 'date_created']
    ordering = ('-date_created',)
    readonly_fields = ('slug', 'date_published', 'mdtext')
    inlines = [TextBlockInline, PostImageInline,]
    fieldsets = [
        ("Blog Post", {'fields': ['title', 'slug', 'user', 'tags', 'published', 'text', 'mdtext']}),
    ]
    form = PostAdminForm


@admin.register(PostImage)
class PostImageAdmin(admin.ModelAdmin):
    list_display = ('pk', 'thumb', 'post')
    list_display_links = ('pk', 'thumb',)
    readonly_fields = ('small', 'medium', 'large', 'name', 'post', 'med')

    def thumb(self, obj):
        if obj.image:
            return mark_safe('<img src="%s" style="height:50px;width:auto;">' % obj.small.url)
        else:
            "no image"
    thumb.allow_tags = True
    def med(self, obj):
        return mark_safe('<img src="%s" style="max-width:100%s;">' %(obj.medium.url, '%'))
    med.allow_tags = True
    med.short_description = 'Current Image'
    fieldsets = [
        ('Upload Image', {'fields': ['med', 'image']}),
        ('Resizing Dimensions', {'fields': ['small_dims', 'medium_dims', 'large_dims']}),
        ('Image Information', {'fields': ['post', 'name', 'small', 'medium', 'large']}),
    ]

@admin.register(TextBlock)
class TextBlockAdmin(admin.ModelAdmin):
    list_display = ('pk', 'post')



