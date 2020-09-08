def average(parsed_data):
    average_data = []
    for i in range(len(parsed_data['forecastsYandex'])):
        yandex = parsed_data['forecastsYandex'][i]
        gismeteo = parsed_data['forecastsGismeteo'][i]
        weathercom = parsed_data['forecastsWeatherCom'][i]

        date = {}
        date['day_of_week'] = yandex['day_of_week']

        date['day'] = {}
        if weathercom['day']['temp'] is None:
            date['day']['temp'] = round(1 / 2 * (yandex['day']['temp'] + gismeteo['day']['temp']), 1)
        else:
            date['day']['temp'] = round(1 / 3 * (yandex['day']['temp'] + gismeteo['day']['temp'] +
                                        weathercom['day']['temp']), 1)
        date['day']['shortcasts'] = []
        date['day']['shortcasts'].append(yandex['day']['shortcast'])
        date['day']['shortcasts'].append(gismeteo['day']['shortcast'])
        date['day']['shortcasts'].append(weathercom['day']['shortcast'])

        date['night'] = {}
        date['night']['temp'] = round(1 / 3 * (yandex['night']['temp'] + gismeteo['night']['temp'] +
                                      weathercom['night']['temp']), 1)
        date['night']['shortcasts'] = []
        date['night']['shortcasts'].append(yandex['night']['shortcast'])
        date['night']['shortcasts'].append(gismeteo['night']['shortcast'])
        date['night']['shortcasts'].append(weathercom['night']['shortcast'])

        average_data.append(date)
    return average_data
