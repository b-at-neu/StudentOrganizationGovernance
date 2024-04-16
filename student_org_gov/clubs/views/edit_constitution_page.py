from django.shortcuts import render
from django.views.decorators.http import require_GET

from clubs import models
from student_org_gov.decorators import club_exists, club_required
from clubs.models import Club


@require_GET
@club_exists
@club_required
def view(request, club_url):
    club = Club.objects.get(url=club_url)
    constitution = club.create_edit_constitution()
    return render(request, "clubs/edit_constitution.html", {
        'club': club,
        'constitution': constitution,
        'articles': list(models.Article.objects.filter(constitution__pk=constitution.pk).order_by('number')),
    })