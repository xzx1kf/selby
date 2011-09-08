from django.db import models

class Course(models.Model):
    name = models.CharField(max_length=50)
    going = models.CharField(max_length=50)

    def __unicode__(self):
        return self.name

class Race(models.Model):
    name = models.CharField(max_length=200)
    distance = models.CharField(max_length=10)
    time = models.TimeField()
    course = models.ForeignKey(Course)
    runners = models.IntegerField()

    def __unicode__(self):
        return self.name

class Horse(models.Model):
    name = models.CharField(max_length=50)
    weight = models.IntegerField()
    race = models.ForeignKey(Race)
    last_ran = models.IntegerField()
    forecast_odds = models.DecimalField(max_digits=5, decimal_places=2)

