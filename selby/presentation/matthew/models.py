from django.db import models

class Course(models.Model):
    name = models.CharField(max_length=50)
    going = models.CharField(max_length=50)

    def __unicode__(self):
        return self.name

class Race(models.Model):
    name = models.CharField(max_length=200)
    course = models.ForeignKey(Course)

    def __unicode__(self):
        return self.name

class Horse(models.Model):
    name = models.CharField(max_length=50)
    race = models.ForeignKey(Race)

