from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.template import RequestContext, loader

def updateAD(request):
    template = loader.get_template('admin/photo_cache.html')
    context = RequestContext(request, {})
    return HttpResponse(template.render(context))
