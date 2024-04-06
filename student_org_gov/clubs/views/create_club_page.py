from django.urls import reverse

from clubs import forms
from student_org_gov.views_templates import render_form

from student_org_gov.decorators import role_required
from users.models import RoleUser

# Create a new club
@role_required(RoleUser.Roles.VIEWER)
def view(request):
    return render_form(
        request=request,
        form=forms.CreateClubForm(request.POST or None, user=request.user), 
        template="clubs/create_club.html", 
        success_url=reverse("clubs")
    )