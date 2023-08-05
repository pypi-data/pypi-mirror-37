=====
owghat-api
=====
owghat-api is a django app for Islamic times (owghat e shar'ee)

Quick start
-----------
pip install django-owghatapi

requirements: sqlparse,djangorestframework,pytz

1. Add "owghatapi" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'owghatapi',
    ]

2. Include the owghatapi URLconf in your project urls.py like this::

    path('owghatapi/', include('owghatapi.urls')),

3. Run `python manage.py migrate` to create the owghat models and seed the DB .


5. Visit http://127.0.0.1:8000/owghatapi/<str:city-name>/ to get the times for more than 400 selected cities of iran (city name in Farsi), 
	http://127.0.0.1:8000/owghatapi/35.69439/51.42151 to get the times for today and specific location(latitude/longitude) in iran,
	and http://127.0.0.1:8000/<int:year>/<int:month>/<int:day>/<str:lat>/<str:long>/<str:tz>/ for specific time,location,and timezone
	