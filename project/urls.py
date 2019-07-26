from django.conf.urls import url
from . import views

app_name = 'project'

urlpatterns = [

    url(r'^$', views.index, name='index'),
    url(r'^register/$', views.register, name='register'),
    url(r'^login_user/$', views.login_user, name='login_user'),
    url(r'^logout_user/$', views.logout_user, name='logout_user'),
    url(r'^(?P<project_id>[0-9]+)/$', views.detail, name='detail'),
    url(r'^create_project/$', views.create_project, name='create_project'),
    url(r'^(?P<project_id>[0-9]+)/delete_project/$',views.delete_project, name='delete_project'),
    url(r'^(?P<project_id>[0-9]+)/create_application/$',views.create_application, name='create_application'),
    url(r'^(?P<project_id>[0-9]+)/delete_application/(?P<application_id>[0-9]+)/$',views.delete_application, name='delete_application'),
]