import json

from django import forms
from django.contrib.staticfiles import finders

from . import models
from users.models import RoleUser

class CreateClubForm(forms.ModelForm):
    class Meta:
        model = models.Club
        fields = ["full_name", "abbreviation"]

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        self.fields["purpose"] = forms.CharField(max_length=200, required=True)
        self.fields["affiliation"] = forms.CharField(max_length=200, required=True)
        self.fields["dues"] = forms.IntegerField(min_value=0)

    def save(self, commit=True):
        object = super(CreateClubForm, self).save(commit=commit)

        # Assign club to user
        if self.user.role == RoleUser.Roles.VIEWER:
            self.user.role = RoleUser.Roles.E_BOARD
            self.user.club = object
            self.user.save()

        # Create constitution
        self.instance.create_constitution(
            club=object,
            structure=json.load(open(finders.find("clubs/TEMPLATE_CONSTITUTION.json"))),
            purpose=self.cleaned_data.get("purpose", ""),
            affiliation=self.cleaned_data.get("affiliation", ""),
            dues_amount=self.cleaned_data.get("dues", ""),
        )
        