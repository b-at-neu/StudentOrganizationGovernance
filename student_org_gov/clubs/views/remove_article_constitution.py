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

    # Do not delete last article
    if len(article.constitution.articles.all()) > 1:
        article.delete()

    return HttpResponseRedirect(reverse("edit_constitution", kwargs={
        "club_url": club.url
    }))