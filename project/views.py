from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .forms import ProjectForm, ApplicationForm, UserForm
from .models import Project, Application, CheckList
import sqlite3
# Create your views here.

# This is home page. When user logs in, the page that will be seen


def index(request):
    if not request.user.is_authenticated:  # Does user log in?
        return render(request, 'project/login.html')
    else:
        projects = Project.objects.all()  # Getter all projects
        applications = Application.objects.all()  # Getter all applications

        query = request.GET.get("q")  # Search project

        if query:
            projects = projects.filter(
                Q(name__icontains=query)
            ).distinct()

            return render(request, 'project/index.html', {'projects': projects, 'applications': applications})
        else:
            return render(request, 'project/index.html', {'projects': projects, 'applications': applications})

# This is projects page


def projects(request):
    if not request.user.is_authenticated:  # Does user log in?
        return render(request, 'project/login.html')
    else:
        projects = Project.objects.all()  # Getter all projects
        return render(request, 'project/projects.html', {'projects': projects})

# This is applications page


def applications(request):
    if not request.user.is_authenticated:  # Does user log in?
        return render(request, 'project/login.html')
    else:
        projects = Project.objects.all()  # Getter all projects
        # Getter all applications that related with users who logged in
        applications = Application.usernameInApp(request)
        return render(request, 'project/applications.html', {'projects': projects, 'applications': applications})

# This is register page


def register(request):
    form = UserForm(request.POST or None)
    if form.is_valid():  # Is there register form?
        user = form.save(commit=False)
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user.set_password(password)  # User's password is set
        user.save()  # User's password is saved database
        # User logs in home page
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                projects = Project.objects.all()
                applications = Application.objects.all()
                return render(request, 'project/index.html', {'projects': projects, 'applications': applications})
    context = {
        "form": form,
    }
    return render(request, 'project/register.html', context)

# This is log in page


def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                request.session.set_expiry(300)  # 5 minutes expire session
                projects = Project.objects.all()
                applications = Application.objects.all()
                return render(request, 'project/index.html', {'projects': projects, 'applications': applications})
            else:
                return render(request, 'project/login.html', {'error_message': 'Your account has been disabled'})
        else:
            return render(request, 'project/login.html', {'error_message': 'Invalid login'})
    return render(request, 'project/login.html')

#This is log out


def logout_user(request):
    logout(request)
    form = UserForm(request.POST or None)
    context = {
        "form": form,
    }
    return render(request, 'project/login.html', context)

# This is project_detail page
# project_id is the project unique id


def project_detail(request, project_id):
    if not request.user.is_authenticated:  # Does user log in?
        return render(request, 'project/login.html')
    else:
        project = get_object_or_404(Project, pk=project_id)
        applications = Application.objects.all().filter(project_id=project.id)

        return render(request, 'project/project_detail.html', {'project': project, 'applications': applications})

# This is applications_detail page
# project_id is the project unique id
# application_id is the application unique id
def application_detail(request, project_id, application_id):
    if not request.user.is_authenticated: # Does user log in?
        return render(request, 'project/login.html')
    else:
        project = get_object_or_404(Project, pk=project_id)
        application = get_object_or_404(Application, pk=application_id)
        checklists = CheckList.objects.all()

        checkboxLength = len(list(application.checklist))
        table = []

        for i in range(checkboxLength):
            table.append([list(checklists)[i], list(application.checklist)[i]])

        return render(request, 'project/application_detail.html', {'project': project, 'application': application, 'checklists': checklists, 'checkboxLength': checkboxLength, 'table': table})

#This is for user to see selected project applications and checkboxes together.


def checklist_detail(request, project_id):
    if not request.user.is_authenticated:
        return render(request, 'project/login.html')
    else:
        project = get_object_or_404(Project, pk=project_id)
        applications = Application.objects.filter(project_id=project.id)
        checklists = CheckList.objects.all()

        applicationLength = len(list(applications))
        table = []

        for i in range(applicationLength):
            checkboxLength = len(list(applications[i].checklist))
            for j in range(checkboxLength):
                table.append([list(checklists)[j], list(
                    applications[i].checklist)[j]])

        return render(request, 'project/checklist_detail.html', {'project': project, 'applications': applications, 'checklists': checklists, 'table': table})

#This is for creating projects.


def create_project(request):
    if not request.user.is_authenticated:
        return render(request, 'project/login.html')
    else:
        form = ProjectForm(request.POST or None)
        if form.is_valid():
            project = form.save(commit=False)
            project.user = request.user
            project.save()
            return render(request, 'project/project_detail.html', {'project': project})
        context = {
            "form": form,
        }
    return render(request, 'project/create_project.html', context)

#This is for deleting projects.


def delete_project(request, project_id):
    if not request.user.is_authenticated:
        return render(request, 'project/login.html')
    else:
        project = get_object_or_404(Project, pk=project_id)
        project.delete()
        return render(request, 'project/index.html')

#This is for creating application.


def create_application(request, project_id):
    if not request.user.is_authenticated:
        return render(request, 'project/login.html')
    else:
        form = ApplicationForm(request.POST or None)
        project = get_object_or_404(Project, pk=project_id)
        if form.is_valid():
            applications = Application.objects.all()
            for apps in applications:
                if apps.name == form.cleaned_data.get("name"):
                    context = {
                        'project': project,
                        'form': form,
                        'error_message': 'You already added that application',
                    }
                    return render(request, 'project/create_application.html', context)
            application = form.save(commit=False)
            # User can only create projects that project's user is itself.
            application.project = project
            c = CheckList.objects.all()
            cstr = ''
            for a in c:
                cstr = cstr+'0'
            application.checklist = cstr
            application.reported = cstr
            application.save()
            return render(request, 'project/project_detail.html', {'project': project})
        context = {
            'project': project,
            'form': form,
        }
        return render(request, 'project/create_application.html', context)

#This is for deleting application.


def delete_application(request, project_id, application_id):
    project = get_object_or_404(Project, pk=project_id)
    application = Application.objects.get(pk=application_id)
    application.delete()
    return render(request, 'project/project_detail.html', {'project': project})

#This is for updating database when any of checkbox has changed.

def checkbox_check(request, application_id):

    if request.method == 'POST':
        checklist = request.POST['checklist']

        application = get_object_or_404(Application, pk=application_id)
        application.checklist = checklist

        print(checklist)
        
        conn = sqlite3.connect('db.sqlite3')
        c = conn.cursor()
        c.execute("UPDATE project_application SET checklist = ? WHERE id = ?", (checklist, application_id))
        conn.commit()
        c.close()
        conn.close()
        
        return HttpResponse('')
