import json
import requests

from bs4 import BeautifulSoup


def parse_weather():
    '''Формат погоды:
    утро -
    день -
    вечер -
    ночь -  '''
    gismeteo = parse_gismeteo()
    dates = gismeteo[1]
    gismeteo_temps = gismeteo[2]
    yandex_temps = parse_yandex()
    weathercom_temps = parse_weathercom()
    parsed_data = {
        'dates': dates,
        'weathercom_temps': weathercom_temps,
        'gismeteo_temps': gismeteo_temps,
        'yandex_temps': yandex_temps}
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
    return temps


def parse_gismeteo():
    headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64 AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36'
        }
    resp = requests.get('https://www.gismeteo.ru/weather-sankt-peterburg-4079/3-days/',
                        headers=headers)
    parser = BeautifulSoup(resp.text,
                           'html.parser')

    temp_spans = parser.find_all(class_='unit unit_temperature_c')
    temps = []
    for span in temp_spans:
        temps.append(span.string)

    day0 = parser.find('div', attrs={'data-index': '0'})
    day0 = day0.a.text

    day1 = parser.find('div', attrs={'data-index': '1'})
    day1 = day1.a.text

    day2 = parser.find('div', attrs={'data-index': '2'})
    day2 = day2.a.text

    #  list
    dates = [day0, day1, day2]

    #  dict
    gismeteo = {}
    days = []
    for i in range(3):
        day = {}
        day['Ночь'] = temps[0 + 4 * i]
        day['Утро'] = temps[1 + 4 * i]
        day['День'] = temps[2 + 4 * i]
        day['Вечер'] = temps[3 + 4 * i]
        days.append(day)

    gismeteo[day0] = days[0]
    gismeteo[day1] = days[1]
    gismeteo[day2] = days[2]

    return (gismeteo, dates, temps)


def parse_yandex():
    '''Формат для температуры - утро, день, вечер, ночь. По два значения температуры
    на промежуток + третье "как ощущается" '''
    headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64 AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36'
        }
    resp = requests.get('https://yandex.ru/pogoda/saint-petersburg/details',
                        headers=headers)
    parser = BeautifulSoup(resp.text,
                           'html.parser')

    temp_spans = parser.find_all(class_='temp__value')
    temps = []
    for i in range(1, len(temp_spans) + 1):
        if i % 3 != 0:
            temps.append(temp_spans[i-1].string)

    return temps


print(parse_weathercom())
