import hashlib
import uuid
from datetime import datetime

from django.conf import settings
from django.core.mail import send_mail
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect
from app.models import User

# Create your views here.
from app.models import BsTitle

from app.models import Post

from app.models import Reply

from app.models import Good


def index(request):
    btitles = BsTitle.objects.all().values('bid', 'btitle').distinct()
    stitles = BsTitle.objects.all()
    # btitles = BsTitle.objects.filter()
    # stitles = BsTitle.objects.filter()
    # list1 = []
    # print('--------------',btitles)
    # for bt in btitles:
    #     if bt.bid not in list1:
    #         list1.append(bt)
    # for i in list1:
    #     print(i.id,'-----------',i.bid)
    data = {
        # 'btitles':list1,
        'btitles': btitles,
        'stitles': stitles,

    }
    return render(request, 'app/index.html', data)


# def baseposts(request,bid,sid):
# def baseposts(request,bid):
#     btitles = BsTitle.objects.filter(bid=bid).values('bid','btitle').distinct()
#     stitles = BsTitle.objects.filter(bid=bid)
#     data = {
#         'bstitles':btitles,
#         'stitles':stitles,
#         'bid':bid,
#     }
#     return render(request,'app/baseposts.html',data)

def baseposts(request, bid):
    btitles = BsTitle.objects.filter(bid=bid).values('bid', 'btitle').distinct()
    stitles = BsTitle.objects.filter(bid=bid)
    data = {
        'btitles': btitles,
        'stitles': stitles,
        'bid': bid,
        # 'sid':sid,
    }

    return render(request, 'app/baseposts.html', data)


def postslist(request, sid):
    plist = Post.objects.filter(stitle_id=sid)
    data = {
        'plist': plist,
        'sid': sid,
    }

    return render(request, 'app/postslist.html', data)


def postdetail(request, pid):
    try:
        pone = Post.objects.filter(id=pid)[0]
        # 下面整理出该用户的状态（是否激活）作用在于允不允许评论

        username = request.session.get('username')
        status = False
        if username:
            user = User.objects.filter(username=username)[0]
            # status = pone.author.isActive
            status = user.isActive

        # 或者pone = Post.objects.get(id=pid)
        article = pone.article
        content = pone.content
        # 回复需要的参数
        pid = pid
        # pid = id
        replies = Reply.objects.filter(post=pone)
        #
        # replies = Reply.objects.filter(post__id=pid)
        goods = Good.objects.filter(post=pone).count()

        data = {
            'article': article,
            'content': content,
            'pid': pid,
            # 'pid':pid,
            'replies': replies,
            'goods': goods,
            'status':status,
            # 此处作为判断用户是否登陆下展示“本帖子中包含更多资源”
            'username':username,
        }
        return render(request, 'app/postdetail.html', data)
    except Exception as e:
        # return render(request,'404.html',locals())
        return render(request,'404.html',locals())


def posting(request):
    return render(request, 'app/posting.html')


def writing(request, sid):
    try:
        username = request.session.get('username')
        user = User.objects.filter(username=username)[0]
        stitle = BsTitle.objects.filter(sid=sid)[0]
        sid = sid
        if request.method == 'GET':
            data = {
                'username': username,
                'sid': sid,
            }
            return render(request, 'app/writing.html', data)
        else:
            article = request.POST.get('article')
            content = request.POST.get('content')

            post = Post.create(article=article, content=content, author=user, stitle=stitle)
            post.save()
            print('888888888888888')
            return redirect('/index/')
    except Exception as e:
        return render(request, '404.html', locals())


def reply(request, pid):
    if request.method == 'POST':
        content = request.POST.get('content')
        username = request.session.get('username')
        user = User.objects.filter(username=username)[0]
        pone = Post.objects.filter(id=pid)[0]
        # pid = pid
        # data = {
        #     'content':content,
        #     'user':user,
        #     'pone':pone,
        #     'pid':pid,
        # }
        reply = Reply.create(content=content, post=pone, user=user)
        reply.save()

        return redirect('/postdetail/{}/'.format(pid))
        # return render(request,'app/postdetail.html',data)
        # referer = request.META.get('HTTP_REFERER')
        # return redirect(referer)
        # return redirect('/postdetail/?pid=' + pid +  '/')
        # return redirect('/postdetail/?pid=pid')


def goods(request, pid):
    username = request.session.get('username')
    # pone = Post.objects.filter(id=pid)[0]
    # 方法2主键用get可以直接获取单个对象
    pone = Post.objects.get(id=pid)
    user = User.objects.filter(username=username)[0]
    if Good.objects.filter(post=pone, user=user).count() < 1:
        goods = Good.create(post=pone, user=user)
        goods.save()

    return redirect('/postdetail/{}/'.format(pid))


def register(request):
    if request.method == 'GET':
        return render(request, 'app/register.html')
    else:

        params = request.POST
        name = params.get('username')
        username1 = User.objects.filter(username=name)
        if username1.count() >= 1:
            return redirect('/register/')
        passwd1 = params.get('password')
        passwd2 = params.get('repassword')
        code = params.get('code')
        email = params.get('email')
        if passwd1 != passwd2:
            return redirect('/register/')
        code1 = request.session["code"]
        if code.upper() != code1.upper():
            return redirect('/register/')
        m = hashlib.md5()
        b = passwd1.encode(encoding='utf-8')
        m.update(b)
        password_md5 = m.hexdigest()
        user = User()
        user.username = name
        user.password = password_md5
        user.email = email
        user.save()
        request.session['username']=name
        return redirect('/index/')
        # #发邮件
        # #验证码
        # activeValue = str(uuid.uuid4())
        # #存储到session
        # request.session["activeKey"] = activeValue
        # html_message = "<a href='http://127.0.0.1:8000/active/?name=%s&activeKey=%s'>点击激活</a>"%(name, activeValue)
        # mailStr = request.POST.get("email")
        # send_mail("注册激活", "", settings.EMAIL_FROM,
        #           [mailStr], html_message=html_message)
        # return HttpResponse("用户注册成功，请进入邮件激活后使用")


# def active(request):
#     # user = User.objects.filter()
#     activeValue1 = request.GET.get("activeKey")
#     activeValue2 = request.session.get("activeKey")
#     if activeValue1 != activeValue2:
#         return HttpResponse("激活失败")
#
#     user = User.objects.get(username=request.GET.get("name"))
#     user.isActive = True
#     user.save()
#     del request.session["activeKey"]
#     return HttpResponse("激活成功")


# 激活位置选择2
def active(request):
    name = request.session.get('username')
    user = User.objects.filter(username=name)[0]
    # 发邮件
    # 验证码
    activeValue = str(uuid.uuid4())
    # 存储到session
    request.session["activeKey"] = activeValue
    html_message = "<a href='http://127.0.0.1:8000/reactive/?name=%s&activeKey=%s'>点击激活</a>" % (name, activeValue)
    mailStr = user.email
    # mailStr = request.POST.get("email")
    send_mail("注册激活", "", settings.EMAIL_FROM,
              [mailStr], html_message=html_message)
    return HttpResponse("用户注册成功，请进入邮件激活后使用")


def reactive(request):
    # user = User.objects.filter()
    activeValue1 = request.GET.get("activeKey")
    activeValue2 = request.session.get("activeKey")
    if activeValue1 != activeValue2:
        return HttpResponse("激活失败")
    user = User.objects.get(username=request.GET.get("name"))
    user.isActive = True
    user.save()
    del request.session["activeKey"]
    return HttpResponse("激活成功")


def login(request):
    if request.method == 'GET':
        return render(request, 'app/login.html')
    else:
        username1 = request.POST.get('username')
        password1 = request.POST.get('password')
        m = hashlib.md5()
        b = password1.encode(encoding='utf-8')
        m.update(b)
        password1_md5 = m.hexdigest()
        code1 = request.POST.get('code')
        code2 = request.session['code']
        uname = User.objects.filter(username=username1)
        if uname:
            if password1_md5 != uname[0].password:
                return redirect('/login/')
            if code1.upper() != code2.upper():
                return redirect('/login/')
            request.session['username'] = username1
            return redirect('/index/')

        return redirect('/register/')


def logout(request):
    request.session.flush()
    return redirect('/index/')


def details(request):
    return render(request, 'app/basedetails.html')


def base(request):
    return render(request, 'app/base.html')


def basepersonal(request):
    return render(request, 'app/basepersonal.html')


def bsavatar(request):
    return render(request, 'app/bsavatar.html')


def bsprofile(request):
    return render(request, 'app/bsprofile.html')


def bspfcontact(request):
    return render(request, 'app/bspfcontact.html')


def bspfedu(request):
    return render(request, 'app/bspfedu.html')


def bspfwork(request):
    return render(request, 'app/bspfwork.html')


def bspfinformation(request):
    return render(request, 'app/bspfinformation.html')


def bscredit(request):
    return render(request, 'app/bscredit.html')


def bscdrecord(request):
    return render(request, 'app/bscdrecord.html')


def bscdrule(request):
    return render(request, 'app/bscdrule.html')


def bsusergroup(request):
    return render(request, 'app/bsusergroup.html')


def bsugbuy(request):
    return render(request, 'app/bsugbuy.html')


def bsugmine(request):
    return render(request, 'app/ugmine.html')


def bsprivacy(request):
    return render(request, 'app/bsprivacy.html')


def bspwsafe(request):
    return render(request, 'app/bspwsafe.html')


def bspromotion(request):
    return render(request, 'app/bspromotion.html')


def verifycode(request):
    # 引入绘图模块
    from PIL import Image, ImageDraw, ImageFont
    # 引入随机函数模块
    import random
    # 定义变量，用于画面的背景色、宽、高
    bgcolor = (random.randrange(20, 100), random.randrange(
        20, 100), random.randrange(20, 100))
    width = 100
    height = 50
    # 创建画面对象
    im = Image.new('RGB', (width, height), bgcolor)
    # 创建画笔对象
    draw = ImageDraw.Draw(im)
    # 调用画笔的point()函数绘制噪点
    for i in range(0, 100):
        xy = (random.randrange(0, width), random.randrange(0, height))
        fill = (random.randrange(0, 255), 255, random.randrange(0, 255))
        draw.point(xy, fill=fill)
    # 定义验证码的备选值
    str = '1234567890QWERTYUIOPASDFGHJKLZXCVBNMqwertyuiopasdfghjklzxcvbnm'
    # 随机选取4个值作为验证码
    rand_str = ''
    for i in range(0, 4):
        rand_str += str[random.randrange(0, len(str))]
    # 构造字体对象
    # font = ImageFont.truetype(r'common/fonts/code.ttf', 40)
    font = ImageFont.truetype(r'C:/Windows/Fonts/Arial/ariblk.ttf', 40)
    # 构造字体颜色
    fontcolor1 = (255, random.randrange(0, 255), random.randrange(0, 255))
    fontcolor2 = (255, random.randrange(0, 255), random.randrange(0, 255))
    fontcolor3 = (255, random.randrange(0, 255), random.randrange(0, 255))
    fontcolor4 = (255, random.randrange(0, 255), random.randrange(0, 255))
    # 绘制4个字
    draw.text((5, 2), rand_str[0], font=font, fill=fontcolor1)
    draw.text((25, 2), rand_str[1], font=font, fill=fontcolor2)
    draw.text((50, 2), rand_str[2], font=font, fill=fontcolor3)
    draw.text((75, 2), rand_str[3], font=font, fill=fontcolor4)
    # 释放画笔
    del draw
    # 内存文件操作
    import io
    buf = io.BytesIO()
    # 将图片保存在内存中，文件类型为png
    im.save(buf, 'png')

    # 将验证码保存到session，以便后续验证
    request.session["code"] = rand_str
    print(rand_str)

    # 将内存中的图片数据返回给客户端，MIME类型为图片png
    return HttpResponse(buf.getvalue(), 'image/png')



def search(request):
    keyword = request.POST.get('keyword')
    results = Post.objects.filter(Q(content__contains=keyword) | Q(article__contains=keyword) )

    data = {
        'keyword':keyword,
        'results':results,
        'keyword':keyword,
    }
    return render(request,'app/search.html',data)

