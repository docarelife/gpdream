from django.db import models
#普通文本编辑器
from ckeditor.fields import RichTextField
#带图片文件上传的文本编辑器
from ckeditor_uploader.fields import RichTextUploadingField

from django.utils import timezone
import datetime
# Create your models here.
#作者模型

class Author(models.Model):
    name=models.CharField('作者姓名',max_length=20)
    email=models.EmailField('电子邮箱',max_length=50)
    phone_num=models.CharField('手机号码',max_length=20)
    reg_date=models.DateTimeField('注册时间')
    def __str__(self):
        return self.name
    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.reg_date <= now
    was_published_recently.admin_order_field = 'reg_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Register recently?'

#文章模型
class Article(models.Model):
    title=models.CharField('文章标题',max_length=200)
    #普通
    #content=RichTextField('文章正文')
    #带文件上传
    content=RichTextUploadingField('文章正文')
    pub_date=models.DateTimeField('发布日期')
    author=models.ForeignKey(Author,on_delete=models.CASCADE)
    def __str__(self):
        return self.title

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now
    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'