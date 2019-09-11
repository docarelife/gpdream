from django.shortcuts import render



#‘首页’视图
def index(request):
    return render(request,'index.html')

#‘全科梦’视图
def list(request):
    return render(request,'list.html')

#‘学无止境’视图
def link(request):
    return render(request,'link.html')

#‘心情随笔’视图
def share(request):
    return render(request,'share.html')

#‘关于我们’视图
def about(request):
    return render(request, 'about.html')

#‘留言板’视图
def gbook(request):
    return render(request,'gbook.html')