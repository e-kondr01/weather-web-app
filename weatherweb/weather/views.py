import json
import requests

from django.http import HttpResponseRedirect
from django.shortcuts import render


def index(request):
    return HttpResponseRedirect('/weather/')


def main(request):
    """Gets weather forecast for a week from three sources:
    OpenWeather, weather.com and yandex. Returns
    JSON results and an average result."""
    #  Location params
    latitude = 60
    longitude = 30
    days = 5

    #  Weather.com API
    weathercom_json = requests.get(f'http://api.weather.com/v1/geocode/{latitude}/{longitude}/forecast/daily/{days}day.json',
        params={'apiKey': 'dc5ea0e10f11465f9ea0e10f11e65fa6'})

    #  OpenWeather API
    openweather_json = requests.get('https://api.openweathermap.org/data/2.5/onecall',
        params={'lat': latitude, 'lon': longitude, 'appid': 'c2788a7691e78525795de7170c9f349e'})

    #  WeatherBit API
    weatherbit_json = requests.get('https://weatherbit-v1-mashape.p.rapidapi.com/forecast/3hourly',
        headers={'x-rapidapi-host': "weatherbit-v1-mashape.p.rapidapi.com",
                 'x-rapidapi-key': "7364d7fb71msh2d462a6fff9d1b1p102b53jsnff2949c01c27"},
        params={'lat': latitude, 'lon': longitude, "lang":"en"},
        )

    #  Processing data
    pass

    return render(request, 'weatherweb/weather.html', {
        'weathercom': weathercom_json.json(),
        'openweather': openweather_json.json(),
        'weatherbit': weatherbit_json.json()
    })
