from datetime import datetime

from django.http import HttpResponseBadRequest, HttpResponseRedirect
from django.urls import reverse

from student_org_gov.views_templates import post

from clubs import models
from student_org_gov.decorators import role_required
from users.models import RoleUser



# Approval or denial of a constitution
@role_required(RoleUser.Roles.BOARD_MEMBER)
def view(request):
    data = post(request)

    try:
        constitution = models.Constitution.objects.get(pk=data.get("constitution"))
    except:
        return HttpResponseBadRequest("Model data not found")
    decision = data.get("decision")

    if decision != "0" and decision != "1":
        return HttpResponseBadRequest("Not proper type for 'decision'")
        
    # Check and change status and add timestamp
    if constitution.status == models.Constitution.Status.SUBMITTED:
        if decision == "1":
            constitution.status = models.Constitution.Status.APPROVED
        elif decision == "0":
            constitution.status = models.Constitution.Status.DENIED
        constitution.reviewed_timestamp = datetime.now()
        constitution.save()

    return HttpResponseRedirect(reverse("clubs"))