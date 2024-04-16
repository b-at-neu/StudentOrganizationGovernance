from django.http import HttpResponseBadRequest, HttpResponseRedirect
from django.urls import reverse
from django.views.decorators.http import require_POST

from student_org_gov.views_templates import post

from clubs import models
from student_org_gov.decorators import role_required
from clubs.models import Club
from users.models import RoleUser


@require_POST
@role_required(RoleUser.Roles.ADMIN)
def view(request):
    data = post(request)

    try:
        club = Club.objects.get(pk=data.get("club"))
    except:
        return HttpResponseBadRequest(f"Club model data with pk '{data.get('club')}' not found")
    
    constitutions = models.Constitution.objects.filter(club=club)

    # Don't delete last constitution
    if constitutions.count() > 1:
        constitutions.last().delete()
    
    return HttpResponseRedirect(reverse("club", kwargs={ "club_url": club.url }))