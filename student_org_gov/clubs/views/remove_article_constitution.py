from django.http import HttpResponseBadRequest, HttpResponseForbidden, HttpResponseRedirect
from django.urls import reverse

from student_org_gov.decorators import club_exists, club_required, role_required
from student_org_gov.views_templates import post
from users.models import RoleUser

from clubs import models


@role_required(RoleUser.Roles.E_BOARD)
def view(request):
    data = post(request)
    if data == False:
        return HttpResponseForbidden("POST request expected.")

    try:
        article = models.Article.objects.get(pk=data.get("article"))
    except:
        return HttpResponseBadRequest("Model data not found")
        
    club = article.constitution.club

    @club_exists
    @club_required
    def sub(request, club_url):        
        # Do not delete last article
        if len(article.constitution.articles.all()) > 1:
            article.delete()

        return HttpResponseRedirect(reverse("edit_constitution", kwargs={
            "club_url": club_url
        }))
            
    return sub(request, club_url=club.url)