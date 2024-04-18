from django.shortcuts import render
from django.views.decorators.http import require_GET

from clubs import models
from student_org_gov.decorators import club_constitution_exists, role_required, constitution_has_status
from users.models import RoleUser

@require_GET
@role_required(RoleUser.Roles.BOARD_MEMBER)
def board_overview_page(request):

    club_list = []

    for club in models.Club.objects.all():
        # Add info about club to list
        club_list.append({
            'club_model': club,
            'recent_submitted_constitution': club.get_recently_submitted_constitutions().first(),
            'recent_approved_constitution': club.get_recently_approved_constitutions().first()
        })
    return render(request, "board/board_overview.html", { 'club_list': club_list })


@require_GET
@club_constitution_exists
@constitution_has_status(models.Constitution.Status.SUBMITTED)
@role_required(RoleUser.Roles.BOARD_MEMBER)
def review_constitution_page(request, club_url, constitution_pk):
    club = models.Club.objects.get(url=club_url)
    
    return render(request, "board/review_constitution.html", {
        "club": club,
        "old_constitution": club.constitutions.order_by("-timestamp").filter(status=models.Constitution.Status.APPROVED).first(),
        "constitution": models.Constitution.objects.get(pk=constitution_pk),
    })