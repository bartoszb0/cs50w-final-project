from django.contrib.auth.models import AbstractUser
from django.db import models

ROLE_CHOICES = [('Admin', 'Admin'), ('Staff', 'Staff')]

PRIORITY_CHOICES = [('Low', 'Low'), ('Medium', 'Medium'), ('High', 'High')]

STATUS_CHOICES = [('To be done', 'To be done'), ('Done', 'Done')]

# Create your models here.
class User(AbstractUser):
    role = models.CharField(max_length=5 ,choices=ROLE_CHOICES, default='Staff')
    boss = models.ManyToManyField("self", blank=True, symmetrical=False, related_name="boss_of_user")

class Task(models.Model):
    name = models.CharField(max_length=32)
    description = models.TextField(blank=True)
    deadline = models.DateField()
    priority = models.CharField(max_length=6, choices=PRIORITY_CHOICES)
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tasks_assigned_to")
    assigned_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tasks_assigned_by")
    status = models.CharField(max_length=11, choices=STATUS_CHOICES, default='To be done')

    def __str__(self):
        return f"{self.name}"