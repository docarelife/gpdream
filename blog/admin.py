from django.contrib import admin
from .models import Author,Article

# Register your models here.

# ######模型关联管理
# #提供3个Choice对象的编辑区域
# class ArticleInline(admin.TabularInline):
#     model = Article
#     extra = 1
# class AuthorAdmin(admin.ModelAdmin):
#     #question列表页，显示的字段
#     list_display = ('name', 'email', 'phone_num','reg_date')
#     #单个问题详情页，字段分类显示
#     fieldsets = [
#         (None,               {'fields': ['name']}),
#         ('Date information', {'fields': ['reg_date'], 'classes': ['collapse']}),
#     ]
#     #每个问题关联的Choice，在Question内编辑
#     inlines = [ArticleInline]
#     #页面右边多出了一个基于pub_date的过滤面板
#     list_filter = ['reg_date']
#     #添加搜索
#     search_fields = ['name']
#
# #在后台管理页面注册
# admin.site.register(Author, AuthorAdmin)


admin.site.register([Author,Article])