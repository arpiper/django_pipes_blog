from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator

from .models import Post, PostImage, TextBlock
from .forms import PostForm, TextBlockFormSet


class IndexView(ListView):
    model = Post
    template_name = 'django_pipes_blog/index.html'
    context_object_name = 'posts'

    def get_queryset(self, *args, **kwargs):
        post_list = Post.objects.filter(
            published=True
        ).order_by(
            '-date_published'
        )
        posts = []
        for p in post_list:
            posts.append({
                'title': p.title,
                'date_published': p.date_published,
                'textblock_set': p.textblock_set.all(),
                'year': p.date_published.year,
                'month': p.date_published.strftime('%m'),
                'day': p.date_published.day,
                'slug': p.slug
            })
        return posts
        

class SinglePostView(DetailView):
    model = Post
    template_name = 'django_pipes_blog/post.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'year' in self.kwargs.keys():
            year = self.kwargs['year'] 
            month = self.kwargs['month']
            day = self.kwargs['day']
            slug = self.kwargs['slug']
            post = Post.objects.get(
                date_published__year=year,
                date_published__month=month,
                date_published__day=day,
                slug=slug
            )
            context['post'] = post
            context['post_id'] = post.id
        elif 'slug' in self.kwargs.keys():
            post = Post.objects.get(slug=self.kwargs['slug'])
            context['post'] = post
            context['post_id'] = post.id
        return context


@method_decorator(csrf_protect, name='dispatch')
class NewPostView(CreateView):
    model = Post
    template_name = 'django_pipes_blog/create_post.html'
    fields = ['title', 'published', 'tags']
    context_object_name = 'post_form'

    def get_context_data(self):
        context = super(NewPostView, self).get_context_data()
        context['formset'] = TextBlockFormSet(instance=self.object)
        context['username'] = self.request.user
        context['action'] = reverse('django_pipes_blog:new_post')
        return context

    def post(self, request):
        context = {}
        form = PostForm(self.request.POST)
        if form.is_valid():
            context['form'] = form
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            formset = TextBlockFormSet(self.request.POST, instance=post)
            if formset.is_valid():
                formset.save()
            context['formset'] = formset
            return redirect('django_pipes_blog:post_slug', slug=post.slug) 
        context['formset'] = TextBlockFormSet(self.request.POST, errors='oops')
        return render(self.request, self.template_name, context=context)


class EditPostView(UpdateView):
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
            context['formset'] = TextBlockFormSet(self.request.POST, instance=self.get_object())
        else:
            context['formset'] = TextBlockFormSet(instance=self.get_object())
        print(context)
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object(**kwargs)
        context = self.get_context_data(*args, **kwargs)
        form = PostForm(self.request.POST)
        print('post', context)
        if form.is_valid():
            p = form.save(commit=False)
            if context['formset'].is_valid():
                context['formset'].save()
                p.save()
                context['status'] = 'success'
                #return render(self.request, self.template_name, context=context)
        return render(self.request, self.template_name, context=context)
