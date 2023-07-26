from celery import shared_task
from NewsPaper.settings import DEFAULT_FROM_EMAIL
from news.models import Post
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from datetime import datetime, timedelta
from news.models import Category


@shared_task
def new_post(instance_id):

    instance = Post.objects.get(id=instance_id)

    if instance.type == 'AR':
        post_type = 'articles'
    else:
        post_type = 'news'

    html_content = render_to_string(
        'post_created.html',
        {
            'post': instance,
            'post_type': post_type,
        }
    )

    subject = f'New post announced'

    subs = [i.subscribers.all() for i in instance.category.all()]
    msg = EmailMultiAlternatives(
        subject=subject,
        body=instance.content,
        from_email=DEFAULT_FROM_EMAIL,
        to=[j.email for i in subs for j in i],
    )
    msg.attach_alternative(html_content, "text/html")
    msg.send()


@shared_task
def refreshed_post(instance_id):

    instance = Post.objects.get(id=instance_id)

    if instance.type == 'AR':
        post_type = 'articles'
    else:
        post_type = 'news'

    changed = True
    html_content = render_to_string(
        'post_created.html',
        {
            'post': instance,
            'changed': changed,
            'post_type': post_type,
        }
    )

    subject = f"""Post refreshed"""

    subs = [i.subscribers.all() for i in instance.category.all()]
    msg = EmailMultiAlternatives(
        subject=subject,
        body=instance.content,
        from_email=DEFAULT_FROM_EMAIL,
        to=[j.email for i in subs for j in i],
    )
    msg.attach_alternative(html_content, "text/html")
    msg.send()


@shared_task
def new_posts_last_week_sender():

    week_ago = (datetime.now() - timedelta(days=7)).date()

    for i in Category.objects.all():
        if i.subscribers.all():
            subs = [j for j in i.subscribers.all()]
            posts = Post.objects.filter(category=i.id, datetime_in__gt=week_ago)

            newsletter = True
            html_content = render_to_string(
                'post_created.html',
                {
                    'newsletter': newsletter,
                    'posts': posts,
                }
            )

            subject = """Posts for last week"""

            msg = EmailMultiAlternatives(
                subject=subject,
                # body=,
                from_email=DEFAULT_FROM_EMAIL,
                to=[i.email for i in subs],
            )
            msg.attach_alternative(html_content, "text/html")
            msg.send()
