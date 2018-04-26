from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import Http404
from django.db.models import Q
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User

import calendar

from .models import Post, PostImage, TextBlock
from .forms import PostForm, TextBlockFormSet, ImageFormSet
from .utils import getPostDates, preparePostList, parseText


class IndexView(ListView):
    model = Post
    template_name = 'django_pipes_blog/multipost.html'
    context_object_name = 'posts'

    def get_queryset(self, *args, **kwargs):
        post_list = Post.objects.filter(
            published=True
        ).order_by(
            '-date_published'
        )
        return preparePostList(post_list)

    def get_context_data(self, *args, **kwargs):
        context = super(IndexView, self).get_context_data(*args, **kwargs)
        context['user'] = self.request.user
        context['sidebar_recent'], context['sidebar_month_list'] = getSidebarPostLinks()
        return context 
   

class SinglePostView(DetailView):
    model = Post
    template_name = 'django_pipes_blog/post.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = None
        if 'year' in self.kwargs.keys():
            year = self.kwargs['year'] 
            month = self.kwargs['month']
            day = self.kwargs['day']
            slug = self.kwargs['slug']
            post = Post.objects.get(
                date_published__year=year,
                date_published__month=month,
                date_published__day=day,
                slug=slug,
                published=True,
            )
        elif 'slug' in self.kwargs.keys():
            post = Post.objects.get(slug=self.kwargs['slug'], published=True)
        elif 'pk' in self.kwargs:
            post = Post.objects.get(
                pk=self.kwargs['pk'],
                user=self.request.user
            )
        else:
            return Http404('This blog post hasn\'t been written yet')
        if post:
            context['post'] = post
            context['post_id'] = post.id
            context['post_tags_array'] = post.tags.split(' ')
        context['user'] = self.request.user
        context['sidebar_recent'], context['sidebar_month_list'] = getSidebarPostLinks()
        return context


class MultiPostView(ListView):
    model = Post
    template_name = 'django_pipes_blog/multipost.html'
    context_object_name = 'posts'

    def get_queryset(self, *args, **kwargs):
        posts = Post.objects.filter(
            date_published__year=self.kwargs['year'], 
            date_published__month=self.kwargs['month']
        ).order_by(
            '-date_published'
        )
        return preparePostList(posts)

    def get_context_data(self, *args, **kwargs):
        context = super(MultiPostView, self).get_context_data(*args, **kwargs)
        context['user'] = self.request.user
        context['sidebar_recent'], context['sidebar_month_list'] = getSidebarPostLinks()
        context['month'] = calendar.month_name[int(self.kwargs['month'])]
        context['year'] = self.kwargs['year']
        return context


class SearchTagsView(ListView):
    model = Post
    template_name = 'django_pipes_blog/multipost.html'
    context_object_name = 'posts'

    def get_queryset(self, *args, **kwargs):
        tags = self.kwargs['tags'].split('&')
        q = Q()
        for tag in tags:
            q |= Q(tags__icontains=tag)
        post_list = Post.objects.filter(q)
        posts = preparePostList(post_list)
        return posts

    def get_context_data(self, *args, **kwargs):
        context = super(SearchTagsView, self).get_context_data(*args, **kwargs)
        context['sidebar_recent'], context['sidebar_month_list'] = getSidebarPostLinks()
        context['tag'] = self.kwargs['tags'].split('&')
        return context


class AllPosts(LoginRequiredMixin, ListView):
    model = User
    template_name = 'django_pipes_blog/multipost.html'
    context_object_name = 'posts'

    def get_queryset(self):
        posts = Post.objects.filter(
            user=self.request.user,
            published=True
        ).order_by(
            '-date_created'
        )
        return preparePostList(posts)

    def get_context_data(self):
        context = super().get_context_data()
        context['user'] = self.request.user
        context['sidebar_recent'], context['sidebar_month_list'] = getSidebarPostLinks()
        return context


@method_decorator(csrf_protect, name='dispatch')
class NewPostView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'django_pipes_blog/create_post.html'
    form_class = PostForm
    context_object_name = 'post_form'
    
    #def get_object(self, **kwargs):
        #return Post.objects.get(pk=self.kwargs['pk'])

    def get_context_data(self):
        context = super(NewPostView, self).get_context_data()
        context['action'] = reverse('django_pipes_blog:new_post')
        context['username'] = self.request.user
        context['imageset'] = ImageFormSet()
        context['sidebar_recent'], context['sidebar_month_list'] = getSidebarPostLinks()
        return context

    def post(self, request, *args, **kwargs):
        context = {
            'username': self.request.user,
            'imageset': ImageFormSet(self.request.POST, self.request.FILES),
        }
        form = PostForm(self.request.POST)
        if form.is_valid():
            context['form'] = form
            post = form.save(commit=False)
            post.user = request.user
            post.save() # save the post first to create an id and db entry for the parse func.
            # parse the text for markdown style tags
            post.mdtext = parseText(post.text, p.id)
            post.save()
            if context['imageset'].is_valid():
                context['imageset'].save()
            if post.published:
                return redirect('django_pipes_blog:post_slug', slug=post.slug) 
            return redirect('django_pipes_blog:edit_post', pk=post.pk)
        return render(self.request, self.template_name, context=context)


@method_decorator(csrf_protect, name='dispatch')
class EditPostView(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'django_pipes_blog/create_post.html'
    context_object_name = 'post_form'

    def get_object(self, **kwargs):
        return Post.objects.get(pk=self.kwargs['pk'])

    def get_context_data(self, *args, **kwargs):
        context = super(EditPostView, self).get_context_data(*args, **kwargs)
        context['post_id'] = self.kwargs['pk']
        context['action'] = reverse('django_pipes_blog:edit_post', kwargs={'pk':self.kwargs['pk']}) 
        if self.request.POST:
            context['imageset'] = ImageFormSet(self.request.POST, self.request.FILES, instance=self.object)
        else:
            context['imageset'] = ImageFormSet(instance=self.object)
        context['sidebar_recent'], context['sidebar_month_list'] = getSidebarPostLinks()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object(**kwargs)
        context = self.get_context_data(*args, **kwargs)
        form = context['form']
        if form.is_valid():
            p = form.save(commit=False)
            if context['imageset'].is_valid():
                context['imageset'].save()
                p.save()
                # parse the text for markdown style tags
                p.mdtext = parseText(p.text, p.id)
                p.save()
                context['status'] = 'Post Successfully Updated'
                # return the single post view
            if p.published:
                return redirect('django_pipes_blog:post_slug', slug=p.slug)
        return render(self.request, self.template_name, context=context)


##
# Get list of most recent 5 posts and links for months containing posts for the sidebar.
## 
def getSidebarPostLinks():
    post_list = Post.objects.filter(published=True).order_by('-date_published')
    posts = []
    for post in post_list[:5]:
        p = {
            'slug': post.slug,
            'title': post.title,
        }
        p.update(getPostDates(post))
        posts.append(p)
    month_list = {}
    for post in post_list:
        y = post.date_published.year
        m = calendar.month_name[post.date_published.month]
        if ('%s %s' %(m,y)) not in month_list.keys():
            month_list[('%s %s' %(m, y))] = {
                'year': y,
                'month': post.date_published.strftime('%m')
            }
    return posts, month_list


