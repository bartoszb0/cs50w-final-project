from django.contrib import messages
from django.core.validators import validate_email
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from django.http import HttpResponseRedirect
from django.urls import reverse
from functools import wraps

from .models import User

def create_new_user(request, username, email, password, confirmation, role="Staff"):
        # Check whether the data was inputted correctly
        if not username or not email or not password or not confirmation:
            messages.warning(request, "All fields are required.")
            return False
        
        # Check for the same password
        if password != confirmation:
            messages.warning(request, "Passwords must match.")
            return False
        
        # Validate email
        try:
            validate_email(email)
        except ValidationError:
            messages.warning(request, "Invalid email address format.")
            return False

        # Attempt to create new user
        try:
            if role == "Admin":
                user = User.objects.create_user(username, email, password, role='Admin')
            elif role == "Staff":
                user = User.objects.create_user(username = username, email = email, password = password)
                user.boss.set([request.user])
                user.save()
        except IntegrityError:
            messages.warning(request, "Username already taken")
            return False
        
        return True


# Decorator
def admin_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.user.role != "Admin":
            return HttpResponseRedirect(reverse('index'))
        return view_func(request, *args, **kwargs)
    return wrapper
