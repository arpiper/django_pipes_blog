from django.shortcuts import render
from django.views.generic import ListView, DetailView
from apps.django_pipes_blog import Post, PostImage, TextBlock


class IndexView(ListView):
    model = Post

