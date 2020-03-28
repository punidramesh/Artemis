from django.db import models

class Livedata(models.Model):
    country = models.CharField(max_length = 120)
    dead = models.CharField(max_length = 120)
    confirmed = models.CharField(max_length = 120)
    recovered = models.CharField(max_length = 120)
