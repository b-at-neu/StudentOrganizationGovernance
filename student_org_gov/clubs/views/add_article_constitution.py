from django.http import HttpResponseBadRequest, HttpResponseForbidden, HttpResponseRedirect
from django.urls import reverse

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
        constitution = models.Constitution.objects.get(pk=data.get("constitution"))
    except:
        return HttpResponseBadRequest("Model data not found")
    
    club = constitution.club

    @club_exists
    @club_required
    def sub(request, club_url): 
        # Get new number
        if constitution.articles.last() is not None:
            number = constitution.articles.last().number + 1
        else:
            number = 1

        models.Article.objects.create(
            constitution=constitution,
            number=number,
            title=""
        )    

        return HttpResponseRedirect(reverse("edit_constitution", kwargs={
            "club_url": club_url
        }))
    
    return sub(request, club_url=club.url)