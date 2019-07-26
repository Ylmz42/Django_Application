from django.contrib.auth.models import Permission, User
from django.db import models

# Create your models here.


class Project(models.Model):

    user = models.ForeignKey(User, default=1, on_delete=models.SET_DEFAULT, related_name='user')
    name = models.CharField(max_length=100)
    situation = models.CharField(max_length=10)

    def __str__(self):
        return self.name + ' - ' + self.situation


class Application(models.Model):

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='project')
    name = models.CharField(max_length=100)
    access = models.CharField(max_length=100)
    username = models.CharField(max_length=30)
    notes = models.TextField(max_length=1000)
    checklist = models.CharField(max_length=100)
    reported = models.CharField(max_length=100)

    def __str__(self):
        return self.name + ' - ' + self.access + ' - ' + self.username + ' - ' + self.notes + ' - ' + self.checklist + ' - ' + self.reported


class CheckList(models.Model):

    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name