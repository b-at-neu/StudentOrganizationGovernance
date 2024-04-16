from django.shortcuts import render
from django.views.decorators.http import require_GET

from clubs.models.club import Club

@require_GET
def view(request):
    return render(request, "clubs/clubs.html", {
        'clubs': list(Club.objects.all())
    })