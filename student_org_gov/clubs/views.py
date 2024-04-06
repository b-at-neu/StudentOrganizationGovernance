from datetime import datetime

from django.http import HttpResponseBadRequest, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from student_org_gov.views_templates import post, render_form

from . import models, forms
from student_org_gov.decorators import club_constitution_exists, club_exists, club_required, min_role_required, role_required
from clubs.models import Club
from users.models import RoleUser

############
# Page views
############

# Overview of all clubs
def clubs_page(request):
    return render(request, "clubs/clubs.html", {
        'clubs': list(Club.objects.all())
    })



# View all information about a certain club
@club_exists
@club_required
def club_page(request, club_url):
    return render(request, "clubs/club.html", {
        'club': Club.objects.get(url=club_url)
    })



# Create a new club
@role_required(RoleUser.Roles.VIEWER)
def create_club_page(request):
    return render_form(
        request=request,
        form=forms.CreateClubForm(request.POST or None, user=request.user), 
        template="clubs/create_club.html", 
        success_url=reverse("clubs")
    )



# Constitution of a certain club
@club_constitution_exists
def constitution_page(request, club_url, constitution_pk):
    return render(request, "clubs/constitution.html", {
        'club': Club.objects.get(url=club_url),
        'constitution': models.Constitution.objects.get(pk=constitution_pk),
        'articles': list(models.Article.objects.filter(constitution__pk=constitution_pk).order_by('number')),
    })



# Edit a constitution of a certain club
@club_exists
@club_required
def edit_constitution_page(request, club_url):
    club = Club.objects.get(url=club_url)
    constitution = club.create_edit_constitution()
    return render(request, "clubs/edit_constitution.html", {
        'club': club,
        'constitution': constitution,
        'articles': list(models.Article.objects.filter(constitution__pk=constitution.pk).order_by('number')),
    })


################
# Post methods #
################


# Delete a constitution
@role_required(RoleUser.Roles.ADMIN)
def delete_constitution(request):
    data = post(request)

    try:
        club = Club.objects.get(pk=data.get("club"))
        constitutions = models.Constitution.objects.filter(club=club)
    except:
        return HttpResponseBadRequest("Model data not found")

    # Don't delete last constitution
    if constitutions.count() > 1:
        constitutions.last().delete()
    
    return HttpResponseRedirect(reverse("club", kwargs={ "club_url": club.url }))



# Delete a club
@role_required(RoleUser.Roles.ADMIN)
def delete_club(request):
    data = post(request)

    try:
        club = Club.objects.get(pk=data.get("club"))
    except:
        return HttpResponseBadRequest("Model data not found")

    # Delete club
    club.delete()
    
    return HttpResponseRedirect(reverse("clubs"))



# Submit a constitution for approval
@role_required(RoleUser.Roles.E_BOARD)
@club_required
def submit_constitution(request, club_url):
    data = post(request)
    
    try:
        constitution = models.Constitution.objects.get(pk=data.get("constitution"))
    except:
        return HttpResponseBadRequest("Model data not found")
    
    # Check and change status and add timestamp
    if constitution.status == models.Constitution.Status.EDITED:
        constitution.status = models.Constitution.Status.SUBMITTED
        constitution.submitted_timestamp = datetime.now()
        constitution.save()

    return HttpResponseRedirect(reverse("club", kwargs={ "club_url": constitution.club.url }))



# Approval or denial of a constitution
@role_required(RoleUser.Roles.BOARD_MEMBER)
def review_constitution(request):
    data = post(request)

    try:
        constitution = models.Constitution.objects.get(pk=data.get("constitution"))
    except:
        return HttpResponseBadRequest("Model data not found")
    decision = data.get("decision")

    if decision != "0" and decision != "1":
        return HttpResponseBadRequest("Not proper type for 'decision'")
        
    # Check and change status and add timestamp
    if constitution.status == models.Constitution.Status.SUBMITTED:
        if decision == "1":
            constitution.status = models.Constitution.Status.APPROVED
        elif decision == "0":
            constitution.status = models.Constitution.Status.DENIED
        constitution.reviewed_timestamp = datetime.now()
        constitution.save()

    return HttpResponseRedirect(reverse("clubs"))



# Save the edits in the constitution
@role_required(RoleUser.Roles.E_BOARD)
@club_required
def save_constitution_edits(request, club_url):
    data = post(request)

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

        elif type == "section":
            section = models.Section.objects.get(pk=id)
            section.content = v
            section.save()

    return HttpResponseRedirect(reverse("constitution", kwargs={ 
        "club_url": constitution.club.url, 
        "constitution_pk": constitution.pk 
    }))



def remove_article_constitution(request):
    data = post(request)

    try:
        article = models.Article.objects.get(pk=data.get("article"))
    except:
        return HttpResponseBadRequest("Model data not found")
    
    club = article.constitution.club

    # Do not delete last article
    if len(article.constitution.articles.all()) > 1:
        article.delete()

    return HttpResponseRedirect(reverse("edit_constitution", kwargs={
        "club_url": club.url
    }))



def add_article_constitution(request):
    data = post(request)

    try:
        constitution = models.Constitution.objects.get(pk=data.get("constitution"))
    except:
        return HttpResponseBadRequest("Model data not found")
    
    club = constitution.club

    # Get new number
    if constitution.articles.last() is not None:
        number = constitution.articles.last().number + 1
    else:
        number = 1

    models.Article.objects.create(
        constitution=constitution,
        number=number,
        title=""
    )    

    return HttpResponseRedirect(reverse("edit_constitution", kwargs={
        "club_url": club.url
    }))



def remove_section_constitution(request):
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


def add_section_constitution(request):
    data = post(request)

    try:
        article = models.Article.objects.get(pk=data.get("article"))
    except:
        return HttpResponseBadRequest("Model data not found")
    
    club = article.constitution.club

    # Get new number
    if article.sections.last() is not None:
        number = article.sections.last().number + 1
    else:
        number = 1

    models.Section.objects.create(
        article=article,
        number=number,
        content=""
    )    

    return HttpResponseRedirect(reverse("edit_constitution", kwargs={
        "club_url": club.url
    }))