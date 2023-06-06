import random

from django.shortcuts import render
from django.views.generic import ListView, DetailView
from news.models import Post
from random import randint


class PostList(ListView):
    model = Post
    template_name = 'news.html'
    context_object_name = 'news'
    ordering = '-datetime_in'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['random_index'] = random.randint(1, len(Post.objects.all()))
        return context


class PostDetail(DetailView):
    model = Post
    template_name = 'new.html'
    context_object_name = 'new'
    pk_url_kwarg = 'id'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['random_index'] = random.randint(1, len(Post.objects.all()))
        return context
