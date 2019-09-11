from django.shortcuts import render,redirect
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse

from .models import Comment


# Create your views here.
def update_comment(request):
    #跳转（重定向）链接
    referer = request.META.get('HTTP_REFERER', reverse('article:article_list'))
    #获取请求数据
    user=request.user

    #数据检查
    if not user.is_authenticated:
        return render(request, 'error.html', {'message':'用户尚未登录','redirect_to':referer})

    text=request.POST.get('text','').strip()
    if text=='':
        return render(request, 'error.html', {'message':'评论不能为空','redirect_to':referer})
    try:
        content_type = request.POST.get('content_type', '')
        object_id = int(request.POST.get('object_id', ''))
        # 获得模型对象
        # --获得ContentType模型中的content_type对应的模型
        model_class = ContentType.objects.get(model=content_type).model_class()
        # --从获取的模型中根据id找到对应文章的对象
        model_obj = model_class.objects.get(pk=object_id)
    except Exception as e:
        return render(request, 'error.html', {'message':'评论对象不存在','redirect_to':referer})

    #检查通过，保存添加数据
    comment=Comment()
    comment.user=user
    comment.text=text
    comment.content_object=model_obj
    comment.save()
    return redirect(referer)
