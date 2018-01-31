from django.urls import path, re_path
from . import views

app_name = 'django_pipes_blog'

urlpatterns = [
    re_path(r'^$', views.IndexView.as_view(), name='index'),
    re_path(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/(?P<slug>[\w]+)/$', views.SinglePostView.as_view()),
    path('<slug:slug>/', views.SinglePostView.as_view()),
    path('post/new/', views.NewPostView.as_view(), name='new_post'),
]
