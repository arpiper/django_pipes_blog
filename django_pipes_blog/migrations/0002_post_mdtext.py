# Generated by Django 2.0.4 on 2018-04-19 23:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('django_pipes_blog', '0001_squashed_0005_auto_20180207_1714'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='mdtext',
            field=models.TextField(blank=True, null=True),
        ),
    ]
