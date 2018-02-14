====
blog
====

Basic blogging app for Django 2.0 built simply as an exercice in reinventing the wheel. 

Quick Start
-----------

1. Add "django_pipes_blog" to your INSTALLED_APPS setting like this::

  INSTALLED_APPS = [
    ...
    'django_pipes_blog',
  ]

2. Include the blog URLConf in your project urls.py like this::
  
  path('blog/', include(django_pipes_blog.urls)),

3. Run `python manage.py migrate` to create the blog models.

