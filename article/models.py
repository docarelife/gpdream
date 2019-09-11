from django.db import models
#django自带用户模型
from django.contrib.auth.models import User
from ckeditor_uploader.fields import RichTextUploadingField
from django.db.models.fields import exceptions
from django.contrib.contenttypes.models import ContentType
from read_statistics.models import ReadTime

# Create your models here.
# 通用作者模型
class Author_base(models.Model):
    name = models.CharField('作者姓名', max_length=20)
    create_time = models.DateTimeField('创建时间')

    def __str__(self):
        return self.name

# 分类模型
class Category(models.Model):
    name = models.CharField('分类名', max_length=50)

    def __str__(self):
        return self.name

# 通用文章模型
class Article_base(models.Model):
    # 文章标题
    title = models.CharField('文章标题', max_length=200)
    # 文章简介
    info = models.CharField('文章简介', max_length=400)
    # 文章标签
    tags = models.CharField('文章标签', max_length=100)
    # 文章正文
    content = RichTextUploadingField()
    # 分类
    category = models.ForeignKey(Category,verbose_name='分类', on_delete=models.DO_NOTHING)
    # 文章作者
    author = models.ForeignKey(Author_base,verbose_name='文章作者',on_delete=models.DO_NOTHING)
    #django自带用户管理:删文章不删作者；default=1,表示admin用户的主键为1
    check_user=models.ForeignKey(User,verbose_name='审查人',on_delete=models.DO_NOTHING,default=1)
    # 创建时间
    pub_date = models.DateTimeField('创建时间', auto_now_add=True)
    # 更新时间
    update_time = models.DateTimeField('更新时间', auto_now=True)

    # 阅读次数
    '''
    read_times = models.PositiveIntegerField('阅读次数',default=0)
    '''

    # 权重
    weight = models.PositiveIntegerField('权重',default=0)
    #是否为草稿
    is_draft=models.BooleanField('草稿?',default=False)

    def __str__(self):
        return '文章%s：%s' % (self.id,self.title)

    #模型的阅读次数累计方法
    '''
    #方法一：新建方法
    def increase_views(self):
        self.read_times += 1
        self.save(update_fields=['read_times'])
    '''
    '''
    #方法二：新建模型
    def get_read_time(self):
        try:
            return self.readtime.read_time
        except exceptions.ObjectDoesNotExist:
            return 0
    '''
    #方法三：新建阅读统计app
    def get_read_time(self):
        try:
            content_type=ContentType.objects.get_for_model(self)
            readtime=ReadTime.objects.get(content_type=content_type,object_id=self.id)
            return readtime.read_time
        except exceptions.ObjectDoesNotExist:
            return 0

    #获得关联模型的字段、属性和方法

    #元数据类
    class Meta:
        #设置排序字段
        ordering=['-pub_date']

'''
#文章阅读计数模型
class ReadTime(models.Model):
    read_time=models.IntegerField('阅读次数',default=0)
    article_base=models.OneToOneField(Article_base,on_delete=models.DO_NOTHING)
    def __str__(self):
        return str(self.read_time)
'''
