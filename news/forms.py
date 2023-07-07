from django.shortcuts import render
from django import forms
from django.core.exceptions import ValidationError
from news.models import Post
from django.contrib.auth.models import Group, User
from allauth.account.forms import SignupForm


class PostForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        self.fields['name'].label = 'Наименование'
        self.fields['content'].label = 'Содержание'
        self.fields['category'].empty_label = None
        self.fields['category'].label = 'Категория'
        self.fields['author'].label = 'Автор'
        self.fields['author'].empty_label = 'Выберите автора'
        self.fields['author'].disabled = True

    class Meta:
        model = Post

        fields = ['name',
                  'content',
                  'author',
                  'category']


class CreatingPostForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(CreatingPostForm, self).__init__(*args, **kwargs)
        self.fields['name'].label = 'Наименование'
        self.fields['content'].label = 'Содержание'
        self.fields['category'].empty_label = None
        self.fields['category'].label = 'Категория'
        self.fields['author'].label = 'Автор'
        self.fields['author'].empty_label = 'Выберите автора'

    class Meta:
        model = Post

        fields = ['name',
                  'content',
                  'author',
                  'category']


class BasicSignupForm(SignupForm):

    def save(self, request):
        user = super(BasicSignupForm, self).save(request)
        basic_group = Group.objects.get(name='common')
        basic_group.user_set.add(user)
        return user


class UserForm(forms.ModelForm):

    # def __init__(self, *args, **kwargs):
    #     super(UserForm, self).__init__(*args, **kwargs)
    #     self.fields['username'].label = 'Имя'
    #     self.fields['password'].label = 'Пароль'
    #     self.fields['email'].label = 'Почта'

    class Meta:
        model = User

        fields = ['username',
                  'password',
                  'email'
                  ]
