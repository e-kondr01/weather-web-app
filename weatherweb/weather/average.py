def average(parsed_data):
    average_data = []
    for i in range(len(parsed_data['forecastsYandex'])):
        yandex = parsed_data['forecastsYandex'][i]
        gismeteo = parsed_data['forecastsGismeteo'][i]
        weathercom = parsed_data['forecastsWeatherCom'][i]
        date = {}
        date['day_of_week'] = yandex['day_of_week']
        date['day'] = {}
        date['day']['temp'] = round(1 / 3 * (yandex['day']['temp'] + gismeteo['day']['temp'] +
                                    weathercom['day']['temp']), 1)
        date['night'] = {}
        date['night']['temp'] = round(1 / 3 * (yandex['night']['temp'] + gismeteo['night']['temp'] +
                                      weathercom['night']['temp']), 1)

        average_data.append(date)
    return average_data
