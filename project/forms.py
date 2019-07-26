from django import forms
from django.contrib.auth.models import User

from .models import Project, Application


class ProjectForm(forms.ModelForm):

    class Meta:
        model = Project
        fields = ['user', 'name', 'situation']


class ApplicationForm(forms.ModelForm):

    class Meta:
        model = Application
        fields = ['project', 'name', 'access', 'username', 'notes']


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']