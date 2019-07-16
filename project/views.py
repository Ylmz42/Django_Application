from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.shortcuts import render, get_object_or_404
from .forms import UserForm
from .models import Project
from .models import Application

# Create your views here.

def index(request):
    apps = Application.objects.all()
    my_dict = []
    control=0
    for obj in apps:
        add=obj.project.project_name
        for x in my_dict:
            if add == x:
                control=1
                break
        if control == 0:
            my_dict.append(add)
        control=0
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
                projects = Project.objects.filter(user=request.user)
                return render(request, 'project/index.html', {'projects': projects})
    context = {
        "form": form,
    }
    return render(request, 'project/register.html', context)

def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                projects = Project.objects.filter(user=request.user)
                return render(request, 'project/index.html', {'projects': projects})
            else:
                return render(request, 'project/login.html')#, {'error_message': 'Your account has been disabled'})
        else:
            return render(request, 'project/login.html')#, {'error_message': 'Invalid login'})
    return render(request, 'project/login.html')

def logout_user(request):
    logout(request)
    form = UserForm(request.POST or None)
    context = {
        "form": form,
    }
    return render(request, 'project/login.html', context)

def detail(request, project_id):
    # try/Except statement
    project = get_object_or_404(Project.objects.all(), pk=project_id)
    return render(request, 'project/project_detail.html',  {'project': project})
