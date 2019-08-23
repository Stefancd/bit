from django.db import models

# Create your models here.
from tinymce.models import HTMLField


class User(models.Model):
    username = models.CharField(max_length=20, verbose_name='用户名')
    password = models.CharField(max_length=256)
    email = models.CharField(max_length=30)
    isActive = models.BooleanField(default=False)

    class Meta:
        db_table = 'users'
        verbose_name_plural='用户列表'



class BsTitle(models.Model):
    bid = models.IntegerField(null=False,default=0)
    sid = models.IntegerField(unique=True,null=False,auto_created=True)
    btitle = models.CharField(max_length=20)
    stitle = models.CharField(max_length=20)
    class Meta:
        db_table = 'bstitles'
        verbose_name_plural='板块分级'

class Post(models.Model):
    article = models.CharField(max_length=20)
    content = models.TextField()
    author = models.ForeignKey('User')
    time1 = models.DateTimeField(auto_now_add=True)
    stitle = models.ForeignKey('BsTitle',to_field='sid')

    class Meta:
        db_table = 'posts'
        verbose_name_plural='帖子列表'

    @classmethod
    def create(cls, article,content,author,stitle):
        return cls(article=article,content=content,author=author,stitle=stitle)


class Reply(models.Model):
    post = models.ForeignKey('Post')
    user = models.ForeignKey('User')
    content = models.CharField(max_length=200)
    create_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'replies'

    @classmethod
    def create(cls, content,post,user):
        return cls(content=content,post=post,user=user)

class Good(models.Model):
    post = models.ForeignKey('Post')
    user = models.ForeignKey('User')

    class Meta:
        db_table = 'goods'

    @classmethod
    def create(cls,post,user):
        return cls(post=post,user=user)


