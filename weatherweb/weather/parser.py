import json


def parser(weathercom_json=None, openweather_json=None, weatherbit_json=None):
    weathercom = parse_weathercom(weathercom_json)
    openweather = parse_openweather(openweather_json)
    weatherbit = parse_weatherbit(weatherbit_json)
    parsed_data = {
        'weathercom': weathercom,
        'openweather': openweather,
        'weatherbit': weatherbit}
    return parsed_data


def parse_weathercom(weathercom):
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


def parse_openweather(openweather):
    return None


def parse_weatherbit(weatherbit):
    return None
