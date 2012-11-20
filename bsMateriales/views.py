from django.template import RequestContext
from django.shortcuts import render_to_response

def index(request):
    """docstring for index"""
    return render_to_response('menuPrincipal.html',context_instance=RequestContext(request)) 