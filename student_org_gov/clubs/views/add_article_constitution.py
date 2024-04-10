from django.http import HttpResponseBadRequest, HttpResponseForbidden, JsonResponse

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
        return HttpResponseBadRequest(f"Constitution model data with pk '{data.get('constitution')}' not found")
    
    club = constitution.club

    @club_exists
    @club_required
    def sub(request, club_url): 
        # Get new number
        if constitution.articles.last() is not None:
            number = constitution.articles.last().number + 1
        else:
            number = 1

        article = models.Article.objects.create(
            constitution=constitution,
            number=number,
            title=""
        )    

        return JsonResponse({
            "number": number,
            "pk": article.pk,
        })
    
    return sub(request, club_url=club.url)