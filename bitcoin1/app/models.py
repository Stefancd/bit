from django.db import models

# Create your models here.
from tinymce.models import HTMLField


class User(models.Model):
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=20)
    email = models.CharField(max_length=30)

    class Meta:
        db_table = 'users'

class Post(models.Model):
    article = models.CharField(max_length=20)
    content = models.TextField()
    author = models.ForeignKey('User')
    time1 = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'posts'


class Bigtitle