from cms.settings import STATIC_COLORS
from random import randint

def is_moderator(user):
    if user.is_superuser:
        return True
    return user.groups.filter(name__in=['moderator'])

def getBorderColorClassFromIndex(idx):
    idx = idx % len(STATIC_COLORS)
    return STATIC_COLORS[randint(0, idx )]
