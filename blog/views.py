from django.shortcuts import render,get_object_or_404,HttpResponse

from blog.forms import ArticleForm
from .models import Author,Article
# Create your views here.

#‘文章详情页’视图
def info(request):
    return render(request,'info.html')

#‘通过ID检索显示文章详情页’视图
def detail(request,article_id):
    article=get_object_or_404(Article,pk=article_id)
    context={'article':article}
    return render(request, 'blog/article_detail.html', context)

#'富文本编辑器'视图
def edit(request):
    if request.method!='POST':
        form=ArticleForm()
    else:
        return HttpResponse('失败')
    context={'form':form}
    return render(request, 'blog/edit1.html', context)