from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

# Create your models here.
class ReadTime(models.Model):
    read_time=models.IntegerField('阅读计数',default=0)

    #固定格式
    content_type=models.ForeignKey(ContentType,on_delete=models.DO_NOTHING)
    object_id=models.PositiveIntegerField()
    content_object=GenericForeignKey('content_type','object_id')
