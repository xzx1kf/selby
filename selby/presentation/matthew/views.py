from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
import cPickle
from django.conf import settings

def index(request):
    #f = open('temp.obj', 'r')
    #courses = cPickle.load(f)
    #f.close()

    context = RequestContext(request, {
        'courses': settings.COURSES,
        })
    return render_to_response('main.html', context)

def detail(request, matthew_id):
    return HttpResponse("You're looking at the results of matthew %s." % matthew_id)
