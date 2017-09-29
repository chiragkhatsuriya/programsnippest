import django_filters
from django import forms
from django.contrib.auth.models import User, Group
from django.forms import TextInput


class UserFilter(django_filters.FilterSet):
    first_name = django_filters.CharFilter(lookup_expr='icontains', widget=TextInput(attrs={'class': 'form-control'}))
    last_name = django_filters.CharFilter(lookup_expr='icontains', widget=TextInput(attrs={'class': 'form-control'}))
    email = django_filters.CharFilter(lookup_expr='icontains', widget=TextInput(attrs={'class': 'form-control'}))
    groups = django_filters.ModelChoiceFilter(queryset=Group.objects.all(),widget=forms.Select(attrs={'class': 'form-control'}))
    class Meta:
        model = User
        fields = ['first_name', 'last_name','groups','email' ]