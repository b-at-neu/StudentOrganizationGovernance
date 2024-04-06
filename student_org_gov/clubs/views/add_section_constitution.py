from django.http import HttpResponseBadRequest, HttpResponseRedirect
from django.urls import reverse

from student_org_gov.views_templates import post

from clubs import models


def view(request):
    data = post(request)

    try:
        article = models.Article.objects.get(pk=data.get("article"))
    except:
        return HttpResponseBadRequest("Model data not found")
    
    club = article.constitution.club

    # Get new number
    if article.sections.last() is not None:
        number = article.sections.last().number + 1
    else:
        number = 1

    models.Section.objects.create(
        article=article,
        number=number,
        content=""
    )    

    return HttpResponseRedirect(reverse("edit_constitution", kwargs={
        "club_url": club.url
    }))