from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'status', 'priority', 'deadline', 'assigned_to']

class TaskFilterForm(forms.Form):
    status = forms.ChoiceField(choices=Task.STATUS_CHOICES, required=False)
    priority = forms.ChoiceField(choices=Task.PRIORITY_CHOICES, required=False)