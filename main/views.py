from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.http import JsonResponse
from django.views.decorators.http import require_GET

from .forms import LoginForm, RegisterForm, TaskForm, TaskEditForm, ProjectForm
from django.shortcuts import render, redirect, get_object_or_404
from .models import Unit, Status, Task, Role, Project

User = get_user_model()


def main(request):
    if not request.user.is_authenticated:
        return redirect('authorization/login')

    tasks_done = Task.objects.filter(status__name='Done')
    tasks_untouched = Task.objects.filter(status__name='Untouched')
    tasks_in_progress = Task.objects.filter(status__name='In Progress')
    projects = Project.objects.all()

    return render(request, "main.html", {
        'tasks_done': tasks_done,
        'tasks_untouched': tasks_untouched,
        'tasks_in_progress': tasks_in_progress,
        'projects': projects,
    })


# @login_required
# def logout_view(request):
#     if request.method == 'POST':
#         logout(request)
#         messages.success(request, "You have been logged out successfully.")
#         return redirect('main')
#     return render(request, 'logout.html')


@require_GET
def get_units_by_project(request):
    project_id = request.GET.get('project_id')
    if project_id:
        try:
            project = Project.objects.get(pk=project_id)
            units = project.unit.all().values('id', 'first_name', 'second_name')
            units_list = [
                {'id': u['id'], 'name': f"{u['first_name']} {u['second_name']}"}
                for u in units
            ]
            return JsonResponse({'units': units_list})
        except Project.DoesNotExist:
            return JsonResponse({'units': []})
    return JsonResponse({'units': []})


@login_required
def create_project(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('main')
    else:
        form = ProjectForm()
    return render(request, 'create_project.html', {'form': form})


@login_required
def update_project(request, pk):
    project = get_object_or_404(Project, pk=pk)

    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            return redirect('main')
    else:
        form = ProjectForm(instance=project)

    return render(request, 'update_project.html', {'form': form, 'project': project})


@login_required
def add_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.save()
            unit_ids = request.POST.getlist('unit')
            task.unit.set(unit_ids)
            return redirect('main')
    else:
        form = TaskForm()
    return render(request, 'create_task.html', {'form': form})


@login_required
def edit_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if request.method == 'POST':
        form = TaskEditForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('main')
    else:
        form = TaskEditForm(instance=task)
    return render(request, 'edit_task.html', {'form': form, 'task': task})


#########################################################################################################


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('main')
            else:
                form.add_error(None, 'Invalid username or password')
    else:
        form = LoginForm()

    return render(request, 'authorization/login.html', {'form': form})


def registration_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            Unit.objects.create(
                first_name=user.first_name,
                second_name=user.last_name,
                role=None
            )
            user = authenticate(username=user.username, password=form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                return redirect('main')
            else:
                form.add_error(None, "Не вдалося авторизувати користувача після реєстрації")
    else:
        form = RegisterForm()

    return render(request, 'authorization/registration.html', {'form': form})
