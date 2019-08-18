from django.conf.urls import url

from app import views

urlpatterns = [
    url(r'^index/$',views.index),
    url(r'^login/$',views.login,name='login'),
    url(r'^logout/$',views.logout,name='logout'),
    url(r'^register/$',views.register,name='register'),
    url(r'^details/$',views.details),
    url(r'^base/$', views.base),
    url(r'^basepersonal/$', views.basepersonal),
    url(r'^bsavatar/$', views.bsavatar),

    url(r'^bsprofile/$', views.bsprofile),
    url(r'^bspfcontact/$', views.bspfcontact),
    url(r'^bspfedu/$', views.bspfedu),
    url(r'^bspfwork/$', views.bspfwork),
    url(r'^bspfinformation/$', views.bspfinformation),

    url(r'^bscredit/$', views.bscredit),
    url(r'^bscdrecord/$', views.bscdrecord),
    url(r'^bscdrule/$', views.bscdrule),

    url(r'^bsusergroup/$', views.bsusergroup),
    url(r'^bsugbuy/$', views.bsugbuy),
    url(r'^bsugmine/$', views.bsugmine),


    url(r'^bsprivacy/$', views.bsprivacy),
    url(r'^bsprivacy/$', views.bsprivacy),



    url(r'^bspwsafe/$', views.bspwsafe),
    url(r'^bspromotion/$', views.bspromotion),


    url(r'^verifycode/$', views.verifycode),
    # url(r'^post/(?P<pk>\d+)$', views.post),

]
