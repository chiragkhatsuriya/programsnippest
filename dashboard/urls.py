from django.conf.urls import url

from dashboard import views

app_name="dashboard"
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^pages/add', views.add_page, name='add_page'),
    url(r'pages/edit/(?P<page_id>[0-9]+)/$', views.edit_page, name='edit_page'),
    url(r'pages/delete/(?P<page_id>[0-9]+)/$', views.delete_page, name='delete_page'),
url(r'pages/deleted', views.deleted_pages, name='deleted_pages'),
    url(r'^pages', views.list_pages, name='pages'),
    url(r'^tags/add', views.add_tag, name='add_tag'),
    url(r'tags/delete/(?P<tag_id>[0-9]+)/$', views.delete_tag, name='delete_tag'),
    url(r'tags/toggle_visibility/(?P<tag_id>[0-9]+)/$', views.tag_toggle_visibility, name='tag_toggle_visibility'),
    url(r'tags/assign_templates', views.assign_templates, name='assign_templates'),
url(r'tags/unassign_templates/(?P<tag_id>[0-9]+)/(?P<template_id>[0-9]+)/', views.unassign_templates, name='unassign_templates'),
    url(r'^tags', views.list_tags, name='tags'),



 ]
