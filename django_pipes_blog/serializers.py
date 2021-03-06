from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Post, PostImage

class PostSerializer(serializers.HyperlinkedModelSerializer):
    #images = serializers.HyperlinkedRelatedField(view_name='postimage-detail', read_only=True)
    user = serializers.ReadOnlyField(source='user.username')
    url = serializers.HyperlinkedIdentityField(view_name='django_pipes_blog:post-detail', lookup_field='pk')
    class Meta:
        model = Post
        fields = ('url', 'user', 'tags', 'title', 'text', 'published', 
            'date_published', 'date_created', 'postimage_set' 
        )


class PostImageSerializer(serializers.HyperlinkedModelSerializer):
    post = serializers.ReadOnlyField(source='post.id')
    class Meta:
        model = PostImage
        fields = ('url', 'name', 'image', 'post')


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', )
    
