from django.contrib import admin
from apps.django_pipes_blog.models import Post, PostImage, TextBlock


class PostImageInline(admin.StackedInline):
    model = PostImage
    fieldsets = (
        (None, {
            'fields': ('image', 'small_dims', 'medium_dims', 'large_dims')
        }),
    )


class TextBlockInline(admin.StackedInline):
    model = TextBlock


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'tags', 'published', 'date_published', 'date_created')
    list_display_links = ('pk', 'title', 'date_created')
    fieldsets = [
        ("Blog Post", {'fields': ['title','tags']}),
    ]
    list_filter = ['date_published', 'date_created']
    search_fields = ['title', 'date_published', 'date_created']
    ordering = ('-date_created',)
    inlines = [TextBlockInline, PostImageInline,]


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



