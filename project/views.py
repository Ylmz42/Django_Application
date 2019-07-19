from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.shortcuts import render, get_object_or_404
from .forms import ProjectForm, ApplicationForm, UserForm
from .models import Project, Application

# Create your views here.

def index(request):#Returns all applications and project names.
    apps = Application.objects.all()
    my_dict = Project.objects.all()
    return render(request, 'project/index.html',{'apps':apps, 'my_dict':my_dict})


def register(request):
    form = UserForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user.set_password(password)
        user.save()
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return index(request)
    context = {
        "form": form,
    }
    return render(request, 'project/register.html', context)

def login_user(request):
    if request.user.is_authenticated:
        return render(request, 'project/index.html')
    else:
        if request.method == "POST":
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return index(request)
                else:
                    return render(request, 'project/login.html', {'error_message': 'Your account has been disabled'})
            else:
                return render(request, 'project/login.html', {'error_message': 'Invalid login'})
        return render(request, 'project/login.html')

def logout_user(request):
    logout(request)
    form = UserForm(request.POST or None)
    context = {
        "form": form,
    }
    return render(request, 'project/login.html', context)

def detail(request, project_id):
    if not request.user.is_authenticated:
        return render(request, 'project/login.html')
    else:
        user = request.user
        project = get_object_or_404(Project, pk=project_id)
        return render(request, 'project/detail.html', {'project': project, 'user': user})
    # project = get_object_or_404(Project.objects.all(), pk=project_id)#Returns project object if it is exist. If ıt's not returns 404 page.
    # return render(request, 'project/detail.html',  {'project': project})

def create_project(request):
    if not request.user.is_authenticated:
        return render(request, 'project/login.html')
    else:
        form = ProjectForm(request.POST or None)
        if form.is_valid():
            project = form.save(commit=False)
            project.user = request.user

            project.save()
            return render(request, 'project/detail.html', {'project': project})
        context = {
            "form": form,
        }
    return render(request, 'project/create_project.html', context)

def delete_project(request, project_id):
    project = Project.objects.get(pk=project_id)
    project.delete()
    projects = Project.objects.filter(user=request.user)
    return render(request, 'project/index.html', {'projects': projects})

def create_application(request, project_id):
    form = ApplicationForm(request.POST or None)
    project = get_object_or_404(Project, pk=project_id)
    if form.is_valid():
        projects_applications = project.song_set.all()
        for a in projects_applications:
            if projects_applications.application_name == form.cleaned_data.get("application_name"):
                context = {
                    'project': project,
                    'form': form,
                    'error_message': 'You already added that application',
                }
                return render(request, 'project/create_application.html', context)
        application = form.save(commit=False)
        application.project = project

        application.save()
        return render(request, 'project/detail.html', {'project': project})
    context = {
        'project': project,
        'form': form,
    }
    return render(request, 'project/create_application.html', context)

def delete_application(request, project_id, application_id):
    project = get_object_or_404(Project, pk=project_id)
    application = Application.objects.get(pk=application_id)
    application.delete()
    return render(request, 'project/detail.html', {'project': project})
