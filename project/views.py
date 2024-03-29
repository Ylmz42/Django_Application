from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .forms import ProjectForm, ApplicationForm, UserForm
from .models import Project, Application, CheckList
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
        # BURAYA KULLANICININ YETKİLİ OLDUĞU PROJELER GELECEK.
        projects = Project.objects.all()  # Getter all projects
        return render(request, 'project/projects.html', {'projects': projects})

# This is applications page


def applications(request):
    if not request.user.is_authenticated:  # Does user log in?
        return render(request, 'project/login.html')
    else:
        projects = Project.objects.all()  # Getter all projects
        applications = Application.objects.all()
        # Getter all applications that related with users who logged in
        # BURAYA KULLANICIN YETKİLİ OLDUĞU PROJELER VE UYGULAMALAR LİSTESİ GELECEK.
        #applications = Application.usernameInApp(request)
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
                #request.session.set_expiry(300)  # 5 minutes expire session
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

# BURAYI SADECE PROJEDEKI YETKILI KISILER GOREBILECEK


def project_detail(request, project_id):
    if not request.user.is_authenticated:  # Does user log in?
        return render(request, 'project/login.html')
    else:
        #BURAYA KULLANICININ YETKİLİ OLDUĞU UYGULAMALAR GELECEK.
        project = get_object_or_404(Project, pk=project_id)
        applications = Application.objects.filter(project_id=project.id)

        return render(request, 'project/project_detail.html', {'project': project, 'applications': applications})

# This is applications_detail page
# project_id is the project unique id
# application_id is the application unique id

# BURAYI SADECE UYGULAMAYA YETKILI KISILER GOREBILECEK


def application_detail(request, project_id, application_id):
    if not request.user.is_authenticated:  # Does user log in?
        return render(request, 'project/login.html')
    else:
        project = get_object_or_404(Project, pk=project_id)
        application = get_object_or_404(Application, pk=application_id)
        checklists = CheckList.objects.all()

        checkboxLength = len(checklists)
        table = []

        for i in range(checkboxLength):
            table.append([list(checklists)[i], list(application.checklist)[i]])

        return render(request, 'project/application_detail.html', {'project': project, 'application': application, 'table': table})

#This is for user to see selected project applications and checkboxes together.

# BURAYI PROJEYE YETKILI KISILER GOREBILECEK VE PROJEDE YETKILI OLDUGU UYGULAMALAR GOSTERILECEK


def report(request, project_id):
    if not request.user.is_authenticated:
        return render(request, 'project/login.html')
    else:
        project = get_object_or_404(Project, pk=project_id)
        applications = Application.objects.filter(project_id=project.id)
        checklists = CheckList.objects.all()

        return render(request, 'project/report.html', {'project': project, 'applications': applications, 'checklists': checklists})

#This is for creating projects.


def create_project(request):
    if not request.user.is_authenticated:
        return render(request, 'project/login.html')
    else:
        if request.user.is_superuser:
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
        else:
            projects = Project.objects.all()
            applications = Application.objects.all()

            return render(request, 'project/index.html', {'projects': projects, 'applications': applications})

#This is for deleting projects.


def delete_project(request, project_id):
    if not request.user.is_authenticated:
        return render(request, 'project/login.html')
    else:
        projects = Project.objects.all()
        applications = Application.objects.all()

        if request.user.is_superuser:
            project = get_object_or_404(Project, pk=project_id)
            project.delete()

            return render(request, 'project/index.html', {'projects': projects, 'applications': applications})
        else:
            return render(request, 'project/index.html', {'projects': projects, 'applications': applications})

#This is for creating application.


def create_application(request, project_id):
    if not request.user.is_authenticated:
        return render(request, 'project/login.html')
    else:
        if request.user.is_superuser:
            form = ApplicationForm(request.POST or None)
            project = get_object_or_404(Project, pk=project_id)
            if form.is_valid():
                Applications = Application.objects.all()
                for apps in Applications:
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

                checklists = CheckList.objects.all()
                checklist = ''

                for check in checklists:
                    checklist = checklist+'0'

                application.checklist = checklist
                application.reported = checklist
                application.save()

                applications = Application.objects.filter(
                    project_id=project.id)

                return render(request, 'project/project_detail.html', {'project': project, 'applications': applications})
            context = {
                'project': project,
                'form': form,
            }
            return render(request, 'project/create_application.html', context)
        else:
            projects = Project.objects.all()
            applications = Application.objects.all()

            return render(request, 'project/index.html', {'projects': projects, 'applications': applications})

#This is for deleting application.


def delete_application(request, project_id, application_id):
    if not request.user.is_authenticated:
        return render(request, 'project/login.html')
    else:
        if request.user.is_superuser:
            project = get_object_or_404(Project, pk=project_id)
            application = Application.objects.get(pk=application_id)
            application.delete()

            applications = Application.objects.filter(project_id=project.id)
            return render(request, 'project/project_detail.html', {'project': project, 'applications': applications})
        else:
            projects = Project.objects.all()
            applications = Application.objects.all()

            return render(request, 'project/index.html', {'projects': projects, 'applications': applications})
#This is for updating database when any of checkbox has changed.


def setChecklist(request):
    if not request.user.is_authenticated:
        return render(request, 'project/login.html')
    else:
        checklist = request.POST['checklist']
        application_id = request.POST['application_id']

        Application.objects.filter(id=application_id).update(checklist=checklist)

        return HttpResponse('')


def getChecklist(request):
    if not request.user.is_authenticated:
        return render(request, 'project/login.html')
    else:
        application_id = request.GET.get("application_id")
        application = Application.objects.filter(id=application_id)
        check = ""

        for app in application:
            check += app.checklist

        data = {
            'check': check,
        }

        return JsonResponse(data)


def setReportlist(request):
    if not request.user.is_authenticated:
        return render(request, 'project/login.html')
    else:
        reportlist = request.POST['reportlist']
        project_id = request.POST['project_id']

        applications = Application.objects.filter(project_id=project_id)
        checklists = CheckList.objects.all()

        reported = []

        for i in range(len(applications)):
            report = ""
            for j in range(len(checklists)):
                report += reportlist[i + (len(applications) * j)]
            reported.append(report)

        count = 0
        for app in applications:
            Application.objects.filter(id=app.id).update(reported=reported[count])
            count += 1

        return HttpResponse('')


def getReportlist(request):
    if not request.user.is_authenticated:
        return render(request, 'project/login.html')
    else:
        project_id = request.GET.get("project_id")
        applications = Application.objects.filter(project_id=project_id)
        checklists = CheckList.objects.all()

        report = ""
        application_id = []
        appLength = len(applications)
        checklistLength = len(checklists)

        for app in applications:
            report += app.reported
            application_id.append(app.id)

        data = {
            'report': report,
            'appLength': appLength,
            'checklistLength': checklistLength,
            'application_id': application_id,
        }

        return JsonResponse(data)