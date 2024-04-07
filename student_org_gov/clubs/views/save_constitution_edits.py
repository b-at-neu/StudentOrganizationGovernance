from datetime import datetime

from django.http import HttpResponseBadRequest, HttpResponseRedirect
from django.urls import reverse

from student_org_gov.views_templates import post

from clubs import models
from student_org_gov.decorators import club_required, role_required
from users.models import RoleUser


# Save the edits in the constitution
@role_required(RoleUser.Roles.E_BOARD)
@club_required
def view(request, club_url):
    data = post(request)

    print(data)

    try:
        constitution = models.Constitution.objects.get(pk=data.get("constitution"))
    except:
        return HttpResponseBadRequest("Model data not found")

    # Update all model data
    for k, v in data.items():
        split_k = k.split("#")

        # Ignore improper formats
        if len(split_k) != 2:
            continue

        type = split_k[0]
        id = split_k[1]

        # Handle articles
        if type == "article":
            article = models.Article.objects.get(pk=id)
            article.title = v
            article.save()

        # Handle sections
        elif type == "section":
            section = models.Section.objects.get(pk=id)
            section.content = v
            section.save()

    return HttpResponseRedirect(reverse("constitution", kwargs={ 
        "club_url": constitution.club.url, 
        "constitution_pk": constitution.pk 
    }))