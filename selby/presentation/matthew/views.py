from django.shortcuts import render_to_response
from django.template import RequestContext
from matthew.models import Course, Race, Horse

def list_courses(request):
    course_list = Course.objects.all()
    context = RequestContext(request, {
        'list_name': 'Courses:',
        'list': course_list,
        })
    return render_to_response('list.html', context)

def list_races(request, course_id):
    race_list = Race.objects.filter(course=course_id)
    context = RequestContext(request, {
        'list_name': 'Races',
        'list': race_list,
        })
    return render_to_response('list.html', context)

def list_horses(request, race_id):
    horse_list = Horse.objects.filter(race=race_id)
    context = RequestContext(request, {
        'list_name': 'Horses',
        'list': horse_list,
        })
    return render_to_response('list.html', context)
    
