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
    forecasts_weathercom = parse_weathercom(days_count, days_of_week)

    parsed_data = {}
    parsed_data["metadata"] = {
        "status_code": 200,
        "unit": unit}

    parsed_data['forecastsYandex'] = forecasts_yandex
    parsed_data['forecastsGismeteo'] = forecasts_gismeteo
    parsed_data['forecastsWeatherCom'] = forecasts_weathercom
    return parsed_data


def parse_weathercom(days_count, days_of_week):
    headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64 AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36'
        }
    resp = requests.get('https://weather.com/ru-RU/weather/tenday/l/4edb4827c7f66b1542f84ce1d8d644970e9b935d45d21d4d143e87d94925a4bf',
                        headers=headers)
    parser = BeautifulSoup(resp.text,
                           'html.parser')

    #  Temperature

    starts_with_night = False
    temp_spans = parser.find_all(attrs={'data-testid': "TemperatureValue"})
    if len(temp_spans) % 2 != 0:
        starts_with_night = True

    first_temp_spans = parser.find_all(class_="_-_-node_modules-@wxu-components-src-molecule-DaypartDetails-DailyContent-DailyContent--temp--_8DL5")

    high_temp_spans = parser.find_all(class_="_-_-node_modules-@wxu-components-src-molecule-DaypartDetails-DetailsSummary-DetailsSummary--highTempValue--3x6cL")
    if not starts_with_night:
        high_temp_spans.insert(0, first_temp_spans[0])
    high_temp_strings = []
    for i in range(days_count):
        high_temp_strings.append(high_temp_spans[i].string)
    high_temps = []
    for high_temp_string in high_temp_strings:
        high_temps.append(int(high_temp_string[:len(high_temp_string)-1]))
    if starts_with_night:
        high_temps.insert(0, None)

    low_temp_spans = parser.find_all(class_="_-_-node_modules-@wxu-components-src-molecule-DaypartDetails-DetailsSummary-DetailsSummary--lowTempValue--1DlJK")
    if starts_with_night:
        low_temp_spans.insert(0, first_temp_spans[0])
    else:
        low_temp_spans.insert(0, first_temp_spans[1])
    low_temp_strings = []
    for i in range(days_count):
        low_temp_strings.append(low_temp_spans[i].string)
    low_temps = []
    for low_temp_string in low_temp_strings:
        low_temps.append(int(low_temp_string[:len(low_temp_string)-1]))

    #  Shortcast
    shortcast_p = parser.find_all(class_="_-_-node_modules-@wxu-components-src-molecule-DaypartDetails-DailyContent-DailyContent--narrative--3AcXd")
    shortcasts = []
    for i in range(days_count):
        shortcasts.append(shortcast_p[i].text)

    forecasts_weathercom = fill_table(days_count=days_count, days_of_week=days_of_week,
                                      shortcasts=shortcasts, day_temps=high_temps,
                                      night_temps=low_temps)
    return forecasts_weathercom


def parse_gismeteo(days_count):
    headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64 AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36'
        }
    resp = requests.get('https://www.gismeteo.ru/weather-sankt-peterburg-4079/10-days/',
                        headers=headers)
    parser = BeautifulSoup(resp.text,
                           'html.parser')

    #  Temperature
    temp_spans = parser.find_all(class_='unit unit_temperature_c')
    temp_strings = []
    for i in range(days_count * 2):
        temp_strings.append(temp_spans[i].string)
    temps = []
    for temp_string in temp_strings:
        temps.append(int(temp_string[1:]))
    day_temps = []
    night_temps = []
    for i in range(len(temps)):
        if i % 2 == 0:
            day_temps.append(temps[i])
        else:
            night_temps.append(temps[i])

    #  Day of week
    day_divs = parser.find_all(class_='w_date__day')
    days_ru = []
    for i in range(days_count):
        days_ru.append(day_divs[i].string)
    days_of_week = []
    for day in days_ru:
        days_of_week.append(weekdays[day])

    #  Shortcast
    shortcast_spans = parser.find_all(class_='tooltip')
    shortcasts = []
    for i in range(days_count):
        shortcasts.append(shortcast_spans[i]['data-text'])

    forecasts_gismeteo = fill_table(days_count=days_count, days_of_week=days_of_week,
                                    shortcasts=shortcasts, day_temps=day_temps,
                                    night_temps=night_temps)
    return (forecasts_gismeteo, days_of_week)


def parse_yandex(days_count, days_of_week):
    headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64 AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36'
        }
    resp = requests.get('https://yandex.ru/pogoda/saint-petersburg',
                        headers=headers)
    parser = BeautifulSoup(resp.text,
                           'html.parser')

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

    #  Shortcast
    shortcast_divs = parser.find_all(class_='forecast-briefly__condition')
    shortcasts = []
    for i in range(4, 4 + days_count):
        shortcasts.append(shortcast_divs[i].text)

    forecasts_yandex = fill_table(days_count=days_count, days_of_week=days_of_week,
                                  shortcasts=shortcasts, day_temps=day_temps,
                                  night_temps=night_temps)
    return forecasts_yandex


def fill_table(days_count=10, days_of_week=[], shortcasts=[], day_temps=[],
               night_temps=[]):
    forecasts = []
    for i in range(days_count):
        date = {}
        date['day_of_week'] = days_of_week[i]
        date['day'] = {}
        date['day']['shortcast'] = shortcasts[i]
        date['day']['temp'] = day_temps[i]
        date['night'] = {}
        date['night']['shortcast'] = shortcasts[i]
        date['night']['temp'] = night_temps[i]
        forecasts.append(date)

    return forecasts
