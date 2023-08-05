from datetime import date
from datetime import datetime

from .PrayTimes import PrayTimes


class DatePrayerTime():

    @staticmethod
    def get_by_long_lat(lat, long):
        praytimes = PrayTimes()
        praytimes.setMethod("Tehran")
        times = praytimes.getTimes(date.today(), (float(lat), float(long)), 3.5)
        time_array = ['Fajr', 'Sunrise', 'Dhuhr', 'Sunset', 'Maghrib', 'Midnight']
        time_dict = {}
        for i in time_array:
            print(i + ': ' + times[i.lower()])
            time_dict[i.lower()] = times[i.lower()]
        return time_dict

    @staticmethod
    def get_by_date_lat_long(year, month, day, lat, long, tz):
        date_str = str(year) + "-" + str(month) + "-" + str(day)
        format_str = '%Y-%m-%d'
        praytimes = PrayTimes()
        datetime_obj = datetime.strptime(date_str, format_str)

        praytimes.setMethod("Tehran")
        times = praytimes.getTimes(datetime_obj.date(), (float(lat), float(long)), float(tz))
        time_array = ['Fajr', 'Sunrise', 'Dhuhr', 'Sunset', 'Maghrib', 'Midnight']
        time_dict = {}
        for i in time_array:
            print(i + ': ' + times[i.lower()])
            time_dict[i.lower()] = times[i.lower()]
        return time_dict

    @staticmethod
    def get_by_city(latitude, longitude, tz):
        # date_str = str(year) + "-" + str(month) + "-" + str(day)
        # format_str = '%Y-%m-%d'
        praytimes = PrayTimes()
        # datetime_obj = datetime.strptime(date_str, format_str)

        praytimes.setMethod("Tehran")
        times = praytimes.getTimes(date.today(), (float(latitude), float(longitude)), float(tz))
        time_array = {'Fajr': 'فجر', 'Sunrise': 'طلوع', 'Dhuhr': 'ظهر', 'Sunset': 'غروب', 'Maghrib': 'مغرب',
                      'Midnight': 'نیمه شب'}
        time_dict = {}
        for i in time_array:
            time_dict[time_array.get(i)] = times[i.lower()]
        return time_dict
