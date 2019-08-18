from django.http import HttpResponse
from django.shortcuts import render, redirect
from app.models import User



# Create your views here.
from app.models import BsTitle


def index(request):
    btitles = BsTitle.objects.all().values('bid','btitle').distinct()
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
        'btitles':btitles,
        'stitles':stitles,

    }
    return render(request,'app/index.html',data)



def register(request):
    if request.method == 'GET':
        return render(request, 'app/register.html')
    else:
        params = request.POST
        name = params.get('username')
        passwd1 = params.get('password')
        passwd2 = params.get('repassword')
        code = params.get('code')
        email = params.get('email')
        if passwd1 != passwd2:
            return redirect('/register/')
        code1 = request.session["code"]
        if code.upper() != code1.upper():
            return redirect('/register/')
        user = User()
        user.username = name
        user.password = passwd1
        user.email = email
        user.save()
        return redirect('/index/')

def login(request):
    if request.method == 'GET':
        return render(request,'app/login.html')
    else:
        username1 = request.POST.get('username')
        password1 = request.POST.get('password')
        code1 = request.POST.get('code')
        code2 = request.session['code']
        uname = User.objects.filter(username=username1)
        if uname:
            if password1 != uname[0].password:
                return redirect('/login/')
            if code1.upper() != code2.upper():
                return redirect('/login/')
            request.session['username']=username1
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
    return render(request,'app/bscdrecord.html')


def bscdrule(request):
    return render(request,'app/bscdrule.html')


def bsusergroup(request):
    return render(request, 'app/bsusergroup.html')

def bsugbuy(request):
    return render(request,'app/bsugbuy.html')


def bsugmine(request):
    return render(request,'app/ugmine.html')


def bsprivacy(request):
    return render(request, 'app/bsprivacy.html')


def bspwsafe(request):
    return render(request, 'app/bspwsafe.html')


def bspromotion(request):
    return render(request, 'app/bspromotion.html')





def verifycode(request):
    #引入绘图模块
    from PIL import Image, ImageDraw, ImageFont
    #引入随机函数模块
    import random
    #定义变量，用于画面的背景色、宽、高
    bgcolor = (random.randrange(20, 100), random.randrange(
        20, 100), random.randrange(20, 100))
    width = 100
    height = 50
    #创建画面对象
    im = Image.new('RGB', (width, height), bgcolor)
    #创建画笔对象
    draw = ImageDraw.Draw(im)
    #调用画笔的point()函数绘制噪点
    for i in range(0, 100):
        xy = (random.randrange(0, width), random.randrange(0, height))
        fill = (random.randrange(0, 255), 255, random.randrange(0, 255))
        draw.point(xy, fill=fill)
    #定义验证码的备选值
    str = '1234567890QWERTYUIOPASDFGHJKLZXCVBNMqwertyuiopasdfghjklzxcvbnm'
    #随机选取4个值作为验证码
    rand_str = ''
    for i in range(0, 4):
        rand_str += str[random.randrange(0, len(str))]
    #构造字体对象
    # font = ImageFont.truetype(r'common/fonts/code.ttf', 40)
    font = ImageFont.truetype(r'C:/Windows/Fonts/Arial/ariblk.ttf', 40)
    #构造字体颜色
    fontcolor1 = (255, random.randrange(0, 255), random.randrange(0, 255))
    fontcolor2 = (255, random.randrange(0, 255), random.randrange(0, 255))
    fontcolor3 = (255, random.randrange(0, 255), random.randrange(0, 255))
    fontcolor4 = (255, random.randrange(0, 255), random.randrange(0, 255))
    #绘制4个字
    draw.text((5, 2), rand_str[0], font=font, fill=fontcolor1)
    draw.text((25, 2), rand_str[1], font=font, fill=fontcolor2)
    draw.text((50, 2), rand_str[2], font=font, fill=fontcolor3)
    draw.text((75, 2), rand_str[3], font=font, fill=fontcolor4)
    #释放画笔
    del draw
    #内存文件操作
    import io
    buf = io.BytesIO()
    #将图片保存在内存中，文件类型为png
    im.save(buf, 'png')

    # 将验证码保存到session，以便后续验证
    request.session["code"] = rand_str

    #将内存中的图片数据返回给客户端，MIME类型为图片png
    return HttpResponse(buf.getvalue(), 'image/png')


# def bstitle(request):
