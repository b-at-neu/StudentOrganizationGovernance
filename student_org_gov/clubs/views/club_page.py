from django.shortcuts import render

from student_org_gov.decorators import club_exists, club_required
from clubs.models import Club

# View all information about a certain club
@club_exists
@club_required
def view(request, club_url):
    return render(request, "clubs/club.html", {
        'club': Club.objects.get(url=club_url)
    })