from django import forms
from .models import Service, Task, Client


class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ["name", "description"]


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["name", "service", "completed"]


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ["name", "email"]
