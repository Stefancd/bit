from django.db import models

# Create your models here.
from tinymce.models import HTMLField


class User(models.Model):
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=20)
    email = models.CharField(max_length=30)

    class Meta:
        db_table = 'users'



class BsTitle(models.Model):
    bid = models.IntegerField(null=False,default=0)
    sid = models.IntegerField(unique=True,null=False,auto_created=True)
    btitle = models.CharField(max_length=20)
    stitle = models.CharField(max_length=20)
    class Meta:
        db_table = 'bstitles'


class Post(models.Model):
    article = models.CharField(max_length=20)
    content = models.TextField()
    author = models.ForeignKey('User')
    time1 = models.DateTimeField(auto_now_add=True)
    stitle = models.ForeignKey('BsTitle',to_field='sid')
    class Meta:
        db_table = 'posts'




