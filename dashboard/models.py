from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models
from django.utils.text import slugify



class TemplateGroup(models.Model):
    group_id=models.IntegerField()
    group_name=models.CharField(max_length=255)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

class Templates(models.Model):
    ext_id=models.IntegerField()
    title = models.CharField(max_length=255)
    slug=models.SlugField(max_length=255, db_index=True,unique=True)
    description = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    template_group=models.ForeignKey(TemplateGroup,null=True)

    def __str__(self):
        return self.title

class Tags(models.Model):
    homePageVisibility = (
        (1, "yes"), (0, "no"),
    )
    title=models.CharField(max_length=128)
    show_in_homepage = models.IntegerField(default=1, choices=homePageVisibility)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    templates = models.ManyToManyField(Templates, related_name="tags", null=True, blank=True)

class Keywords(models.Model):
    keyword=models.CharField(max_length=128)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

class Page(models.Model) :
    typeChoices = (
        (1, "category"), (0, "single"),(2, "landing"),
    )
    statusChoices = (
        (1, "moderation"), (0, "new"),(2,"published"),
    )
    homePageVisibility=(
        (1, "yes"), (0, "no"),
    )
    short_title = models.CharField(max_length=255)
    title=models.CharField(max_length=255)
    main_image=models.ImageField(null=True,blank=True)
    main_image_quote = models.TextField(null=True, blank=True)
    main_image_quote_sub = models.TextField(null=True, blank=True)
    description = models.TextField()
    slug = models.SlugField(max_length=255, db_index=True,unique=True)
    parent = models.ForeignKey("self", null=True, blank=True)
    category=models.ManyToManyField("self")
    meta_keywords=models.CharField(max_length=128)
    meta_description = models.CharField(max_length=128)
    status = models.IntegerField(default=0, choices=statusChoices)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    type=models.IntegerField(default=0, choices=typeChoices)
    show_in_homepage=models.IntegerField(default=1, choices=homePageVisibility)
    view_order=models.IntegerField(null=True)
    show_in_tags=models.IntegerField(null=True)
    keywords=models.ManyToManyField(Keywords,related_name="keywords")
    assigned_user=models.ForeignKey(User,null=True,blank=True,related_name="page_users")
    templates=models.ManyToManyField(Templates,related_name="pages")
    deleted = models.IntegerField(default=0, choices=homePageVisibility)
    redirect_to=models.ForeignKey("self", null=True, blank=True,related_name="redirected_from")
    class Meta:
        db_table = "page"

    def __str__(self):
        return self.title

    def get_child_pages(self):
        return Page.objects.filter(category=self,type=0,status=2).order_by("-updated_on")

    def get_child_categories(self):
        return Page.objects.filter(parent=self, type=1, status=2)

    def get_absolute_url(self):
        return "/"+self.slug

class CtaButton(models.Model):
    page=models.OneToOneField(Page,related_name="cta")
    name=models.CharField(max_length=255)
    url=models.CharField(max_length=255)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)




