from django.urls import path
from . import views


urlpatterns=[
    path('',views.info,name='info'),
    path('<int:article_id>/',views.detail,name='detail'),
    path('edit/',views.edit,name='edit'),
]