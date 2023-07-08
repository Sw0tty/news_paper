from django.db.models.signals import post_save, post_delete, m2m_changed
from news.models import Post, Category, PostCategories
from django.dispatch import receiver
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from news.tasks import new_post, refreshed_post
from datetime import datetime, timedelta


@receiver(m2m_changed, sender=PostCategories)
def notify_me(sender, instance, action, **kwargs):

    if instance.created and 'post_add' in action:
        new_post.apply_async([instance.id], countdown=5)


@receiver(post_save, sender=Post)
def notify_me(sender, instance, created, **kwargs):

    refreshed_post.delay(instance.id)
    instance.created = created
