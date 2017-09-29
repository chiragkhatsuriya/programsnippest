from django.contrib.auth.models import Group, User
from django.forms import *

from users.models import UserProfile


class UserProfileForm(ModelForm):
    class Meta:
        model=UserProfile
        fields=['phone_number','age','gender']
        widgets = {'phone_number': NumberInput(attrs={'class': 'form-control'}),'age': NumberInput(attrs={'class': 'form-control'}),'gender': Select(attrs={'class': 'form-control'})}


class UserForm(ModelForm):
    def __init__(self, user, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        if user.groups.filter(name__in=['content writer']):
            del self.fields["groups"]
    groups=ModelMultipleChoiceField(queryset=Group.objects.all(),required=False,widget=SelectMultiple(attrs={'class': 'form-control'}))

    class Meta:
        model=User
        fields=['first_name','last_name','email','groups']
        widgets = {'first_name': TextInput(attrs={'class': 'form-control'}),
                   'last_name': TextInput(attrs={'class': 'form-control'}),
                   'email': EmailInput(attrs={'class': 'form-control'}),

                   }



class PasswordForm(Form):
    password = CharField(widget=PasswordInput(attrs={'class': 'form-control'}), required=True)
    confirm_password = CharField(widget=PasswordInput(attrs={'class': 'form-control'}), required=True)
