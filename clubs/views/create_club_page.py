from django.urls import reverse

from clubs import forms
from clubs.models.club import Club
from student_org_gov.views_templates import render_form

from student_org_gov.decorators import role_required
from users.models import RoleUser

# Create a new club
@role_required(RoleUser.Roles.VIEWER)
def view(request):
        
    form = forms.CreateClubForm(request.POST or None)

    # Create model
    if form.is_valid():
        o = Club.objects.create(
            full_name=form.cleaned_data["full_name"],
            abbreviation=form.cleaned_data["abbreviation"],
        )

        # Change user role
        if request.user.role == RoleUser.Roles.VIEWER:
            request.user.role = RoleUser.Roles.E_BOARD
            request.user.club = o
            request.user.save()

    return render_form(
        request=request,
        form=form, 
        template="clubs/create_club.html", 
        success_url=reverse("clubs")
    )