from django.http import HttpResponseRedirect
from django.shortcuts import render
import requests

from .models import City
from .forms import CityForm


def index(request):
    error = ''
    appid = 'e131f94b32b73a7c982e359f5457b2fb'
    url = 'https://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=' + appid
    cities = City.objects.all()

    if request.method == 'POST':
        form = CityForm(request.POST)
        res = requests.get(url.format(request.POST['name'])).json()

        if res['cod'] == 200:
            form.save()
        else:
            error = res['message']

    form = CityForm()
    all_cities = []

    for city in cities:
        res = requests.get(url.format(city.name)).json()
        city_info = {
            'id': city.id,
            'city': city.name,
            'temp': res['main']['temp'],
            'icon': res['weather'][0]['icon'],
        }
        all_cities.append(city_info)

    context = {
        'all_info': all_cities,
        'error': error,
        'form': form,
    }
    return render(request, 'weather/index.html', context)


def delete(request, id):
    City.objects.get(id=id).delete()
    return HttpResponseRedirect('/')
