from django.shortcuts import render
from django.views.generic import ListView, DetailView
from apps.django_pipes_blog.models import Post, PostImage, TextBlock


class IndexView(ListView):
    model = Post
    template_name = 'django_pipes_blog/index.html'
    context_object_name = 'posts'

    def get_queryset(self, *args, **kwargs):
        posts = Post.objects.filter(
            user=self.request.user, 
            published=True
        ).order_by(
            '-date_published'
        )
        return posts
        
