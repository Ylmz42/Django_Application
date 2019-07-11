from django.conf.urls import url
from . import views

app_name = 'project'

urlpatterns = [

    url(r'^$', views.index, name='index'),
    url(r'^register/$', views.register, name='register'),
    url(r'^login_user/$', views.login_user, name='login_user'),
    url(r'^logout_user/$', views.logout_user, name='logout_user'),
    url(r'^(?P<project_id>[0-9]+)/$', views.detail, name='detail'),
]
