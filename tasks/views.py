import json
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.urls import reverse
from django.shortcuts import render, redirect

from .forms import TaskForm

from .models import User, Task

from .helpers import create_new_user, admin_required

# Create your views here.
def login_view(request):
    if request.method == "POST":
        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            messages.warning(request, "Invalid username and/or password.")
            return render(request, "tasks/login.html")
    else:
        return render(request, "tasks/login.html")
    

def register_admin_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]

        if not create_new_user(
            request,
            username = username,
            email = email,
            password = password,
            confirmation = confirmation,
            role = "Admin"
        ):
            return HttpResponseRedirect(reverse("register"))
        else:
            messages.success(request, "Admin account created. Log in")
            return HttpResponseRedirect(reverse("register"))
    else:
        return render(request, "tasks/register.html")


@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("login"))

@login_required
def change_password(request):
    if request.method == "POST":
        old_password = request.POST["old_password"]
        new_password = request.POST["new_password"]
        confirmation = request.POST["confirmation"]
        
        if not old_password or not new_password or not confirmation:
            messages.warning(request, "All fields are required.")
            return HttpResponseRedirect(reverse("change_password"))
        
        user = request.user

        if user.check_password(old_password):
            if new_password == confirmation:
                user.set_password(new_password)
                user.save()
                update_session_auth_hash(request, user)
                messages.success(request, "Password changed succesfully")
                return HttpResponseRedirect(reverse("change_password"))
            else:
                messages.warning(request, "Passwords are not the same")
                return HttpResponseRedirect(reverse("change_password"))
        else:
            messages.warning(request, "Current password is incorrect")
            return HttpResponseRedirect(reverse("change_password"))

    else:
        return render(request, "tasks/change_password.html")


@login_required
def index(request):
    if request.user.role != "Admin":
        return HttpResponseRedirect(reverse('index_user', args=[request.user.username]))
    else:
        return render(request, "tasks/admin_panel.html", {
            "task_form": TaskForm(user=request.user),
            "unfinished_tasks": Task.objects.filter(assigned_by=request.user).exclude(status="Done").order_by("deadline"),
            "finished_tasks": Task.objects.filter(assigned_by=request.user).exclude(status="To be done").order_by("deadline"),
            "stats_finished": Task.objects.filter(assigned_by=request.user, status="Done").count(),
            "stats_tbd": Task.objects.filter(assigned_by=request.user, status="To be done").count(),
        })

@login_required
def index_user(request, username):
    user = User.objects.get(username=username)
    boss = user.boss.all()
    # Only user and his boss have access to his tasks
    if request.user in boss or request.user == user:
        return render(request, "tasks/user.html", {
            "user": user,
            "unfinished_tasks": Task.objects.filter(assigned_to=user).exclude(status="Done").order_by("deadline"),
            "finished_tasks": Task.objects.filter(assigned_to=user).exclude(status="To be done").order_by("deadline"),
            "stats_finished": Task.objects.filter(assigned_to=user, status="Done").count(),
            "stats_tbd": Task.objects.filter(assigned_to=user, status="To be done").count(),
        })
    else:
        return HttpResponseRedirect(reverse('index_user', args=[request.user.username]))
        

@login_required
@admin_required # think about this? maybe use this for user to give himself a task as well
def add_assign_task(request):
    if request.method == "POST":
        form = TaskForm(request.POST, user=request.user)
        if form.is_valid():
            new_task = Task(
                name = form.cleaned_data["name"],
                description = form.cleaned_data["description"],
                deadline = form.cleaned_data["deadline"],
                priority = form.cleaned_data["priority"],
                assigned_to = User.objects.get(username=form.cleaned_data["assigned_to"]),
                assigned_by = request.user
            )
            new_task.save()
            messages.success(request, "Task created succesfully")
            return HttpResponseRedirect(reverse('index'))
        else:
            messages.warning(request, "Task not created, please try again")
            return HttpResponseRedirect(reverse('index'))
    else:
        return HttpResponseRedirect(reverse('index'))
    

@login_required
@admin_required
def new_user(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]

        if not create_new_user(
            request,
            username = username,
            email = email,
            password = password,
            confirmation = confirmation,
        ):
            return HttpResponseRedirect(reverse("new_user"))
        else:
            messages.success(request, "User created.")
            return HttpResponseRedirect(reverse('new_user'))
    
    elif request.method == "DELETE":
        data = json.loads(request.body)
        user = User.objects.get(id=data["user_id"])
        Task.objects.filter(assigned_to=user).all().delete()
        user.delete()

        return JsonResponse({}, status=204)

    else:
        users = User.objects.filter(boss=request.user)
        return render(request, "tasks/new_user.html", {
            "users": users,
            "unfinished_tasks": Task.objects.filter(assigned_by=request.user).exclude(status="Done").order_by("deadline"),
        })
    

# walidacja do zaznaczenia zadania jako skonczone - request.user musi byc w assigned to albo assigned by
@login_required
def marktask(request):
    if request.method == "POST":
        data = json.loads(request.body)
        task = Task.objects.get(id=data["task_id"])
        
        if task.assigned_by == request.user or task.assigned_to == request.user:
            if task.status == 'To be done':
                task.status = 'Done'
            else:
                task.status = 'To be done'
            task.save()

        return JsonResponse({}, status=201)
    else:
        return HttpResponseRedirect(reverse('index'))