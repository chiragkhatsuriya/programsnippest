import django_filters
from django import forms
from django.contrib.auth.models import User, Group
from django.forms import TextInput, Select

from dashboard.models import Page, Tags


class PageFilter(django_filters.FilterSet):

    title = django_filters.CharFilter(lookup_expr='icontains',widget=TextInput(attrs={'class': 'form-control'}))
    assigned_user = django_filters.ModelChoiceFilter(queryset=User.objects.all(),lookup_expr='exact',widget=Select(attrs={'class': 'form-control'}))
    status = django_filters.ChoiceFilter(choices=Page.statusChoices,lookup_expr='exact', widget=Select(attrs={'class': 'form-control'}))
    type = django_filters.ChoiceFilter(choices=Page.typeChoices, lookup_expr='exact',
                                         widget=Select(attrs={'class': 'form-control'}))
    class Meta:
        model = Page
        fields = ['title', 'assigned_user','status','type' ]


class TagFilter(django_filters.FilterSet):

    title = django_filters.CharFilter(lookup_expr='icontains',widget=TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Tags
        fields = ['title']