from django.http import HttpResponseBadRequest, HttpResponseRedirect
from django.urls import reverse

from student_org_gov.views_templates import post

from clubs import models


def view(request):
    data = post(request)

    try:
        constitution = models.Constitution.objects.get(pk=data.get("constitution"))
    except:
        return HttpResponseBadRequest("Model data not found")
    
    club = constitution.club

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
        "club_url": club.url
    }))