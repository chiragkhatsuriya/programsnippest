from django.conf.urls import url

from public import views

app_name="public"


urlpatterns = [
    url(r'^$', views.index, name='index'),



]