from django.shortcuts import render
from django.views.decorators.http import require_GET

from student_org_gov.decorators import club_exists, club_required
from clubs.models import Club


@require_GET
@club_exists
@club_required
def view(request, club_url):
    return render(request, "clubs/club.html", {
        'club': Club.objects.get(url=club_url)
    })