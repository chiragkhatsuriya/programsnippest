from django import template
from django.contrib.auth.models import Group



register=template.Library()


@register.filter(name='is_moderator')
def is_moderator(user):
    if user.is_superuser:
        return True
    group = Group.objects.get(name='moderator')
    return group in user.groups.all()




