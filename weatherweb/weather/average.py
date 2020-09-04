def average(parsed_data):
    average_data = {}
    for i in range(len(parsed_data['dates'])):
        daily_temps = {}

        try:
            gismeteo_temps_s = parsed_data['gismeteo_temps'][i * 4 + 1: i * 4 + 5]
        except IndexError:
            gismeteo_temps_s = parsed_data['gismeteo_temps'][i * 4 + 1: i * 4 + 4]
        gismeteo_temps = []
        for temp in gismeteo_temps_s:
            gismeteo_temps.append(int(temp[1:]))

        yandex_temps = []
        yandex_temps_s = parsed_data['yandex_temps'][i * 8: i * 8 + 8]
        for temp in yandex_temps_s:
            yandex_temps.append(int(temp[1:]))

        if len(parsed_data['weathercom_temps']) % 2:
            weathercom_temps = parsed_data['weathercom_temps'][i * 2: i * 2 + 2]
        else:
            if i == 0:
                weathercom_temps = parsed_data['weathercom_temps'][0]
            else:
                weathercom_temps = parsed_data['weathercom_temps'][i * 2 - 1: i * 2 + 1]

        print(yandex_temps)
        print(gismeteo_temps)
        daily_temps['Утро'] = (sum(yandex_temps[0: 2]) + gismeteo_temps[0]) // 3
        if len(weathercom_temps) == 2:
            daily_temps['День'] = (sum(yandex_temps[2: 4]) + gismeteo_temps[1] + weathercom_temps[0]) // 4
            weathercom_temps.pop(0)
        else:
            daily_temps['День'] = (sum(yandex_temps[2: 4]) + gismeteo_temps[1]) // 3
        daily_temps['Вечер'] = (sum(yandex_temps[4: 6]) + gismeteo_temps[2]) // 3
        if len(gismeteo_temps) == 4:
            daily_temps['Ночь'] = (sum(yandex_temps[6: 8]) + gismeteo_temps[3] + weathercom_temps[0]) // 4
        else:
            daily_temps['Ночь'] = (sum(yandex_temps[6: 8]) + weathercom_temps[0]) // 3

        average_data[parsed_data['dates'][i]] = daily_temps

    return average_data
