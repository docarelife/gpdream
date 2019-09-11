from django import forms
from .models import Article

class KindEditorWidget(forms.Textarea):
    class Media:
        css={'all':(
            'kindeditor/themes/default/default.css',
            'kindeditor/themes/simple/simple.css',
            )}
        js=(
            'kindeditor/kindeditor-all-min.js',
            'kindeditor/zh-CN.js',
            'kindeditor/config.js',
        )

class ArticleForm(forms.ModelForm):
    title=forms.CharField(label='文章标题',widget=forms.TextInput(attrs={'class':'input'}))
    desc=forms.CharField(label='文章描述',widget=forms.Textarea(attrs={'class':'textarea','rows':4}))
    content=forms.CharField(label='文章内容',widget=KindEditorWidget)
    class Meta:
        model=Article
        exclude=['author',]
