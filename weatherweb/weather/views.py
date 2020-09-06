import json
import requests

from django.http import HttpResponseRedirect
from django.shortcuts import render
from weather.average import average
from weather.parser import parse_weather


def index(request):
    return HttpResponseRedirect('/weather/')


def main(request):
    hours = request.GET.get('unit', 'celsius')
    daysCount = request.GET.get('daysCount', 10)

    parsed_data = parse_weather()
    average_json = average(parsed_data)

    return render(request, 'weatherweb/weather.html', {
        'weathercom': parsed_data['weathercom_temps'],
        'gismeteo': parsed_data['gismeteo_temps'],
        'yandex': parsed_data['yandex_temps'],
        'dates': parsed_data['dates'],
        'average': average_json
    })
