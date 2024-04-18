"""
Functions to assist in views
"""

import json
from django.http import HttpResponseRedirect
from django.shortcuts import render

def default_function():
    pass

def render_form(request, form, template, success_url, success_action=default_function):
    """
    View template for rendering a django form
    """

    if form.is_valid():
        # Create model based on form
        if callable(getattr(form, "save", None)):
            form.save()
        success_action()
        return HttpResponseRedirect(success_url)
    
    return render(request, template, { 'form': form })


def post(request):
    """
    View template for a POST form
    """

    # Check method
    if request.method != "POST":
        return False
    
    # Check if data is json or html form
    elif request.content_type == "application/json":
        data = json.loads(request.body)
        if not isinstance(data, dict):
            data = json.loads(data)
        return data
    return request.POST