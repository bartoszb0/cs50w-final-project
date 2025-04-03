from django.forms import ModelForm
from django import forms
from .models import Task, User

class TaskForm(ModelForm):
    class Meta:
        model = Task
        fields = [
            "name",
            "description",
            "deadline",
            "priority",
            "assigned_to",
        ]
        
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "Enter name"}),
            "description": forms.Textarea(attrs={"placeholder": "Enter description"}),
            "deadline": forms.DateInput(attrs={"type": "date"}),
        }