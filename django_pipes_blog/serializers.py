from rest_framework import serializers

from .models import Post, PostImage

class PostSerializer(serializers.HyperlinkedModelSerializer):
    images = serializers.HyperlinkedRelatedField(view_name='postimage-detail', read_only=True)
    #url = serializers.HyperlinkedIdentityField(view_name='post'
    class Meta:
        model = Post
        fields = ('url', 'tags', 'title', 'text', 'published', 'date_published', 'date_created', 'images')
        extra_kwargs = {
            'post': {'lookup_field': 'slug'}
        }


class PostImageSerializer():
    post = serializers.ReadOnlyField(source='post.id')
    class Meta:
        model = PostImage
        fields = ('url', 'name', 'image', 'post')

