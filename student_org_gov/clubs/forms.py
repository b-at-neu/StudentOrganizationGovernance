import json

from django import forms
from django.contrib.staticfiles import finders

from clubs.models.club import Club
from users.models import RoleUser

class CreateClubForm(forms.Form):
    full_name = forms.CharField(max_length=200, required=True)
    abbreviation = forms.CharField(max_length=50, required=True, help_text="A short-form name for your organization which you will use throughout the constitution.")