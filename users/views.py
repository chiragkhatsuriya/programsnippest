from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from users.forms import UserForm, UserProfileForm, PasswordForm
from users.models import UserProfile


@login_required
@user_passes_test(lambda u:u.is_superuser)
def index(request):
    users=User.objects.all()
    from users.filters import UserFilter
    user_filter=UserFilter(request.GET,users)
    return render(request, 'users/index.html', {'user_filter': user_filter})

@login_required
@user_passes_test(lambda u:u.is_superuser)
def edit(request,user_id):
    edit_user=User.objects.get(pk=user_id)
    try:
        edit_user_profile=UserProfile.objects.get(user=edit_user)
    except:
        edit_user_profile=UserProfile()
    if request.method == 'POST':
        user_form = UserForm(request.user,request.POST,instance=edit_user)
        user_profile_form = UserProfileForm(request.POST,instance=edit_user_profile)
        if all((user_form.is_valid(),user_profile_form.is_valid())):
            user=user_form.save()
            user_profile_form.instance.user=user
            user_profile_form.save()
            return HttpResponseRedirect(reverse("users:index"))
    else:
        user_form=UserForm(request.user,instance=edit_user)
        user_profile_form=UserProfileForm(instance=edit_user_profile)
    return render(request, 'users/edit_user.html',{'edit_user':edit_user,'user_form':user_form,'user_profile_form':user_profile_form})

@login_required
@user_passes_test(lambda u:u.is_superuser)
def add(request):

    if request.method == 'POST':
        user_form = UserForm(request.user,request.POST)
        user_profile_form = UserProfileForm(request.POST)
        if user_form.is_valid() and user_profile_form.is_valid() :
            user = user_form.save()
            user_profile = user_profile_form.save(commit=False)
            user_profile.user = user
            user_profile.save()
            user.username = user.email
            user.save()
            return HttpResponseRedirect(reverse("users:index"))

    else:
        user_form = UserForm(request.user)
        user_profile_form = UserProfileForm()
    return render(request, 'users/edit_user.html',{'user_form':user_form,'user_profile_form':user_profile_form})

@login_required
def edit_profile(request):
    if request.method == 'POST':

        user_form = UserForm(request.user,request.POST,instance=request.user)
        try:
            user_profile_form = UserProfileForm(request.POST,instance=request.user.profile)
        except:
            user_profile_form = UserProfileForm(request.POST)
        if all((user_form.is_valid(),user_profile_form.is_valid())):
            user=user_form.save()
            user_profile_form.instance.user=user
            user_profile_form.save()
            return HttpResponseRedirect(reverse("dashboard:index"))
    else:
        user_form=UserForm(request.user,instance=request.user)
        try:
            user_profile_form=UserProfileForm(instance=request.user.profile)
        except:
            user_profile_form = UserProfileForm()
    return render(request, 'users/edit_user.html',{'edit_user':request.user,'user_form':user_form,'user_profile_form':user_profile_form})

@login_required
def edit_password(request):

    if request.method == 'POST':
        password_form=PasswordForm(request.POST)
        if password_form.is_valid()  and password_form.cleaned_data['password'] == password_form.cleaned_data['confirm_password']:
            user=request.user
            user.set_password(password_form.cleaned_data['password'])
            user.save()
            return HttpResponseRedirect(reverse("dashboard:index"))
        else:
            password_form.add_error('confirm_password', 'The passwords do not match')
    else:
        password_form = PasswordForm()
    return render(request, 'users/edit_password.html',
                  {'password_form': password_form})

@login_required
@user_passes_test(lambda u:u.is_superuser)
def edit_user_password(request,user_id):
    edit_user = User.objects.get(pk=user_id)
    if request.method == 'POST':
        password_form=PasswordForm(request.POST)
        if password_form.is_valid()  and password_form.cleaned_data['password'] == password_form.cleaned_data['confirm_password']:
            edit_user.set_password(password_form.cleaned_data['password'])
            edit_user.save()
            return HttpResponseRedirect(reverse("dashboard:index"))
        else:
            password_form.add_error('confirm_password', 'The passwords do not match')
    else:
        password_form = PasswordForm()
    return render(request, 'users/edit_password.html',
                  {'password_form': password_form,"edit_user":edit_user})