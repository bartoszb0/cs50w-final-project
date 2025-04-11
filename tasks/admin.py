from django.contrib import admin

from .models import User, Task, Progress

# Register your models here.
admin.site.register(User)
admin.site.register(Task)
admin.site.register(Progress)