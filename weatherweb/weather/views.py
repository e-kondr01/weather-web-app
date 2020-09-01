import json
import requests

from django.http import HttpResponseRedirect
from django.shortcuts import render


def index(request):
    return HttpResponseRedirect('/weather/')


def main(request):
    """Gets weather forecast for a week from three sources:
    Gismeteo, weather.com and yandex. Returns
    JSON results and an average result."""
    #  Location params
    latitude = 60
    longitude = 30
    days = 7

    #  Weather.com API
    weathercom_json = requests.get(f'http://api.weather.com/v1/geocode/{latitude}/{longitude}/forecast/daily/{days}day.json',
        params={'apiKey': 'dc5ea0e10f11465f9ea0e10f11e65fa6'})

    #  Gismeteo API
    gismeteo_json = requests.get('https://api.gismeteo.net/v2/weather/forecast',
        params={'latitude': latitude, 'longitude': longitude, 'days': days},
        headers={'X-Gismeteo-Token': '56b30cb255.3443075'})
    
    print(gismeteo_json.request.headers)

    #  Yandex API
    yandex_json = requests.get('https://api.weather.yandex.ru/v2/informers',
        headers={'X-Yandex-API-Key': 'c54630e9-d293-44b1-ab1c-3add95fa374c'},
        params={'lat': latitude, 'lon': longitude},
        )

    print(yandex_json.request.headers)
    #  Processing data
    pass

    return render(request, 'weatherweb/weather.html', {
        'weathercom': weathercom_json.json(),
        'gismeteo': gismeteo_json.json(),
        'yandex': yandex_json.json()
    })
