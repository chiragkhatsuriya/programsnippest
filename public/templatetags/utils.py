import urllib


from django import template

from cms.settings import STATIC_COLORS_TAB

register=template.Library()

@register.filter(name='getTabColorClassFromIndex')
def getTabColorClassFromIndex(idx):
    return "tab-" + STATIC_COLORS_TAB[ idx % STATIC_COLORS_TAB.__len__()]