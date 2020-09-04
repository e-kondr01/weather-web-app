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

    parsed_data = parse_weather()
    average_json = average(parsed_data)

    return render(request, 'weatherweb/weather.html', {
        'weathercom': parsed_data['weathercom_temps'],
        'gismeteo': parsed_data['gismeteo_temps'],
        'yandex': parsed_data['yandex_temps'],
        'dates': parsed_data['dates'],
        'average': average_json
    })
