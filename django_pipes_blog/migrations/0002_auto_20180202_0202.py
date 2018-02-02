# Generated by Django 2.0.1 on 2018-02-02 02:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('django_pipes_blog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='slug',
            field=models.SlugField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='textblock',
            name='block_title',
            field=models.CharField(blank=True, max_length=512, null=True),
        ),
    ]
