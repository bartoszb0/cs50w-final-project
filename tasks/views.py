from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render

from .forms import TaskForm

from .models import User

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
            return render(request, "tasks/login.html", {
                "message": "Invalid username and/or password."
            })
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
            return render(request, "tasks/register.html", {
                "message": "All fields are required.",
            })

        if password != confirmation:
            return render(request, "tasks/register.html", {
                "message": "Passwords must match.",
            })

        # Validate email
        try:
            validate_email(email)
        except ValidationError:
            return render(request, "tasks/register.html", {
                "message": "Invalid email address format.",
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password, role='admin')
            user.save()
            if company != "":
                user.company = company
                user.save()
        except IntegrityError:
            return render(request, "tasks/register.html", {
                "message": "Username already taken.",
            })
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
    if request.user.role != "admin":
        return render(request, "tasks/index.html", {
            "username": request.user.username
        })
    else:
        return render(request, "tasks/admin_panel.html", {
            "task_form": TaskForm
        })