from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render

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
def index(request):
    if request.user.role != "Admin":
        return render(request, "tasks/index.html", {
            "username": request.user.username
        })
    else:
        return render(request, "tasks/admin_panel.html", {
            "task_form": TaskForm,
            "tasks": Task.objects.filter(assigned_by=request.user).exclude(status="Done").order_by("deadline"),
            "stats_finished": Task.objects.filter(assigned_by=request.user, status="Done").count(),
            "stats_tbd": Task.objects.filter(assigned_by=request.user, status="To be done").count(),
        })
    

@login_required
@admin_required # think about this? maybe use this for user to give himself a task as well
def add_assign_task(request):
    if request.method == "POST":
        form = TaskForm(request.POST)
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
def show_task(request, id): #TODO - maybe delete this and use modal instead
    task = Task.objects.get(id=id)
    if task.assigned_to == request.user or task.assigned_by == request.user:
        messages.success(request, "Authorized")
        return HttpResponseRedirect(reverse('index'))
    else:
        messages.warning(request, "Unauthorized")
        return HttpResponseRedirect(reverse('index'))


@login_required # TODO make this available only for admin xd
@admin_required
def new_user(request):
    if request.method == "POST" and request.user.role == "Admin":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]

        print(request.POST)

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

    else:
        users = User.objects.filter(boss=request.user)
        return render(request, "tasks/new_user.html", {
            "users": users
        })