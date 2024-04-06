from django.http import HttpResponseBadRequest, HttpResponseRedirect
from django.urls import reverse

from student_org_gov.views_templates import post

from clubs import models


def view(request):
    data = post(request)

    try:
        section = models.Section.objects.get(pk=data.get("section"))
    except:
        return HttpResponseBadRequest("Model data not found")
    
    club = section.article.constitution.club

    # Do not delete last section
    if len(section.article.sections.all()) > 1:
        section.delete()

    return HttpResponseRedirect(reverse("edit_constitution", kwargs={
        "club_url": club.url
    }))