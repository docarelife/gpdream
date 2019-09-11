from django.urls import path, include
from . import views

app_name = 'article'
urlpatterns = [
    path('', views.article_list, name='article_list'),
    path('<int:article_id>/', views.article_detail, name='article_detail'),
    #按‘分类’获取文章列表路由
    path('category/<int:article_category_id>/', views.article_list_bycategory, name='article_list_bycategory'),
    path('date/<int:year>/<int:month>/', views.article_list_bydate, name='article_list_bydate'),
    path('comment/',include('comment.urls'),name='comment'),
    path('login/',views.login,name='login'),
    path('register/',views.register,name='register'),
]
