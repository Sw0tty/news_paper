from django import template
from random import choice
from news.models import Post

register = template.Library()


@register.simple_tag()
def random_new_id():
    return choice([i['id'] for i in Post.objects.all().values('id')])


