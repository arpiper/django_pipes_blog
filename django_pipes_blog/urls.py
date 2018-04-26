from django.urls import path, re_path, include
from rest_framework import routers
from . import views
from .viewsets import PostViewSet, PostImageViewSet, UserViewSet

app_name = 'django_pipes_blog'

# django rest framework url router registration
router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'postimages', PostImageViewSet)
router.register(r'posts', PostViewSet)

urlpatterns = [
    # django rest framework urls
    re_path(r'^api/', include(router.urls)),
    re_path(r'^api-auth/', include('rest_framework.urls')),

    re_path(r'^$', views.IndexView.as_view(), name='index'),
    re_path(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/(?P<slug>[\w\-\%]+)/$',
        views.SinglePostView.as_view(),
        name='post'
    ),
    re_path(r'(?P<year>\d{4})/(?P<month>\d{2})/$', 
        views.MultiPostView.as_view(), 
        name='multi_post'
    ),
    path('post/new/', views.NewPostView.as_view(), name='new_post'),
    path('post/<slug:slug>/', views.SinglePostView.as_view(), name='post_slug'),
    path('post/<int:pk>/preview/', views.SinglePostView.as_view(), name='preview_post'),
    path('post/<int:pk>/edit/', views.EditPostView.as_view(), name='edit_post'),
    path('tags/<str:tags>/', views.SearchTagsView.as_view(), name='tags'),
    path('post/<int:pk>/unpublished/', views.AllPosts.as_view(), name='unpublished'),
    path('post/<int:pk>/<str:all="all">/', views.AllPosts.as_view(), name='all_posts'),
]
