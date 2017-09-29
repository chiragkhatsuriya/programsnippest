from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.db import models

class UserProfile(models.Model):
    GENDERCHOICE=(('male','Male'),('female','Female'))
    user = models.OneToOneField(User, related_name='profile')
    phone_number=models.TextField(default='')
    age=models.IntegerField(default=0)
    gender=models.CharField(max_length=10,choices=GENDERCHOICE)
    profile_image=models.TextField(default='')
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        db_table="user_profile"

    def __getattribute__(self, name):
        attr = models.Model.__getattribute__(self, name)
        if name == 'profile_image' and not attr:
            return static('imgs/anonymous.png')
        return attr
