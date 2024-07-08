Это усовершенствованный код предыдущей версии, которая состояла из одного файла (не включая базовые файлы Django)

Первая версия:
```Python
from django.http import JsonResponse
from django.views.decorators.http import require_GET
import requests
from math import radians, cos, sin, sqrt, atan2


@require_GET
def calculate_distance(request):
    try:
        iata1 = request.GET.get('iata1')
        iata2 = request.GET.get('iata2')
        if not iata1 or not iata2:
            return JsonResponse({'error': 'Please provide both iata1 and iata2 parameters'},
                                status=400)

        airport1 = get_airport_details(iata1)
        airport2 = get_airport_details(iata2)

        if 'error' in airport1:
            return JsonResponse(
                {'error': f"Unable to retrieve airport data for {iata1}: {airport1['error']}"},
                status=400)
        if 'error' in airport2:
            return JsonResponse(
                {'error': f"Unable to retrieve airport data for {iata2}: {airport2['error']}"},
                status=400)

        lat1, lon1 = airport1['location']['lat'], airport1['location']['lon']
        lat2, lon2 = airport2['location']['lat'], airport2['location']['lon']

        distance = haversine_distance(lat1, lon1, lat2, lon2)

        response_data = {
            'airport1': {
                'iata': iata1,
                'city': airport1['city'],
                'country': airport1['country'],
                'location': {'lat': lat1, 'lon': lon1},
            },
            'airport2': {
                'iata': iata2,
                'city': airport2['city'],
                'country': airport2['country'],
                'location': {'lat': lat2, 'lon': lon2},
            },
            'distance_meters': distance
        }

        return JsonResponse(response_data, status=200)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


def get_airport_details(iata_code):
    url = f'https://places-dev.cteleport.com/airports/{iata_code}'
    response = requests.get(url)

    if response.status_code == 200:
        return response.json()
    else:
        return {'error': 'Unable to fetch data'}


def haversine_distance(lat1, lon1, lat2, lon2):
    Radius_of_Earth = 6371000

    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = Radius_of_Earth * c
    return int(distance)
```