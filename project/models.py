from django.contrib.auth.models import Permission, User
from django.db import models

# Create your models here.
class Project(models.Model):

    user = models.ForeignKey(User, default = 1, related_name = 'user', on_delete=models.SET_DEFAULT)
    name = models.CharField(max_length=150)
    situation = models.CharField(max_length=50)

    def __str__(self):
        return self.name +' - '+ self.situation

class Application(models.Model):

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='project')
    name = models.CharField(max_length=150)
    access = models.CharField(max_length=100)
    username = models.CharField(max_length=50)
    notes = models.TextField(max_length=1000)

    def __str__(self):
        return self.name + ' - ' + self.access + ' - ' + self.username + ' - ' + self.notes