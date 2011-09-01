from models import Course, Race, Horse
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
            r1 = Race(name=race.title, course=c1)
            r1.save()

            for horse in race.horses:
                h1 = Horse(name=horse.name, race=r1)
                h1.save()

if __name__ == '__main__':
    read()
