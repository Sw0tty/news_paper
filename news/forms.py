from django import forms
from django.core.exceptions import ValidationError
from news.models import Post, User, Category, PostCategories, Author


class PostForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        self.fields['name'].label = 'Имя'
        self.fields['type'].label = 'Тип'
        self.fields['category'].empty_label = None
        self.fields['category'].label = 'Категория'
        self.fields['author'].label = 'Автор'
        self.fields['author'].empty_label = 'Выберите автора'

    class Meta:
        model = Post

        fields = ['name',
                  'type',
                  'content',
                  'author',
                  'category']
