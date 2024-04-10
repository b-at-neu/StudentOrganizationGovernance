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
        article = models.Article.objects.get(pk=data.get("article"))
    except:
        return HttpResponseBadRequest(f"Article model data with pk '{data.get('article')}' not found")
    
    club = article.constitution.club

    @club_exists
    @club_required
    def sub(request, club_url):
        # Get new number
        if article.sections.last() is not None:
            number = article.sections.last().number + 1
        else:
            number = 1

        section = models.Section.objects.create(
            article=article,
            number=number,
            content=""
        )    

        return JsonResponse({
            "number": number,
            "pk": section.pk,
            "articlepk": article.pk,
        })
    
    return sub(request, club_url=club.url)