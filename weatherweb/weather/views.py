import json
import requests

from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from weather.average import average
from weather.parser import parse_weather


def index(request):
    return HttpResponseRedirect('/weather/')


def main(request):
    unit = request.GET.get('unit', 'celsius')
    days_count = request.GET.get('daysCount', '10')

    parsed_data = parse_weather(unit=unit, days_count=int(days_count))
    average_data = average(parsed_data)
    parsed_data['forecastsAverage'] = average_data
    return JsonResponse(parsed_data, json_dumps_params={'ensure_ascii': False})
