from django.shortcuts import render
from django.views.generic import ListView, DetailView
from apps.django_pipes_blog.models import Post, PostImage, TextBlock


class IndexView(ListView):
    model = Post
    template_name = 'django_pipes_blog/index.html'
    context_object_name = 'posts'

    def get_queryset(self, *args, **kwargs):
        posts = Post.objects.filter(
            published=True
        ).order_by(
            '-date_published'
        )
        return posts
        

class SinglePostView(DetailView):
    model = Post
    template = 'django_pipes_blog/post.html'
    context_object_name = 'post'

    def get_context_data(self, *args, **kwargs):
        if 'year' in kwargs.keys():
            year = kwargs['year'] 
            month = kwargs['month']
            day = kwargs['day']
            title = kwargs['title']
            post = Post.objects.filter(
                date_published__year=year,
                date_published__month=month,
                date_published__day=day,
                title=title
            )
            if len(post) === 1:
                return post
