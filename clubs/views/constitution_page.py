from django.shortcuts import render
from django.views.decorators.http import require_GET

from clubs import models
from student_org_gov.decorators import club_constitution_exists
from clubs.models import Club


@require_GET
@club_constitution_exists
def view(request, club_url, constitution_pk):
    return render(request, "clubs/constitution.html", {
        'club': Club.objects.get(url=club_url),
        'constitution': models.Constitution.objects.get(pk=constitution_pk),
        'articles': list(models.Article.objects.filter(constitution__pk=constitution_pk).order_by('number')),
    })