from django.db import models

class Livedata(models.Model):
    country = models.CharField(max_length = 120, null = False, blank = False)
    dead = models.CharField(max_length = 120, null = False, blank = False)
    confirmed = models.CharField(max_length = 120, null = False, blank = False)
    recovered = models.CharField(max_length = 120, null = False, blank = False, default='-')

class GlobalStats(models.Model):
    date = models.CharField(max_length = 120, null = False, blank = False, default='')
    dead = models.CharField(max_length = 120, null = False, blank = False)
    confirmed = models.CharField(max_length = 120, null = False, blank = False)
    recovered = models.CharField(max_length = 120, null = False, blank = False, default='-')   

class CountryConfirmedHistory(models.Model):
    c1 = models.CharField(max_length = 120, null = False, blank = False)
    c2 = models.CharField(max_length = 120, null = False, blank = False)
    c3 = models.CharField(max_length = 120, null = False, blank = False)
    c4 = models.CharField(max_length = 120, null = False, blank = False)
    c5 = models.CharField(max_length = 120, null = False, blank = False)
