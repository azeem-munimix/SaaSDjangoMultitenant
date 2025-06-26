from django import forms
from .models import Service, Task, Client, FoiaRequest, Membership


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


class FoiaRequestForm(forms.ModelForm):
    class Meta:
        model = FoiaRequest
        fields = ["description"]


class FoiaAssignForm(forms.Form):
    assignee = forms.ModelChoiceField(queryset=Membership.objects.none())

    def __init__(self, *args, **kwargs):
        tenant = kwargs.pop("tenant")
        super().__init__(*args, **kwargs)
        self.fields["assignee"].queryset = Membership.objects.filter(
            tenant=tenant, role=Membership.STAFF
        ).select_related("user")
