from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User

# Create your models here.
class Comment(models.Model):
    #固定格式,引用外App外键
    content_type=models.ForeignKey(ContentType,on_delete=models.DO_NOTHING)
    object_id=models.PositiveIntegerField()
    content_object=GenericForeignKey('content_type','object_id')

    #自有字段
    text= models.TextField('评论内容')
    comment_time=models.DateTimeField('评论时间',auto_now_add=True)
    user=models.ForeignKey(User,on_delete=models.DO_NOTHING)
    class Meta:
        ordering=['-comment_time']