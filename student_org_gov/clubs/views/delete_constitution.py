from django.http import HttpResponseBadRequest, HttpResponseRedirect
from django.urls import reverse

from student_org_gov.views_templates import post

from clubs import models
from student_org_gov.decorators import role_required
from clubs.models import Club
from users.models import RoleUser


# Delete a constitution
@role_required(RoleUser.Roles.ADMIN)
def view(request):
    data = post(request)

    try:
        club = Club.objects.get(pk=data.get("club"))
        constitutions = models.Constitution.objects.filter(club=club)
    except:
        return HttpResponseBadRequest("Model data not found")

    # Don't delete last constitution
    if constitutions.count() > 1:
        constitutions.last().delete()
    
    return HttpResponseRedirect(reverse("club", kwargs={ "club_url": club.url }))