from django.db import models

class Course(models.Model):
    name = models.CharField(max_length=50)
    going = models.CharField(max_length=50)

class Race(models.Model):
    name = models.CharField(max_length=200)
    meeting = models.ForeignKey(Course)

class Horse(models.Model):
    name = models.CharField(max_length=50)
    race = models.ForeignKey(Race)

