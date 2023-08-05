from django.shortcuts import render
from django.http import HttpResponse
from django.http.response import JsonResponse
from .utils import PrayTimes
from datetime import date
from .utils.PrayerTimeProvider import DatePrayerTime
from .models import IranCitiesFarsi
from .serializers import IranCitiesSerializer
from rest_framework import status


# Create your views here.
def lat_long(request, lat, long):
    return JsonResponse(DatePrayerTime.get_by_long_lat(lat, long), safe=False)


def date_lat_long(request, year, month, day, lat, long, tz):
    return JsonResponse(DatePrayerTime.get_by_date_lat_long(year, month, day, lat, long, float(tz)), safe=False)


def city(request, city):
    try:
        city_obj = IranCitiesFarsi.objects.filter(city__contains=city)
        cs = IranCitiesSerializer(city_obj, many=True)
        if len(cs.data) > 0:
            return JsonResponse(
                DatePrayerTime.get_by_city(cs.data[0].get('latitude'), cs.data[0].get('longitude'),
                                           tz=3.5), safe=False)
        else:
            return JsonResponse("Not Found", safe=False)
    except IranCitiesFarsi.DoesNotExist:
        return JsonResponse("Not Found", status=status.HTTP_404_NOT_FOUND, safe=False)
