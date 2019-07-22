from django.contrib.auth.models import Permission, User
from django.db import models

# Create your models here.
class Project(models.Model):

    user = models.ManyToManyField(User, related_name='users')
    project_name = models.CharField(max_length=250)
    project_situation = models.CharField(max_length=50)

    def __str__(self):
        return self.project_name +' - '+ self.project_situation

class Application(models.Model):

    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    application_name = models.CharField(max_length=250)
    application_access = models.CharField(max_length=50)
    application_notes = models.CharField(max_length=1000)

    def __str__(self):
        return self.application_name + ' - ' + self. application_access + ' - ' + self.application_notes
