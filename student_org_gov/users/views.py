from django.http import HttpResponseBadRequest, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib import auth

from student_org_gov.decorators import anon_required, min_role_required, role_required
from student_org_gov.views_templates import post, render_form

from .models import RoleUser
from .forms import LoginForm, SignUpForm
from clubs.models import Club


@role_required(RoleUser.Roles.ADMIN)
def users_overview(request):
    return render(request, 'users/users.html', context={
        "users": RoleUser.objects.all(),
        "roles": RoleUser.Roles.choices,
        "clubs": Club.objects.all()
    })


@role_required(RoleUser.Roles.ADMIN)
def edit_role(request):
    data = post(request)

    if len(data.get("role")) == 0:
        return HttpResponseBadRequest("Improper role provided")

    try:
        user = RoleUser.objects.get(pk=data.get('user'))
        user.role = data.get('role')
    except:
        return HttpResponseBadRequest("Model data not found")

    user.save()

    return HttpResponseRedirect(reverse("users"))


@role_required(RoleUser.Roles.ADMIN)
def edit_club(request):
    data = post(request)

    if len(data.get("club")) == 0:
        return HttpResponseBadRequest("Improper club provided. For none, write 'None'")
    
    try:
        user = RoleUser.objects.get(pk=data.get('user'))

        # Check for none
        club_pk = data.get('club')
        if club_pk == 'None':
            user.club = None
        else:
            user.club_id = club_pk
        user.save()
    except:
        return HttpResponseBadRequest("Model data not found")

    return HttpResponseRedirect(reverse("users"))


@anon_required
def signup(request):
    def success_action():
        user = auth.authenticate(username=request.POST['username'], password=request.POST['password1'])
        if user:
            auth.login(request, user)

    return render_form(
        request=request,
        form=SignUpForm(request.POST or None), 
        template="users/signup.html", 
        success_url=reverse("home"),
        success_action=success_action
    )


@anon_required
def login(request):
    def success_action():
        user = auth.authenticate(username=request.POST['username'], password=request.POST['password'])
        if user:
            auth.login(request, user)

    return render_form(
        request=request,
        form=LoginForm(request.POST or None), 
        template="users/login.html", 
        success_url=reverse("home"),
        success_action=success_action
    )


@min_role_required(RoleUser.Roles.VIEWER)
def logout(request):

    auth.logout(request)

    return HttpResponseRedirect(reverse("home"))