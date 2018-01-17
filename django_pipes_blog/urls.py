from django.conf.urls import url 
from apps.django_pipes_blog import views

app_name = 'django_pipes_blog'

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
]
