from __future__ import unicode_literals
from django.db import models 
import datetime

class CityWeather(models.Model):
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=2)
    zipcode = models.CharField(max_length=5)
    temperature = models.CharField(max_length=5)
    description = models.TextField()
    created_at = models.DateField(auto_now_add=True)

    def __unicode__(self):
        return self.city