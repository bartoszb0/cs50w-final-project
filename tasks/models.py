from django.contrib.auth.models import AbstractUser
from django.db import models

ROLE_CHOICES = [('admin', 'Admin'), ('staff', 'Staff')]

PRIORITY_CHOICES = [(1, 'Low'), (2, 'Medium'), (3, 'High')]

STATUS_CHOICES = [('to be done', 'To be done'), ('in progress', 'In progress'), ('done', 'Done')]

# Create your models here.
class User(AbstractUser):
    role = models.CharField(max_length=5 ,choices=ROLE_CHOICES, default='staff')
    company = models.CharField(max_length=32, blank=True)
    boss = models.ManyToManyField("self", blank=True, symmetrical=False, related_name="boss_of_user")

class Task(models.Model):
    name = models.CharField(max_length=32)
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tasks_assigned_to")
    deadline = models.DateField()
    description = models.TextField(blank=True)
    assigned_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tasks_assigned_by")
    priority = models.IntegerField(choices=PRIORITY_CHOICES)
    status = models.CharField(max_length=11, choices=STATUS_CHOICES, default='to be done')