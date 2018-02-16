from rest_framework import viewsets

from .serializers import PostSerializer, PostImageSerializer
from .models import Post, PostImage

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class PostImageViewSet(viewsets.ModelViewSet):
    queryset = PostImage.objects.all()
    serializer_class = PostImageSerializer
