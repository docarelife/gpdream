"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),

    #首页路由
    path('', views.index,name='index'),

    #文章详情页路由
    path('info/', include('article.urls')),

    # 全科梦路由
    path('list/', views.list, name='list'),

    # 学无止境路由
    path('link/', views.link, name='link'),

    # 心情随笔路由
    path('share/', views.share, name='share'),

    #关于我们路由
    path('about/', views.about,name='about'),

    #留言路由
    path('gbook/', views.gbook,name='gbook'),

    #添加文件上传路由
    path('ckeditor',include('ckeditor_uploader.urls')),

    #投票路由
    path('polls/',include('polls.urls'),name='polls')
]
#富文本编辑器上传图片等文件用
urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
