from django.contrib import admin
from .models import Article_base,Author_base,Category,ReadTime
# Register your models here.

#自定义后台
#文章模型
@admin.register(Article_base)
class ArticleAdmin(admin.ModelAdmin):
    #后台文章列表显示字段
    list_display = ('id','title','author','check_user','get_read_time','category','pub_date','update_time','weight','is_draft',)
    #按照id升序排列
    ordering =('id',)

#阅读计数模型
'''
@admin.register(ReadTime)
class ReadtimeAdmin(admin.ModelAdmin):
    list_display = ('id','article_base','read_time')
'''


#作者模型
@admin.register(Author_base)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('id','name','create_time')

#分类模型
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id','name')

#注册到自定义后台
'''
admin.site.register(Article_base,ArticleAdmin)
admin.site.register([Author_base,Category])
'''

