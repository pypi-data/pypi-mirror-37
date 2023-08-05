from django.db import models
from django.db.models.fields.related import ManyToManyField


# Create your models here.
class IranCitiesFarsi(models.Model):
    number = models.IntegerField()
    province = models.IntegerField()
    city = models.CharField(max_length=100)
    latitude = models.CharField(max_length=100)
    longitude = models.CharField(max_length=100)
    # cities = CityManager()
