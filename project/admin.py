from django.contrib import admin
from .models import Project, Application, CheckList
# Register your models here.

admin.site.register(Project)
admin.site.register(Application)
admin.site.register(CheckList)