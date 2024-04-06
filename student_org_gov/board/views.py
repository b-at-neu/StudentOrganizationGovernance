from django.shortcuts import render
from django.db.models import Q
from clubs import models
from student_org_gov.decorators import club_constitution_exists, role_required, constitution_has_status
from users.models import RoleUser

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


@club_constitution_exists
@constitution_has_status(models.Constitution.Status.SUBMITTED)
@role_required(RoleUser.Roles.BOARD_MEMBER)
def review_constitution_page(request, club_url, constitution_pk):
    club = models.Club.objects.get(url=club_url)
    old_constitution = club.constitutions.order_by("-timestamp").filter(status=models.Constitution.Status.APPROVED).first()

    all_articles = []
    for article in models.Article.objects.filter(constitution_id=constitution_pk):
        old_article = old_constitution.articles.all().get(number=article.number) if old_constitution else None

        all_sections = []
        for section in article.sections.all():
            all_sections.append({
                "new": section,
                "old": old_article.sections.all().get(number=section.number) if old_article else None
            })

        all_articles.append({
            "new": article,
            "old": old_article,
            "sections": all_sections
        })
    
    return render(request, "board/review_constitution.html", {
        "club": club,
        "new_constitution": models.Constitution.objects.get(pk=constitution_pk),
        "all_articles": all_articles,
    })