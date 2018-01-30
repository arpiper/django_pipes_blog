from django.urls import path, re_path
from . import views

app_name = 'django_pipes_blog'

urlpatterns = [
    re_path(r'^$', views.IndexView.as_view(), name='index'),
    re_path('(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/(?P<day>[0-9]{2})/<str:title>/', views.SinglePostView),
    re_path('<slug:slug>', views.SinglePostView)
]
