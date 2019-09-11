from django import forms
from django.contrib.auth.models import User

class LoginForm(forms.Form):
    username=forms.CharField(label='用户名')
    password=forms.CharField(label='密码',widget=forms.PasswordInput)


class RegForm(forms.Form):
    username=forms.CharField(label='用户名',min_length=6,max_length=20,widget=forms.TextInput(attrs={'place_holder':'请输入用户名'}))
    email=forms.EmailField(label='邮箱',widget=forms.EmailInput(attrs={'place_holder':'请输入邮箱'}))
    password=forms.CharField(label='密码',min_length=6,widget=forms.PasswordInput(attrs={'place_holder':'请输入密码'}))
    password_again=forms.CharField(label='再输入一次',min_length=6,widget=forms.PasswordInput(attrs={'place_holder':'请再次输入密码'}))

    def clean_username(self):
        username=self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('用户名已存在')
        return username
    def clean_email(self):
        email=self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('邮箱已存在')
        return email
    def clean_password_again(self):
        password = self.cleaned_data['password']
        password_again = self.cleaned_data['password_again']
        if password!=password_again:
            raise forms.ValidationError('两次输入密码不一致')
        return password_again