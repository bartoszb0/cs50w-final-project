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

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')  # the request.user will be passed here
        super().__init__(*args, **kwargs)

        # Filter assigned_to to only show users who have this user as their boss and boss himself
        self.fields['assigned_to'].queryset = User.objects.filter(boss=user) | User.objects.filter(id=user.id)