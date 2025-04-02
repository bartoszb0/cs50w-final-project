from django.forms import ModelForm
from django import forms
from .models import Task

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
            "deadline": forms.DateInput(attrs={"type": "date"}),
        }