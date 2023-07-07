from django.db.models.signals import post_save, post_delete, m2m_changed
from news.models import Post, Category, PostCategories
from django.dispatch import receiver
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from news.tasks import new_post
from datetime import datetime, timedelta


@receiver(m2m_changed, sender=PostCategories)
def notify_me(sender, instance, **kwargs):

    new_post.apply_async([instance.id], countdown=5)

    # if instance.type == 'AR':
    #     post_type = 'articles'
    # else:
    #     post_type = 'news'
    #
    # html_content = render_to_string(
    #     'post_created.html',
    #     {
    #         'post': instance,
    #         'post_type': post_type,
    #     }
    # )
    #
    # subject = f'New post announced'
    #
    # subs = [i.subscribers.all() for i in instance.category.all()]
    # msg = EmailMultiAlternatives(
    #     subject=subject,
    #     body=instance.content,
    #     from_email='@yandex.ru',
    #     to=[j.email for i in subs for j in i],
    # )
    # msg.attach_alternative(html_content, "text/html")
    # msg.send()


@receiver(post_save, sender=Post)
def notify_me(sender, instance, created, **kwargs):

    new_post.delay(instance.id)

    # if instance.type == 'AR':
    #     post_type = 'articles'
    # else:
    #     post_type = 'news'
    #
    # changed = True
    # html_content = render_to_string(
    #     'post_created.html',
    #     {
    #         'post': instance,
    #         'changed': changed,
    #         'post_type': post_type,
    #     }
    # )
    #
    # subject = f"""Post refreshed"""
    #
    # subs = [i.subscribers.all() for i in instance.category.all()]
    # msg = EmailMultiAlternatives(
    #     subject=subject,
    #     body=instance.content,
    #     from_email='@yandex.ru',
    #     to=[j.email for i in subs for j in i],
    # )
    # msg.attach_alternative(html_content, "text/html")  # добавляем html
    # msg.send()
