import itertools
from django.contrib.auth.models import User
from django.forms import *
from django.utils.text import slugify

from dashboard.models import Page, CtaButton, Tags, Templates


class SinglePageForm(ModelForm):

    status = ChoiceField(choices=Page.statusChoices, widget=RadioSelect(), required=False)
    show_in_homepage = ChoiceField(choices=Page.homePageVisibility, widget=RadioSelect(), required=False, initial=1)
    description=CharField(widget=Textarea(attrs={'class': 'hide form-control description','lines':2}),required=False)
    category = ModelMultipleChoiceField(queryset=Page.objects.filter(type=1),widget=SelectMultiple(attrs={'class': 'form-control'}), required=True)


    class Meta:
        model = Page
        fields = ['short_title','title', 'description', 'meta_keywords','meta_description','status','slug','category','templates','show_in_homepage','main_image','main_image_quote','main_image_quote_sub']
        widgets = {'title': TextInput(attrs={'class': 'form-control'}),
                   'short_title': TextInput(attrs={'class': 'form-control'}),
                   'slug': TextInput(attrs={'class': 'form-control'}),
                   'meta_keywords': TextInput(attrs={'class': 'form-control'}),
                   'main_image_quote': TextInput(attrs={'class': 'form-control'}),
                   'main_image_quote_sub': TextInput(attrs={'class': 'form-control'}),
                   'templates': SelectMultiple(attrs={'class': 'form-control templates-input'}),
                   'meta_description': Textarea(attrs={'class': 'form-control','lines':2})

                   }

class CategoryPageForm(ModelForm):
    parent = ModelChoiceField(queryset=Page.objects.filter(parent=None,type=1),
                              widget=Select(attrs={'class': 'form-control'}), required=False)
    status = ChoiceField(choices=Page.statusChoices, widget=RadioSelect(), required=False)
    show_in_homepage = ChoiceField(choices=Page.homePageVisibility, widget=RadioSelect(), required=False, initial=1)
    description=CharField(widget=Textarea(attrs={'class': 'hide form-control description','lines':2}),required=False)



    class Meta:
        model = Page
        fields = ['parent','short_title','title', 'description', 'meta_keywords','meta_description','status','slug','templates','show_in_homepage','main_image','main_image_quote','main_image_quote_sub']
        widgets = {'title': TextInput(attrs={'class': 'form-control'}),
                   'short_title': TextInput(attrs={'class': 'form-control'}),
                   'main_image_quote': TextInput(attrs={'class': 'form-control'}),
                   'main_image_quote_sub': TextInput(attrs={'class': 'form-control'}),
                   'slug': TextInput(attrs={'class': 'form-control'}),
                   'meta_keywords': TextInput(attrs={'class': 'form-control'}),
                   'templates': SelectMultiple(attrs={'class': 'form-control templates-input'}),
                   'meta_description': Textarea(attrs={'class': 'form-control','lines':2})

                   }
class LandingPageForm(ModelForm):

    status = ChoiceField(choices=Page.statusChoices, widget=RadioSelect(), required=False)
    show_in_homepage = ChoiceField(choices=Page.homePageVisibility, widget=RadioSelect(), required=False, initial=1)
    description=CharField(widget=Textarea(attrs={'class': 'hide form-control description','lines':2}),required=False)

    class Meta:
        model = Page
        fields = ['short_title','title', 'description', 'meta_keywords','meta_description','status','slug','templates','show_in_homepage','main_image']
        widgets = {'title': TextInput(attrs={'class': 'form-control'}),
                   'short_title': TextInput(attrs={'class': 'form-control'}),
                   'slug': TextInput(attrs={'class': 'form-control'}),
                   'meta_keywords': TextInput(attrs={'class': 'form-control'}),
                   'templates': SelectMultiple(attrs={'class': 'form-control templates-input'}),
                   'meta_description': Textarea(attrs={'class': 'form-control','lines':2})

                   }

class TemplateTagForm(Form):
    templates= ModelMultipleChoiceField(queryset=Templates.objects.all(),
                             widget=SelectMultiple(attrs={'class': 'form-control templates-input'}), required=True)


class CtaForm(ModelForm):
    name = CharField(widget=TextInput(attrs={'class': 'form-control'}),required=False)
    url = CharField(widget=TextInput(attrs={'class': 'form-control'}), required=False)
    class Meta:
        model = CtaButton
        fields = ['name', 'url']

class TagForm(ModelForm):
    title = CharField(widget=TextInput(attrs={'class': 'form-control'}),required=True)

    class Meta:
        model = Tags
        fields = ['title']


class AddPageForm(Form):
    type = ChoiceField(choices=Page.typeChoices, widget=Select(attrs={'class': 'form-control'}), required=False)

class PageStrippedForm(ModelForm):

    class Meta:
        model = Page
        fields = ['title', 'description']
        widgets = {'title': TextInput(attrs={'class': 'form-control'}),
                   'description': Textarea(attrs={'class': 'hide form-control description','lines':2}),


                   }

class UserAssignForm(ModelForm):
    assigned_user=ModelChoiceField(queryset=User.objects.all(),
                                   widget=Select(attrs={'class': 'form-control'}))
    page_id=IntegerField(widget=HiddenInput(attrs={'class': 'form-control modal_page_id'}))
    class Meta:
        model = Page
        fields =['page_id','assigned_user']

class RedirectForm(ModelForm):
    redirect_to = ModelChoiceField(queryset=Page.objects.filter(deleted=0),
                                     widget=Select(attrs={'class': 'form-control'}),required=False)
    page_id = IntegerField(widget=HiddenInput(attrs={'class': 'form-control modal_page_id'}))

    class Meta:
        model = Page
        fields = ['page_id', 'redirect_to']

class PageStatusForm(ModelForm):
    status=ChoiceField(choices=Page.statusChoices, widget=Select(attrs={'class': 'form-control'}), required=True)
    page_id=IntegerField(widget=HiddenInput(attrs={'class': 'form-control modal_page_id'}))
    class Meta:
        model = Page
        fields =['page_id','status']


