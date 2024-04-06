"""
Custom decorators for views
"""

from functools import wraps
from django.core.exceptions import PermissionDenied, ObjectDoesNotExist
from django.http import HttpResponseNotFound

from clubs.models import Club, Constitution
from users.models import RoleUser

def role_required(role):
    """
    Requires the user to have the specific role
    """
    def decorator(function): 
        @wraps(function)
        def wrap(request, *args, **kwargs):

            user = request.user
            if not user.is_anonymous and (user.role == role or user.role == RoleUser.Roles.ADMIN):
                return function(request, *args, **kwargs)
            raise PermissionDenied("Incorrect role.")

        return wrap
    return decorator



def anon_required(function): 
    """
    Requires the user to be an anon user
    """
    @wraps(function)
    def wrap(request, *args, **kwargs):

        user = request.user
        
        if user.is_anonymous:
            return function(request, *args, **kwargs)
        raise PermissionDenied("Incorrect role. Must be anonymous.")

    return wrap



def min_role_required(role):
    """
    Requires the user to have atleast the specific role or higher
    """
    def decorator(function): 
        @wraps(function)
        def wrap(request, *args, **kwargs):

            user = request.user
            if not user.is_anonymous and (user.role <= role or user.role == RoleUser.Roles.ADMIN):
                return function(request, *args, **kwargs)
            raise PermissionDenied("Insufficient role.")

        return wrap
    return decorator



def club_required(club):
    """
    Requires the user to have the specific club
    """
    def decorator(function): 
        @wraps(function)
        def wrap(request, *args, **kwargs):

            user = request.user
            if not user.is_anonymous and (user.club == club or user.role == RoleUser.Roles.ADMIN):
                return function(request, *args, **kwargs)
            raise PermissionDenied("Incorrect club.")

        return wrap
    return decorator


def club_required(function): 
    """
    Requires the user to have the club provided in the function
    (function must have club_url as a parameter)
    """
    @wraps(function)
    def wrap(request, *args, **kwargs):

        # Check for club_url parameter
        club_url = kwargs.get("club_url", None)
        if club_url is None:
            raise ValueError("'club_url' argument not provided")

        try:
            club = Club.objects.get(url=club_url)
        except ObjectDoesNotExist:
            return HttpResponseNotFound("Model data not found")

        user = request.user
        if not user.is_anonymous and (user.club == club or user.role == RoleUser.Roles.ADMIN):
            return function(request, *args, **kwargs)
        raise PermissionDenied("Incorrect club.")

    return wrap


def club_exists(function): 
    """
    Checks if the club exists and redirects otherwise
    (function must have club_url as a parameter)
    """
    @wraps(function)
    def wrap(request, *args, **kwargs):

        # Check for club_url parameter
        club_url = kwargs.get("club_url", None)
        if club_url is None:
            raise ValueError("'club_url' argument not provided")

        if Club.objects.filter(url=club_url).count():
            return function(request, *args, **kwargs)
        return HttpResponseNotFound(f"Club with url '{club_url}' does not exist.")

    return wrap



def club_constitution_exists(function):
    """
    Checks if the club and constitution exist and if they are linked
    (function must have club_url and constitutiton_pk as a parameter)
    """
    @wraps(function)
    def wrap(request, *args, **kwargs):

        # Check for club_url parameter
        club_url = kwargs.get("club_url", None)
        if club_url is None:
            raise ValueError("'club_url' argument not provided")
        
        # Check for constitution_pk parameter
        constitution_pk = kwargs.get("constitution_pk", None)
        if constitution_pk is None:
            raise ValueError("'constitution_pk' argument not provided")

        # Check club exists
        if not Club.objects.filter(url=club_url).count():
            return HttpResponseNotFound(f"Club with url '{club_url}' does not exist.")
    
        # Check consitution exists
        if not Constitution.objects.filter(pk=constitution_pk).count():
            return HttpResponseNotFound(f"Constitution with id '{constitution_pk}' does not exist.")
        
        # Check for link
        if not Constitution.objects.get(pk=constitution_pk).club.url == club_url:
            return HttpResponseNotFound(f"Constitution with id '{constitution_pk}' is not assosiated with club url '{club_url}'")
        
        return function(request, *args, **kwargs)

    return wrap



def constitution_has_status(status):
    """
    Checks if the constitution has the provided status
    (function must have constitution_pk as a parameter)
    """
    def decorator(function): 
        @wraps(function)
        def wrap(request, *args, **kwargs):

            # Check for constitution_pk parameter
            constitution_pk = kwargs.get("constitution_pk", None)
            if constitution_pk is None:
                raise ValueError("'constitution_pk' argument not provided")

            if Constitution.objects.get(pk=constitution_pk).status == status:
                return function(request, *args, **kwargs)
            raise PermissionDenied(f"Constitution does not have proper status.")

        return wrap
    return decorator