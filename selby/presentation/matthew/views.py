from django.shortcuts import render_to_response
from django.template import RequestContext
from matthew.models import Course, Race, Horse
from django.db.models import Q

def list_courses(request):
    course_list = Course.objects.all()
    context = RequestContext(request, {
        'list_name': 'Courses:',
        'list': course_list,
        })
    return render_to_response('list.html', context)

def list_races(request, course_id):
    race_list = Race.objects.filter(course=course_id)

    # Put a filter on the races so that only races that are handicaps
    # are shown.
    race_list = race_list.filter(name__icontains='handicap')
    race_list = race_list.filter(runners__gte=11)
    race_list = race_list.filter(runners__lte=16)
    race_list = race_list.filter(distance__lt=2200)

    context = RequestContext(request, {
        'list_name': 'Races',
        'list': race_list,
        })
    return render_to_response('list_races.html', context)

def list_horses(request, race_id):
    horse_list = Horse.objects.filter(race=race_id)

    # Put a filter on the horses so that only horses out of the
    # top 5 weights are shown.
    horse_list = horse_list.filter(weight__gt=5)

    context = RequestContext(request, {
        'list_name': 'Horses',
        'list': horse_list,
        })
    return render_to_response('list_horses.html', context)

def layem(request): 

    horses = Horse.objects.filter(
            weight__gt=5).filter(
            last_ran__gte=8).filter(
            forecast_odds__gte=5).filter(
            forecast_odds__lte=8.5).filter(
            race__distance__lt=2200).filter(
            race__name__icontains='handicap').filter(
            Q(race__course__going__icontains='good') | 
            Q(race__course__going__icontains='standard')).filter(
            race__runners__lte=16).filter(
            race__runners__gte=11)

    
    context = RequestContext(request, {
        'horses': horses,
        })

    return render_to_response('layem.html', context)
