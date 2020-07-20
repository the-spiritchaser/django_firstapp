from django.db import models

class Anime(models.Model):

    SATURDAY = 0
    SUNDAY = 1
    MONDAY = 2
    TUESDAY = 3
    WEDNESDAY =4
    THURSDAY = 5
    FRIDAY = 6
 
    title = models.CharField(max_length=225)

    start_date = models.DateTimeField()

    end_date = models.DateTimeField()

    week = models.IntegerField(editable=False)

    studio = models.ForeignKey('Studio')


class Studio(models.Model):

    name = models.CharField(max_length=225)
