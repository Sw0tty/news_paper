from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from news.models import Post
from news.forms import PostForm
from news.filters import PostFilter
from django.urls import reverse_lazy


class PostList(ListView):
    model = Post
    template_name = 'news.html'
    context_object_name = 'news'
    ordering = '-datetime_in'
    paginate_by = 10


class PostSearch(ListView):
    model = Post
    template_name = 'search.html'
    context_object_name = 'news'
    ordering = '-datetime_in'

    def get_queryset(self):
        # Получаем обычный запрос
        queryset = super().get_queryset()
        # Используем наш класс фильтрации.
        # self.request.GET содержит объект QueryDict, который мы рассматривали
        # в этом юните ранее.
        # Сохраняем нашу фильтрацию в объекте класса,
        # чтобы потом добавить в контекст и использовать в шаблоне.
        self.filterset = PostFilter(self.request.GET, queryset)
        # Возвращаем из функции отфильтрованный список товаров
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Добавляем в контекст объект фильтрации.
        context['filterset'] = self.filterset
        return context


class PostDetail(DetailView):
    model = Post
    template_name = 'new.html'
    context_object_name = 'new'


class PostCreate(CreateView):
    form_class = PostForm
    model = Post
    template_name = 'post_edit_page.html'

    def form_valid(self, form):

        return super().form_valid(form)


class PostUpdate(UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'post_edit_page.html'


class PostDelete(DeleteView):
    model = Post
    template_name = 'post_delete_page.html'
    success_url = reverse_lazy('posts_list')
