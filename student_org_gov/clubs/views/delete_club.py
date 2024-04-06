from django.http import HttpResponseBadRequest, HttpResponseRedirect
from django.urls import reverse

from student_org_gov.views_templates import post

from student_org_gov.decorators import role_required
from clubs.models import Club
from users.models import RoleUser


# Delete a club
@role_required(RoleUser.Roles.ADMIN)
def view(request):
    data = post(request)

    try:
        club = Club.objects.get(pk=data.get("club"))
    except:
        return HttpResponseBadRequest("Model data not found")

    # Delete club
    club.delete()
    
    return HttpResponseRedirect(reverse("clubs"))