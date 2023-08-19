from django.contrib import admin
from news.models import Post, Author, Category, PostCategories, Comment


class PostAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'author', 'post_category')
    list_filter = ('type', 'category__category_name')


class AuthorAdmin(admin.ModelAdmin):
    list_display = ('user', 'user_rating')
    # list_filter = ('type', 'category__category_name')


admin.site.register(Post, PostAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Category)
admin.site.register(PostCategories)
admin.site.register(Comment)
