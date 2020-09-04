import json
import requests

from django.http import HttpResponseRedirect
from django.shortcuts import render
from weather.average import average
from weather.parser import parse_weather


def index(request):
    return HttpResponseRedirect('/weather/')


def main(request):
    """Gets weather forecast for a week from three sources:
    Gismeteo, weather.com and yandex weather. Returns
    parsed forecast data and an average result."""

    """
    #  Location params
    latitude = 60
    longitude = 30
    days = 5

    #  Weather.com API
    weathercom_json = requests.get(f'http://api.weather.com/v1/geocode/{latitude}/{longitude}/forecast/daily/{days}day.json',
        params={'apiKey': 'dc5ea0e10f11465f9ea0e10f11e65fa6'}).json()


    #  OpenWeather API
    openweather_json = requests.get('https://api.openweathermap.org/data/2.5/onecall',
        params={'lat': latitude, 'lon': longitude, 'appid': 'c2788a7691e78525795de7170c9f349e'}).json()

    #  WeatherBit API
    weatherbit_json = requests.get('https://weatherbit-v1-mashape.p.rapidapi.com/forecast/3hourly',
        headers={'x-rapidapi-host': "weatherbit-v1-mashape.p.rapidapi.com",
                 'x-rapidapi-key': "7364d7fb71msh2d462a6fff9d1b1p102b53jsnff2949c01c27"},
        params={'lat': latitude, 'lon': longitude, "lang":"en"}).json() 
    """
    parsed_data = parse_weather()
    average_json = average(parsed_data)

    return render(request, 'weatherweb/weather.html', {
        'weathercom': parsed_data['weathercom'],
        'gismeteo': parsed_data['gismeteo'],
        'yandex': parsed_data['yandex'],
        'average': average_json
    })
