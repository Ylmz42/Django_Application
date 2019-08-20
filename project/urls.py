from django.conf.urls import url
from . import views

app_name = 'project'

urlpatterns = [

    url(r'^$', views.index, name='index'),
    url(r'^projects/$', views.projects, name='projects'),
    url(r'^applications/$', views.applications, name='applications'),
    url(r'^register/$', views.register, name='register'),
    url(r'^login_user/$', views.login_user, name='login_user'),
    url(r'^logout_user/$', views.logout_user, name='logout_user'),
    url(r'^(?P<project_id>[0-9]+)/$',views.project_detail, name='project_detail'),
    url(r'^(?P<project_id>[0-9]+)/application_detail/(?P<application_id>[0-9]+)/$',views.application_detail, name='application_detail'),
    url(r'^(?P<project_id>[0-9]+)/report/$',views.report, name='report'),
    url(r'^create_project/$', views.create_project, name='create_project'),
    url(r'^(?P<project_id>[0-9]+)/delete_project/$',views.delete_project, name='delete_project'),
    url(r'^(?P<project_id>[0-9]+)/create_application/$',views.create_application, name='create_application'),
    url(r'^(?P<project_id>[0-9]+)/delete_application/(?P<application_id>[0-9]+)/$',views.delete_application, name='delete_application'),
    url(r'^setChecklist/$', views.setChecklist, name='setChecklist'),
    url(r'^getChecklist/$', views.getChecklist, name='getChecklist'),
    url(r'^setReportlist/$', views.setReportlist, name='setReportlist'),
    url(r'^getReportlist/$', views.getReportlist, name='getReportlist'),
]