from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout, get_user_model
from .forms import LoginForm, RegisterForm, TaskForm, TaskEditForm
from django.shortcuts import render, redirect, get_object_or_404
from .models import Unit, Status, Task, Role

User = get_user_model()


def main(request):
    if not request.user.is_authenticated:
        return redirect('authorization/login')

    tasks_done = Task.objects.filter(status__name='Done')
    tasks_untouched = Task.objects.filter(status__name='Untouched')
    tasks_in_progress = Task.objects.filter(status__name='In Progress')

    return render(request, "main.html", {
        'tasks_done': tasks_done,
        'tasks_untouched': tasks_untouched,
        'tasks_in_progress': tasks_in_progress,
    })


# @login_required
# def logout_view(request):
#     if request.method == 'POST':
#         logout(request)
#         messages.success(request, "You have been logged out successfully.")
#         return redirect('main')
#     return render(request, 'logout.html')


@login_required
def add_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
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

