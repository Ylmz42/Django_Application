from django import forms
from django.contrib.auth.models import User
from .models import Project, Application

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username','first_name','last_name', 'email', 'password']

class ProjectForm(forms.ModelForm):

    class Meta:
        model = Project
        fields = [
            'user',
            'project_name',
            'project_situation',
        ]

class ApplicationForm(forms.ModelForm):

    class Meta:
        model = Application
        fields = [
            'project',
            'application_name',
            'application_notes',
            'application_access',
        ]
