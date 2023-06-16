from django.shortcuts import render

from django import forms
from django.core.exceptions import ValidationError
from news.models import Post


class PostForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
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
