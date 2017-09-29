import urllib


from django import template

from dashboard.models import Page, Tags

register=template.Library()

@register.filter(name='get_status_choice')
def get_status_choice(value):
    return dict(Page.statusChoices).get(value, '')

@register.filter(name='get_type_choice')
def get_type_choice(value):
    return dict(Page.typeChoices).get(value, '')

@register.filter(name='get_tag_homepage_choice')
def get_tag_homepage_choice(value):
    return dict(Tags.homePageVisibility).get(value, '')


@register.simple_tag(takes_context=True)
def url_replace(context, **kwargs):
    query = context['request'].GET.dict()
    query.update(kwargs)
    return urllib.parse.urlencode(query)