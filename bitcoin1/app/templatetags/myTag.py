from django import template

#注册我们自定义的标签，只有注册过的标签，系统才能认识你，这是固定写法

from app.models import Post

register = template.Library()



@register.simple_tag
def get_num(ssid):
    postall = Post.objects.filter(stitle_id=ssid).count()
    print(111111111111111111)
    return postall


