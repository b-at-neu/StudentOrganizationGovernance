from django.http import HttpResponseBadRequest, HttpResponseForbidden, JsonResponse
from django.core import serializers

from users.models import RoleUser
from student_org_gov.decorators import club_exists, club_required, role_required
from student_org_gov.views_templates import post

from clubs import models



@role_required(RoleUser.Roles.E_BOARD)
def view(request):
    data = post(request)
    if data == False:
        return HttpResponseForbidden("POST request expected.")

    try:
        constitution = models.Constitution.objects.get(pk=data.get("constitution_pk"))
    except:
        return HttpResponseBadRequest("Model data not found")
    
    @club_exists
    @club_required
    def sub(request, club_url):
        return JsonResponse({
            'constitution': constitution.get_json(),
        })
    
    return sub(request, club_url=constitution.club.url)