from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import Http404
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from dashboard.filters import PageFilter, TagFilter
from dashboard.forms import  UserAssignForm, PageStrippedForm, SinglePageForm, CategoryPageForm, \
    LandingPageForm, AddPageForm, CtaForm, PageStatusForm, RedirectForm, TagForm, TemplateTagForm
from dashboard.models import Page,Keywords, Tags, Templates
from dashboard.utils import is_moderator


@login_required
def index(request):
    user_count=User.objects.all().count()
    pages_count=Page.objects.filter(deleted=0).count()
    moderation_page_count=Page.objects.filter(deleted=0,status=1).count()
    return render(request, 'dashboard/index.html',{"user_count":user_count,"pages_count":pages_count,"moderation_page_count":moderation_page_count})

@csrf_exempt
@login_required
def list_pages(request):

    if request.user.groups.filter(name__in=['content writer']):
        pages=Page.objects.filter(assigned_user=request.user,deleted=0)
    else:
        pages=Page.objects.filter(deleted=0)
    page_filter = PageFilter(request.GET, pages)
    paginator = Paginator(page_filter.qs, 10)
    try:
        page = paginator.page(request.GET.get('page'))
    except PageNotAnInteger:
        page = paginator.page(1)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)

    if request.method == 'POST' and is_moderator(request.user):
        if request.POST.get("submit") == "assign":
            id = request.POST.get("page_id")
            page=Page.objects.get(id=id)
            user_assign_form = UserAssignForm(request.POST,instance=page)
            if user_assign_form.is_valid():
                user_assign_form.save()
                return HttpResponseRedirect(reverse('dashboard:pages'))
        if request.POST.get("submit") == "status":
            id = request.POST.get("page_id")
            page = Page.objects.get(id=id)
            page_status_form=PageStatusForm(request.POST,instance=page)
            if page_status_form.is_valid():
                page_status_form.save()
                return HttpResponseRedirect(reverse('dashboard:pages'))
    else:
        user_assign_form = UserAssignForm()
        page_status_form = PageStatusForm()
    add_page_form = AddPageForm()
    return render(request, 'dashboard/pages.html',{"add_page_form":add_page_form,"page_status_form":page_status_form,"page_filter_form":page_filter,"page_filter":page,"user_assign_form":user_assign_form})

@login_required
def add_page(request):
    keywords=Keywords.objects.all()
    if request.method == 'POST':
        cta_form=CtaForm(request.POST)
        try:
            if int(request.GET.get("type")) == 0:
                page_form = SinglePageForm(request.POST,request.FILES)
                template = 'dashboard/add_single_page.html'
            elif int(request.GET.get("type")) == 1:
                template = 'dashboard/add_category_page.html'
                page_form = CategoryPageForm(request.POST,request.FILES)
            elif int(request.GET.get("type")) == 2:
                template = 'dashboard/add_landing_page.html'
                page_form = LandingPageForm(request.POST,request.FILES)

        except:
            raise Http404("Page does not exist")
        if page_form.is_valid():
            page=page_form.save()
            if request.POST.get("submit")== "moderation":
                page.status=1
                page.save();
            page.type = int(request.GET.get("type"))
            page.save()
            if request.user.groups.filter(name__in=['content writer']):
                page.assigned_user=request.user
                page.save()

            if cta_form.is_valid():
                cta=cta_form.save(commit=False)
                cta.page=page
                cta.save()
            if request.POST.getlist("keyword"):
                keywords_list=request.POST.getlist("keyword");
                insert_keywords=[]
                for keyword in keywords_list:
                    try:
                        keyword_model=Keywords.objects.get(keyword=keyword)
                        insert_keywords.append(keyword_model)
                    except:
                        keyword_model=Keywords()
                        keyword_model.keyword=keyword
                        keyword_model.save()
                        insert_keywords.append(keyword_model)
                page.keywords=insert_keywords
                page.save()

            return HttpResponseRedirect(reverse('dashboard:pages'))
    else:
        try:
            if int(request.GET.get("type"))== 0:
                template='dashboard/add_single_page.html'
                page_form = SinglePageForm()
            elif int(request.GET.get("type")) == 1:
                template = 'dashboard/add_category_page.html'
                page_form=CategoryPageForm()
            elif int(request.GET.get("type")) == 2:
                template = 'dashboard/add_landing_page.html'
                page_form=LandingPageForm()
            else:
                template = 'dashboard/add_page.html'
                page_form = AddPageForm()
        except:
            template = 'dashboard/add_page.html'
            page_form=AddPageForm()
        cta_form = CtaForm()
    return render(request, template, {"page_form":page_form,"cta_form":cta_form,"keywords":keywords})

@login_required
def edit_page(request,page_id):
    keywords = Keywords.objects.all()
    page=Page.objects.get(pk=page_id)
    selected_keywords=[]
    selected_keywords_tr=page.keywords.all()
    for keyword in selected_keywords_tr:
        selected_keywords.append(keyword.keyword)
    if request.method == 'POST':
        if page.type == 0:
            page_form = SinglePageForm(request.POST,request.FILES,instance=page)
            template = 'dashboard/add_single_page.html'
        elif page.type == 1:
            page_form = CategoryPageForm(request.POST,request.FILES,instance=page)
            template = 'dashboard/add_category_page.html'
        elif page.type == 2:
            template = 'dashboard/add_landing_page.html'
            page_form = LandingPageForm(request.POST, request.FILES,instance=page)
        try:
            cta_form = CtaForm(request.POST,instance=page.cta)
        except:
            cta_form = CtaForm(request.POST)
        if page_form.is_valid():
            page_form.save()
            if request.POST.get("submit") == "moderation":
                page.status = 1
                page.save();
            if cta_form.is_valid():
                cta = cta_form.save(commit=False)
                cta.page = page
                cta.save()
            if request.POST.getlist("keyword"):
                page.keywords.all().delete()
                keywords_list = request.POST.getlist("keyword");
                insert_keywords = []
                for keyword in keywords_list:
                    try:
                        keyword_model = Keywords.objects.get(keyword=keyword)
                        insert_keywords.append(keyword_model)
                    except:
                        keyword_model = Keywords()
                        keyword_model.keyword = keyword
                        keyword_model.save()
                        insert_keywords.append(keyword_model)
                page.keywords = insert_keywords
                page.save()
            return HttpResponseRedirect(reverse('dashboard:pages'))
    else:
        if page.type == 0:
            template = 'dashboard/add_single_page.html'
            page_form = SinglePageForm(instance=page)
        elif page.type == 1:
            template = 'dashboard/add_category_page.html'
            page_form = CategoryPageForm(instance=page)
        elif page.type == 2:
            template = 'dashboard/add_landing_page.html'
            page_form = LandingPageForm(instance=page)
        try:
            cta_form = CtaForm(instance=page.cta)
        except:
            cta_form = CtaForm(request.POST)
    return render(request, template,
                  {"page_form": page_form, "cta_form":cta_form,"keywords": keywords, "selected_keywords": selected_keywords})

@login_required
@user_passes_test(lambda u:u.is_superuser)
def delete_page(request,page_id):
    page = Page.objects.get(pk=page_id)
    page.deleted=1
    page.save()
    return HttpResponseRedirect(reverse('dashboard:pages'))

def logout_dashboard(request):
    logout(request)

@login_required
@user_passes_test(lambda u:u.is_superuser)
def deleted_pages(request) :
    if request.method == 'POST':
        id = request.POST.get("page_id")
        page = Page.objects.get(id=id)
        redirect_form=RedirectForm(request.POST,instance=page)
        if redirect_form.is_valid():
            redirect_form.save();
            return HttpResponseRedirect(reverse('dashboard:deleted_pages'))
    pages = Page.objects.filter(deleted=1)
    page_filter = PageFilter(request.GET, pages)
    paginator = Paginator(page_filter.qs, 10)
    try:
        page = paginator.page(request.GET.get('page'))
    except PageNotAnInteger:
        page = paginator.page(1)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)
    redirect_form=RedirectForm()
    return render(request, 'dashboard/deleted_pages.html',{"redirect_form":redirect_form,"page_filter_form":page_filter,"page_filter":page})

@login_required
@user_passes_test(lambda u:u.is_superuser)
def list_tags(request):
    tags=Tags.objects.all()
    tag_filter = TagFilter(request.GET, tags)
    paginator = Paginator(tag_filter.qs, 10)
    try:
        page = paginator.page(request.GET.get('page'))
    except PageNotAnInteger:
        page = paginator.page(1)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)
    tag_form = TagForm()
    template_tag_form=TemplateTagForm()
    return render(request, 'dashboard/tags.html',
                  {"tag_form": tag_form,
                   "tag_filter_form": tag_filter, "page_filter": page,"template_tag_form":template_tag_form})

@login_required
def add_tag(request):
    if request.method == 'POST':
        tag_form = TagForm(request.POST)
        if tag_form.is_valid():
            tag_form.save()
    return HttpResponseRedirect(reverse('dashboard:tags'))

@login_required
def assign_templates(request):
    if request.method == 'POST':
        template_tag_form = TemplateTagForm(request.POST)
        if template_tag_form.is_valid():
            templates=request.POST.getlist("templates")
            tag_id=request.POST.get("tag_id")
            tag=Tags.objects.get(id=tag_id)
            for template in templates:
                try:
                    template_obj=Templates.objects.get(id=template)
                    tag.templates.add(*[template])
                    template_obj.save()
                except:
                    pass

            tag.save()
    return HttpResponseRedirect(reverse('dashboard:tags'))

@login_required
def unassign_templates(request,tag_id,template_id):
    tag=Tags.objects.get(id=tag_id)
    tag.templates.remove(template_id)
    template_obj = Templates.objects.get(id=template_id)
    template_obj.save()
    return HttpResponseRedirect(reverse('dashboard:tags'))

@login_required
@user_passes_test(lambda u:u.is_superuser)
def delete_tag(request,tag_id):
    tag = Tags.objects.get(pk=tag_id)
    tag.delete()
    return HttpResponseRedirect(reverse('dashboard:tags'))

def tag_toggle_visibility(request,tag_id):
    tag = Tags.objects.get(pk=tag_id)
    if tag.show_in_homepage==1:
        tag.show_in_homepage=0
    else:
        tag.show_in_homepage=1
    tag.save()
    return HttpResponseRedirect(reverse('dashboard:tags'))


