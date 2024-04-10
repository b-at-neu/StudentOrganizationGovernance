from datetime import datetime

from django.http import HttpResponseBadRequest, HttpResponseRedirect
from django.urls import reverse

from student_org_gov.views_templates import post

from clubs import models
from student_org_gov.decorators import club_required, role_required
from users.models import RoleUser


# Submit a constitution for approval
@role_required(RoleUser.Roles.E_BOARD)
@club_required
def view(request, club_url):
    data = post(request)
    
    try:
        constitution = models.Constitution.objects.get(pk=data.get("constitution"))
    except:
        return HttpResponseBadRequest(f"Constitution model data with pk '{data.get('constitution')}' not found")
    
    # Check and change status and add timestamp
    if constitution.status == models.Constitution.Status.EDITED:
        constitution.status = models.Constitution.Status.SUBMITTED
        constitution.submitted_timestamp = datetime.now()
        constitution.save()

    return HttpResponseRedirect(reverse("club", kwargs={ "club_url": constitution.club.url }))