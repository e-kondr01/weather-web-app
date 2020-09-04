import json
import requests

from bs4 import BeautifulSoup


def parse_weather():
    weathercom = parse_weathercom()
    gismeteo = parse_gismeteo()
    yandex = parse_yandex()
    parsed_data = {
        'weathercom': weathercom,
        'gismeteo': gismeteo,
        'yandex': yandex}
    return parsed_data


def parse_weathercom():
    '''
    forecast = weathercom['forecasts']
    parsed_data = []
    for date in forecast:
        max_temp = date['max_temp']
        min_temp = date['min_temp']
        day = date['fcst_valid_local']
        parsed_data.append({
            'day': day,
            'max_temp': max_temp,
            'min_temp': min_temp,
        }
        )
    return parsed_data
    '''
    return None


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

    '''
    time_of_day_spans = parser.find_all(class_='time_of_day')
    time_of_day = []
    for time in time_of_day_spans:
        time_of_day.append(time.string)
        if len(time_of_day) == 12:
            break
    '''

    day0 = parser.find('div', attrs={'data-index': '0'})
    day0 = day0.a.text

    day1 = parser.find('div', attrs={'data-index': '1'})
    day1 = day1.a.text

    day2 = parser.find('div', attrs={'data-index': '2'})
    day2 = day2.a.text

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

    return gismeteo


def parse_yandex():
    return None


print(parse_gismeteo())
