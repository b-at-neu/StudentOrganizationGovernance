from django.shortcuts import render

from clubs.models.club import Club

# Overview of all clubs
def view(request):
    return render(request, "clubs/clubs.html", {
        'clubs': list(Club.objects.all())
    })