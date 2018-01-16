from django.conf.urls import url 

app_name = 'django_pipes_blog'

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
]
