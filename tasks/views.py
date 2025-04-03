import random
import string
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.core.mail import send_mail
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render

from .forms import TaskForm

from .models import User, Task

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
        company = request.POST["company"]
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]

        # Check whether the data was inputted correctly
        if not username or not email or not password or not confirmation:
            messages.warning(request, "All fields are required.")
            return render(request, "tasks/register.html")

        if password != confirmation:
            messages.warning(request, "Passwords must match.")
            return render(request, "tasks/register.html")

        # Validate email
        try:
            validate_email(email)
        except ValidationError:
            messages.warning(request, "Invalid email address format.")
            return render(request, "tasks/register.html")

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password, role='Admin')
            user.save()
            if company != "":
                user.company = company
                user.save()
        except IntegrityError:
            messages.warning(request, "Username already taken")
            return render(request, "tasks/register.html")
        
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
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
def add_assign_task(request):
    if request.method == "POST" and request.user.role == "Admin":
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


@login_required
def new_user(request):
    if request.method == "POST" and request.user.role == "Admin":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]

        if not username or not email or not password or not confirmation:
            messages.warning(request, "All fields are required.")
            return render(request, "tasks/register.html")

        try:
            validate_email(email)
        except ValidationError:
            messages.warning(request, "Incorrect email")
            return HttpResponseRedirect(reverse('new_user'))
        
        if password != confirmation:
            messages.warning(request, "Passwords must match.")
            return HttpResponseRedirect(reverse('new_user'))
        
        new_user = User.objects.create_user(
            username = username,
            email = email,
            password = password,
        )
        new_user.boss.set([request.user])

        messages.success(request, "User created.")
        return HttpResponseRedirect(reverse('new_user'))
    else:
        users = User.objects.filter(boss=request.user)
        return render(request, "tasks/new_user.html", {
            "users": users
        })