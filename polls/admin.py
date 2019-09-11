from django.contrib import admin
from polls.models import Question, Choice

# Register your models here.



#提供3个Choice对象的编辑区域
class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3


class QuestionAdmin(admin.ModelAdmin):
    #question列表页，显示的字段
    list_display = ('question_text', 'pub_date', 'was_published_recently')
    #单个问题详情页，字段分类显示
    fieldsets = [
        (None,               {'fields': ['question_text']}),
        ('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}),
    ]
    #每个问题关联的Choice，在Question内编辑
    inlines = [ChoiceInline]
    #页面右边多出了一个基于pub_date的过滤面板
    list_filter = ['pub_date']
    #添加搜索
    search_fields = ['question_text']

#admin.site.register([Question,Choice])
admin.site.register(Question, QuestionAdmin)