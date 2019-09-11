from django.shortcuts import render, redirect,HttpResponse, get_object_or_404, get_list_or_404
from django.core.paginator import Paginator
from django.conf import settings
from django.db.models import Count
from django.contrib.contenttypes.models import ContentType
from django.contrib import auth
from django.urls import reverse
from .models import Article_base, Category
from read_statistics.models import ReadTime
from comment.models import Comment
from .forms import LoginForm,RegForm
from django.contrib.auth.models import User


# 可抽离出公共部分封装为方法
# --传入request、文章列表，返回公共上下文部分字典
def get_common_date(request, articles):
    # 获取页码参数
    page_num = request.GET.get('page', 1)
    # 获取全部文章列表(过滤掉is_draft=True：是草稿的)
    articles = get_list_or_404(Article_base, is_draft=False)

    # 分页开始
    # --每页显示文章数
    each_page_num = settings.EACH_PAGE_NUM
    # --实例化分页器
    paginator = Paginator(articles, each_page_num)
    # --当前页码内所对应文章列表的对象
    page_of_articles = paginator.get_page(page_num)
    # --获取当前当前页码
    current_page_num = page_of_articles.number
    # --页码范围（前后各2个页码）
    page_range = list(range(max(current_page_num - 2, 1), current_page_num)) + list(range(current_page_num,
                                                                                          min(current_page_num + 2,
                                                                                              paginator.num_pages) + 1))
    # --'...'省略中间页码
    if page_range[0] - 1 >= 2:
        page_range.insert(0, '...')
    if paginator.num_pages - page_range[-1] >= 2:
        page_range.append('...')
    # --首尾两个页码
    if page_range[0] != 1:
        page_range.insert(0, 1)
    if page_range[-1] != paginator.num_pages:
        page_range.append(paginator.num_pages)
    # 分页结束

    # 获得分类模型的查询对象
    categorys = get_list_or_404(Category)

    # 按时间分类模块
    # --获得文章时间集合
    pub_dates = Article_base.objects.dates('pub_date', 'month', order='DESC')

    # 组装上下文字典
    context = {}
    # 底部页码显示部分的列表集合
    context['page_range'] = page_range
    # 分页器处理过的文章查询对象
    context['page_of_articles'] = page_of_articles
    # 分类模型的查询对象
    context['categorys'] = categorys
    # 文章发布时间集合
    context['pub_dates'] = pub_dates
    return context


# 获取全部文章列表--视图
def article_list(request):
    # 获取页码参数
    page_num = request.GET.get('page', 1)
    # 获取全部文章列表(过滤掉is_draft=True：是草稿的)
    articles = get_list_or_404(Article_base, is_draft=False)

    # 分页开始
    # --每页显示文章数
    each_page_num = settings.EACH_PAGE_NUM
    # --实例化分页器
    paginator = Paginator(articles, each_page_num)
    # --当前页码内所对应文章列表的对象
    page_of_articles = paginator.get_page(page_num)
    # --获取当前当前页码
    current_page_num = page_of_articles.number
    # --页码范围（前后各2个页码）
    page_range = list(range(max(current_page_num - 2, 1), current_page_num)) + list(range(current_page_num,
                                                                                          min(current_page_num + 2,
                                                                                              paginator.num_pages) + 1))
    # --'...'省略中间页码
    if page_range[0] - 1 >= 2:
        page_range.insert(0, '...')
    if paginator.num_pages - page_range[-1] >= 2:
        page_range.append('...')
    # --首尾两个页码
    if page_range[0] != 1:
        page_range.insert(0, 1)
    if page_range[-1] != paginator.num_pages:
        page_range.append(paginator.num_pages)
    # 分页结束

    # 获得分类模型查询对象和对应文章数
    # 方法一
    '''
    #获得分类模型的查询对象
    categorys=get_list_or_404(Category)
    #用来保存携带新属性（数量）的分类的列表
    category_list=[]
    #获得文章各分类内文章的数量
    for category in categorys:
        article_count=Article_base.objects.filter(category=category).count()
        #文章数量添加为Category类的实例的一个属性，携带到模板
        category.article_count=article_count
        category_list.append(category)
    '''
    # 方法二：
    category_list = Category.objects.annotate(article_count=Count('article_base'))

    # 按时间归档文章模块
    # --获得文章时间集合
    pub_dates = Article_base.objects.dates('pub_date', 'month', order='DESC')
    pub_dates_dist = {}
    for pub_date in pub_dates:
        article_count = Article_base.objects.filter(pub_date__year=pub_date.year,
                                                    pub_date__month=pub_date.month).count()
        pub_dates_dist[pub_date] = article_count

    # 组装上下文字典
    context = {}
    # 本页需显示的页码范围
    context['page_range'] = page_range
    # 本页需显示的文章对象
    context['page_of_articles'] = page_of_articles
    # 带数量的分类对象
    context['categorys'] = category_list
    # 带数量的日期归档字典
    context['pub_dates'] = pub_dates_dist
    return render(request, 'article/article_list.html', context)


# 文章详情页--视图
def article_detail(request, article_id):
    # 按文章ID，找到文章查询模型
    article = get_object_or_404(Article_base, pk=article_id)

    # 调用模型的阅读次数累计方法
    if not request.COOKIES.get('article_%s_read' % article_id):
        # 如果相关cookie不存在，才调用阅读量递增函数
        '''
        #模型内阅读统计方法
        Article_base.increase_views(article)
        '''
        '''
        #新建阅读统计模型后的阅读量获得方法
        if ReadTime.objects.filter(article_base=article).count():
            #存在阅读记录
            readtime=ReadTime.objects.get(article_base=article)
        else:
            #不存在阅读记录
            readtime=ReadTime(article_base=article)
        #计数加1
        readtime.read_time+=1
        readtime.save()
        '''
        # 新建阅读统计App后的阅读量获得方法
        content_type = ContentType.objects.get_for_model(Article_base)
        if ReadTime.objects.filter(content_type=content_type, object_id=article_id).count():
            # 存在阅读记录
            readtime = ReadTime.objects.get(content_type=content_type, object_id=article_id)
        else:
            # 不存在阅读记录
            readtime = ReadTime(content_type=content_type, object_id=article_id)
        # 计数加1
        readtime.read_time += 1
        readtime.save()

    # 获取上一篇文章
    previous_article = Article_base.objects.filter(pub_date__gt=article.pub_date).last()
    # 获得下一篇文章
    next_article = Article_base.objects.filter(pub_date__lt=article.pub_date).first()
    # 存储到上下文字典

    # 获取评论列表
    article_content_type = ContentType.objects.get_for_model(article)
    comments = Comment.objects.filter(content_type=article_content_type, object_id=article.id)

    context = {}
    context['article'] = article
    context['previous_article'] = previous_article
    context['next_article'] = next_article
    context['comments'] = comments

    # 取出相应对象，对其设置cookie
    response = render(request, 'article/article_detail.html', context)
    response.set_cookie('article_%s_read' % article_id, 'True')
    return response


# 按分类显示文章列表--视图
def article_list_bycategory(request, article_category_id):
    # 获取文章分类
    current_category = get_object_or_404(Category, pk=article_category_id)
    # 获取目标分类下全部文章的列表
    articles = get_list_or_404(Article_base, category=current_category)
    # 获取页码参数
    page_num = request.GET.get('page', 1)
    # ----分页开始----
    # 每页显示文章数
    each_page_num = settings.EACH_PAGE_NUM
    # 实例化分页器
    paginator = Paginator(articles, each_page_num)
    # 当前页码内所对应文章列表的对象
    page_of_articles = paginator.get_page(page_num)
    # 获取当前当前页码
    current_page_num = page_of_articles.number
    # 页码范围（前后各2个页码）
    page_range = list(range(max(current_page_num - 2, 1), current_page_num)) + list(range(current_page_num,
                                                                                          min(current_page_num + 2,
                                                                                              paginator.num_pages) + 1))
    # '...'省略中间页码
    if page_range[0] - 1 >= 2:
        page_range.insert(0, '...')
    if paginator.num_pages - page_range[-1] >= 2:
        page_range.append('...')

    # 首尾两个页码
    if page_range[0] != 1:
        page_range.insert(0, 1)
    if page_range[-1] != paginator.num_pages:
        page_range.append(paginator.num_pages)
    # ----分页结束----
    # 获得分类模型的查询对象
    categorys = get_list_or_404(Category)

    context = {}
    context['page_range'] = page_range
    context['page_of_articles'] = page_of_articles
    context['current_category'] = current_category
    context['categorys'] = categorys
    return render(request, 'article/article_list_bycategory.html', context)


# 按日期显示文章列表--视图
def article_list_bydate(request, year, month):
    # 获取页码参数
    page_num = request.GET.get('page', 1)
    # 获取全部文章列表(过滤掉is_draft=True：是草稿的)
    articles = Article_base.objects.filter(pub_date__year=year, pub_date__month=month)

    # 分页开始
    # --每页显示文章数
    each_page_num = settings.EACH_PAGE_NUM
    # --实例化分页器
    paginator = Paginator(articles, each_page_num)
    # --文章的页码
    page_of_articles = paginator.get_page(page_num)
    # --获取当前当前页码
    current_page_num = page_of_articles.number
    # --页码范围（前后各2个页码）
    page_range = list(range(max(current_page_num - 2, 1), current_page_num)) + list(range(current_page_num,
                                                                                          min(current_page_num + 2,
                                                                                              paginator.num_pages) + 1))
    # --'...'省略中间页码
    if page_range[0] - 1 >= 2:
        page_range.insert(0, '...')
    if paginator.num_pages - page_range[-1] >= 2:
        page_range.append('...')
    # --首尾两个页码
    if page_range[0] != 1:
        page_range.insert(0, 1)
    if page_range[-1] != paginator.num_pages:
        page_range.append(paginator.num_pages)
    # 分页结束

    # 获得分类模型的查询对象
    categorys = get_list_or_404(Category)

    # 按时间分类模块
    # --获得文章时间集合
    pub_dates = Article_base.objects.dates('pub_date', 'month', order='DESC')

    # 组装上下文字典
    context = {}
    context['page_range'] = page_range
    context['page_of_articles'] = page_of_articles
    context['categorys'] = categorys
    context['pub_dates'] = pub_dates
    return render(request, 'article/article_list_bydate.html', context)

#登录
def login(request):
    '''
    #自建表单验证，未使用django自带表单验证
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    user = auth.authenticate(request, username=username, password=password)
    if user is not None:
        auth.login(request, user)
        referer=request.META.get('HTTP_REFERER',reverse('article:article_list'))
        return redirect(referer)
    else:
        return render(request,'error.html',{'message':'用户名或密码错误'})
    '''

    '''
    #可代码优化:把如下内容全提出来，放到第一层
    context = {}
    context['login_form'] = login_form
    return render(request, 'login.html', context)
    '''
    if request.method == 'POST':  # 需求提交表单
        login_form=LoginForm(request.POST)
        if login_form.is_valid():
            username=login_form.cleaned_data['username']
            password=login_form.cleaned_data['password']
            user = auth.authenticate(request, username=username, password=password)
            if user is not None:
                auth.login(request, user)
                return redirect(request.GET.get('from',reverse('article:article_list')))
            else:
                login_form.add_error(None,'用户名或密码错误，请重新输入...')
                # 装进上下文字典
                context = {}
                context['login_form'] = login_form
                return render(request, 'login.html', context)
        else:
            context = {}
            context['login_form'] = login_form
            return render(request, 'login.html', context)
    else:  # 'GET'--需求显示登录页面
        # 实例化一个form表单
        login_form = LoginForm()
        # 装进上下文字典
        context = {}
        context['login_form'] = login_form
        return render(request, 'login.html', context)

#注册
def register(request):
    if request.method=='POST':
        reg_form=RegForm(request.POST)
        if reg_form.is_valid():
            username=reg_form.cleaned_data['username']
            email=reg_form.cleaned_data['email']
            password=reg_form.cleaned_data['password']
            #创建用户
            user=User.objects.create_user(username,email,password)
            user.save()
            #登录用户
            user = auth.authenticate(request, username=username, password=password)
            auth.login(request, user)
            return redirect(request.GET.get('from', reverse('article:article_list')))
    else:
        reg_form=RegForm()

    context={}
    context['reg_form']=reg_form
    return render(request,'register.html',context)