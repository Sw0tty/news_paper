from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from news.models import Post, Category
from news.forms import PostForm, CreatingPostForm
from news.filters import PostFilter
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required


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
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class PostDetail(DetailView):
    model = Post
    template_name = 'new.html'
    context_object_name = 'new'


class PostCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_post',)
    form_class = CreatingPostForm
    model = Post
    template_name = 'post_edit_page.html'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        if 'news' in self.request.path:
            post_type = 'NE'
        elif 'articles' in self.request.path:
            post_type = 'AR'
        self.object.type = post_type
        return super().form_valid(form)


class PostUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = ('news.change_post',)
    # redirect_field_name = '/home/'
    form_class = PostForm
    model = Post
    template_name = 'post_edit_page.html'


class PostDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('news.delete_post',)
    model = Post
    template_name = 'post_delete_page.html'
    success_url = reverse_lazy('posts_list')


class ForUsersView(LoginRequiredMixin, TemplateView):
    template_name = 'for-users.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_author'] = not self.request.user.groups.filter(name='authors').exists()
        return context


@login_required
def upgrade_me(request):
    user = request.user
    premium_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        premium_group.user_set.add(user)
    return redirect('/')


class CategoryView(ListView):
    model = Category
    template_name = 'categories.html'
    context_object_name = 'category'


@login_required
def subscribe(request):
    user = request.user
    category = Category.objects.get(id=int(request.GET['category-id']))
    category.subscribers.add(user)

    print(request.GET)
    return redirect('/categories/')


@login_required
def unsubscribe(request):
    user = request.user
    category = Category.objects.get(id=int(request.GET['category-id']))
    category.subscribers.remove(user)
    return redirect('/categories/')
