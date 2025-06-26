from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model


class CustomerSignupForm(UserCreationForm):
    name = forms.CharField(max_length=100)
    domain = forms.CharField(max_length=255, required=False)
    schema_name = forms.CharField(max_length=63, required=False)

    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = UserCreationForm.Meta.fields + ("name", "domain", "schema_name")
