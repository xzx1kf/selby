from models import Course, Race, Horse
from datetime import time
import cPickle

def read():
    f = open("temp.obj", 'r')
    courses = cPickle.load(f)
    f.close()
    load_sql(courses)

def load_sql(courses):
    for course in courses:

        c1 = Course(name=course.name, going=course.going)
        c1.save()

        for race in course.races:
            r1 = Race(
                    name=race.title, 
                    distance=convert_distance_to_yards(race.distance),
                    time=format_time(race.time),
                    runners=race.runners,
                    course=c1)
            r1.save()

            for horse in race.horses:
                h1 = Horse(
                        name=horse.name, 
                        race=r1,
                        weight=horse.weight,
                        last_ran=horse.last_ran,
                        forecast_odds=convert_to_decimal_odds(horse.forecast_odds))
                h1.save()

def format_time(t):
    t = t.split(':')
    race_time = time(int(t[0]) + 12, int(t[1]))
    return race_time

def convert_to_decimal_odds(fractional_odds):
    odds = fractional_odds.split('/')

    try:
        x = float(odds[0])
        y = float(odds[1])
        z = x/y + 1

        return z
    except:
        return 0

def convert_distance_to_yards(distance):
    miles, furlongs, yards = distance

    yards = yards + (furlongs * 220)
    yards = yards + (miles * 1760)

    return yards

if __name__ == '__main__':
    read()
