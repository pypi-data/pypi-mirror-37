from rest_framework import serializers
from .models import IranCitiesFarsi


class PrayerTimeSerializer(serializers.Serializer):
    city = serializers.CharField(required=False, allow_blank=True)
    longitude = serializers.CharField()
    latitude = serializers.CharField()
    fajr = serializers.CharField(required=False)
    toloo = serializers.CharField(required=False)
    zohr = serializers.CharField(required=False)
    ghoroob = serializers.CharField(required=False)
    maghreb = serializers.CharField(required=False)
    nimeshab = serializers.CharField(required=False)


class IranCitiesSerializer(serializers.Serializer):
    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass

    number = serializers.IntegerField()
    province = serializers.IntegerField()
    city = serializers.CharField(max_length=100)
    latitude = serializers.CharField(max_length=100)
    longitude = serializers.CharField(max_length=100)

    class Meta:
        model = IranCitiesFarsi
        fields = ('id', 'number', 'city', 'latitude', 'longitude')
