from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from django.urls import reverse
from django.core.cache import cache
from news.resources import TYPE_OF_NEW


class Post(models.Model):

    news = 'NE'
    article = 'AR'

    name = models.CharField(max_length=255)
    type = models.CharField(max_length=2, choices=TYPE_OF_NEW, default=news)
    datetime_in = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    category = models.ManyToManyField('Category', through='PostCategories')
    author = models.ForeignKey('Author', on_delete=models.CASCADE, related_name='author')
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return f"{self.content[:124]}..."

    def post_category(self):
        if self.category.all():
            return [i for i in self.category.all()]
        return "Без категории"

    def __str__(self):
        return f"{self.name}: {self.preview()}"

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        cache.delete(f'product-{self.pk}')


class Author(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author')
    user_rating = models.IntegerField(default=0)

    def update_rating(self):
        posts_rating = Post.objects.filter(author=self).aggregate(Sum('rating'))['rating__sum']
        comments_rating = Comment.objects.filter(user=self.user).aggregate(Sum('rating'))['rating__sum']
        posts_comments_rating = Comment.objects.filter(post__author=self).aggregate(Sum('rating'))['rating__sum']
        self.user_rating = (posts_rating*3) + comments_rating + posts_comments_rating
        self.save()

    def __str__(self):
        return self.user.username


class Category(models.Model):
    category_name = models.CharField(max_length=255, unique=True)
    subscribers = models.ManyToManyField(User)

    def __str__(self):
        return self.category_name.title()


class PostCategories(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_text = models.TextField()
    datetime_in = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()
