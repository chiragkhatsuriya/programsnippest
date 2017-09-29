from django.conf.urls import url

from users import views

app_name="users"

urlpatterns=[
    url(r'^$', views.index, name='index'),
    url(r'add', views.add, name='add_user'),
    url(r'edit/(?P<user_id>[0-9]+)/$', views.edit, name='edit_user'),
    url(r'profile/edit', views.edit_profile, name='edit_profile'),
    url(r'password/change/(?P<user_id>[0-9]+)/$', views.edit_user_password, name='edit_user_password'),
url(r'password/change', views.edit_password, name='edit_password'),



]