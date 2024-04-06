from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from . import models


class SignUpForm(UserCreationForm):
    class Meta:
        model = models.RoleUser
        fields = ("username", "email")


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
