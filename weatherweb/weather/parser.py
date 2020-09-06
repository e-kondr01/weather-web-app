import json
import requests

from bs4 import BeautifulSoup

weekdays = {
    'Пн': 'Monday',
    'Вт': 'Tuesday',
    'Ср': 'Wednesday',
    'Чт': 'Thursday',
    'Пт': 'Friday',
    'Сб': 'Saturday',
    'Вс': 'Sunday',
}


def parse_weather(unit='', days_count=0):

    forecasts_gismeteo, days_of_week = parse_gismeteo(days_count)
    forecasts_yandex = parse_yandex(days_count, days_of_week)

    parsed_data = {}
    parsed_data['forecastsYandex'] = forecasts_yandex
    parsed_data['forecastsGismeteo'] = forecasts_gismeteo
    print(parsed_data)
    return parsed_data


def parse_weathercom():
    #  Location params
    latitude = 59.57
    longitude = 30.19
    days = 3

    #  Weather.com API
    resp = requests.get(f'http://api.weather.com/v1/geocode/{latitude}/{longitude}/forecast/daily/{days}day.json',
        params={'apiKey': 'dc5ea0e10f11465f9ea0e10f11e65fa6'}).json()

    # strange fahrenheit conversion
    temps = []
    for date in resp['forecasts']:
        try:
            temp_f = date['day']['temp']
            temp = round((temp_f - 32) / 1.8)
            temps.append(temp)
        except KeyError:
            pass
        temp_f = date['night']['temp']
        temp = round((temp_f - 32) / 1.8)
        temps.append(temp)
    return none


def parse_gismeteo(days_count):
    headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64 AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36'
        }
    resp = requests.get('https://www.gismeteo.ru/weather-sankt-peterburg-4079/10-days/',
                        headers=headers)
    parser = BeautifulSoup(resp.text,
                           'html.parser')

    forecasts_gismeteo = []

    #  Temperature
    temp_spans = parser.find_all(class_='unit unit_temperature_c')
    temp_strings = []
    for i in range(days_count * 2):
        temp_strings.append(temp_spans[i].string)
    temps = []
    for temp_string in temp_strings:
        temps.append(int(temp_string[1:]))

    #  Day of week
    day_divs = parser.find_all(class_='w_date__day')
    days_ru = []
    for i in range(days_count):
        days_ru.append(day_divs[i].string)
    days_of_week = []
    for day in days_ru:
        days_of_week.append(weekdays[day])

    #  Shorcast
    shortcast_spans = parser.find_all(class_='tooltip')
    shortcasts = []
    for i in range(days_count):
        shortcasts.append(shortcast_spans[i]['data-text'])

    for i in range(days_count):
        date = {}
        date['day_of_week'] = days_of_week[i]
        date['day'] = {}
        date['day']['shortcast'] = shortcasts[i]
        date['day']['temp'] = temps[i * 2]
        date['night'] = {}
        date['night']['shortcast'] = shortcasts[i]
        date['night']['temp'] = temps[i * 2 + 1]
        forecasts_gismeteo.append(date)

    return forecasts_gismeteo, days_of_week


def parse_yandex(days_count, days_of_week):
    '''Формат для температуры - утро, день, вечер, ночь. По два значения температуры
    на промежуток + третье "как ощущается" '''
    headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64 AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36'
        }
    resp = requests.get('https://yandex.ru/pogoda/saint-petersburg',
                        headers=headers)
    parser = BeautifulSoup(resp.text,
                           'html.parser')
    forecasts_yandex = []

    #  Temperature
    day_temps = []
    night_temps = []
    day_temp_strings = []
    night_temp_strings = []
    day_divs = parser.find_all(class_='temp forecast-briefly__temp forecast-briefly__temp_day')
    for i in range(4, 4 + days_count):
        day_temp_strings.append(day_divs[i].contents[1].text)
    for day_temp_string in day_temp_strings:
        day_temps.append(int(day_temp_string[1:]))
    night_divs = parser.find_all(class_='temp forecast-briefly__temp forecast-briefly__temp_night')
    for i in range(4, 4 + days_count):
        night_temp_strings.append(night_divs[i].contents[1].text)
    for night_temp_string in night_temp_strings:
        night_temps.append(int(night_temp_string[1:]))

    #  Shorcast
    shortcast_divs = parser.find_all(class_='forecast-briefly__condition')
    shortcasts = []
    for i in range(4, 4 + days_count):
        shortcasts.append(shortcast_divs[i].text)

    for i in range(days_count):
        date = {}
        date['day_of_week'] = days_of_week[i]
        date['day'] = {}
        date['day']['shortcast'] = shortcasts[i]
        date['day']['temp'] = day_temps[i]
        date['night'] = {}
        date['night']['shortcast'] = shortcasts[i]
        date['night']['temp'] = night_temps[i]
        forecasts_yandex.append(date)

    return forecasts_yandex
