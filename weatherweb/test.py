import requests


latitude = 60
longitude = 30
days = 7
yandex_json = requests.get('https://api.weather.yandex.ru/v2/informers',
        headers={'X-Yandex-API-Key': 'c54630e9-d293-44b1-ab1c-3add95fa374c'},
        params={'lat': latitude, 'lon': longitude},
        )
print(yandex_json.request.headers)
print(yandex_json.json())


gismeteo_json = requests.get('https://api.gismeteo.net/v2/weather/forecast',
        params={'latitude': latitude, 'longitude': longitude, 'days': days},
        headers={'X-Gismeteo-Token': '56b30cb255.3443075'})
    
print(gismeteo_json.request.headers)
print(gismeteo_json.json())