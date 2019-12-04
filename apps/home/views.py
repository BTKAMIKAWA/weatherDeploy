import requests
from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.shortcuts import render
from django.views.decorators.cache import cache_page
from apps.home.models import *
from .models import CityWeather
from django.shortcuts import render, redirect, HttpResponse
CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)

def index(request):
    return render(request, "home/index.html")

def search_address(request):
    return redirect(request, "/search_address")

@cache_page(CACHE_TTL)
def address(request):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=89953fd7459b665dc09abe3d6513a015'
    
    if request.method == "POST":
        city = request.POST["city"]
  
    response = requests.get(url.format(city)).json()    
    
    temperature = response['main']['temp']
    low = response['main']['temp_min']
    high = response['main']['temp_max']
    humidity = response['main']['humidity']
    wind = response['wind']['speed']
    description = response['weather'][0]['description']

    city_weather = {
        'city': city,
        'temperature': temperature,
        'low' : low,
        'high' : high,
        'humidity' : humidity,
        'wind' : wind,
        'description': description,
        'icon': response['weather'][0]['icon'],
    }
    
    context = {'city_weather' : city_weather}  

    address = request.POST['address']
    state = request.POST['state']
    zipcode = request.POST['zipcode']

    request.session['address'] = address
    request.session['state'] = state
    request.session['zipcode'] = zipcode

    new_city = CityWeather.objects.create(city=city, state=state, zipcode=zipcode,temperature=temperature, description=description)
    
    print(response)
    return render(request, "home/address.html", context)

def search_db(request):
    return redirect(request, "/search_db")

def searchdb(request):
    context = {
        "all_cities" : CityWeather.objects.all()
    }
    return render(request, "home/db.html", context)

def filter_city(request):
    return redirect(request, "filter_city")

def city(request):
    
    city = request.POST['city'].title() 
    context = {
        "city" : CityWeather.objects.filter(city=city)
    }
    return render(request, "home/city.html", context)


