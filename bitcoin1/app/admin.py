from django.contrib import admin
from app.models import *


# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'password', 'email')


class BsTitleAdmin(admin.ModelAdmin):
    list_display = ('btitle', 'stitle')


class PostAdmin(admin.ModelAdmin):
    list_display = ('article', 'author', 'time1', 'stitle')


admin.site.register(User, UserAdmin)
admin.site.register(BsTitle, BsTitleAdmin)
admin.site.register(Post, PostAdmin)
