from django.db import models
from news.resources import TYPE_OF_NEW
from django.contrib.auth.models import User
from django.db.models import Sum


class Post(models.Model):

    news = 'NE'
    article = 'AR'

    name = models.CharField(max_length=255)
    type = models.CharField(max_length=2, choices=TYPE_OF_NEW, default=news)
    datetime_in = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    category = models.ManyToManyField('Category', through='PostCategories')
    author = models.ForeignKey('Author', on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return f"{self.content[:124]}..."


class Author(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    user_rating = models.IntegerField(default=0)

    def update_rating(self):
        posts_rating = Post.objects.filter(author=self).aggregate(Sum('rating'))['rating__sum']
        comments_rating = Comment.objects.filter(user=self.user).aggregate(Sum('rating'))['rating__sum']

        posts_comments = [Comment.objects.filter(post=i) for i in [j for j in Post.objects.filter(author=self)]]
        if len(posts_comments) > 1:
            posts_comments = [j for i in posts_comments for j in i]
        else:
            posts_comments = posts_comments[0]
        posts_comments_rating = sum(i.rating for i in posts_comments)

        self.user_rating = (posts_rating*3) + comments_rating + posts_comments_rating
        self.save()


class Category(models.Model):
    category_name = models.CharField(max_length=255, unique=True)


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
