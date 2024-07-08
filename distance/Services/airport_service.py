import httpx, re
from asgiref.sync import sync_to_async
from ..models import Airport


def ValidateIataCode(iata):
    if len(iata) != 3 or not re.match(r'^[A-Za-z]{3}$', iata):
        raise ValueError('IATA code must be provided.')


class AirportService:
    def __init__(self):
        pass

    async def GetAirportData(self, iata):
        ValidateIataCode(iata)
        iata = iata.upper()
        airport = await self.get_airport_from_db(iata)
        if airport:
            return airport

        async with httpx.AsyncClient() as client:
            response = await client.get(f"https://places-dev.cteleport.com/airports/{iata}")
            if response.status_code == 200:
                airport_data = response.json()
                airport = await self.save_airport_to_db(airport_data)
                return airport
            else:
                raise ValueError("Airport not found")

    @sync_to_async
    def get_airport_from_db(self, iata):
        try:
            airport = Airport.objects.get(iata=iata)
            return airport
        except Airport.DoesNotExist:
            return None

    @sync_to_async
    def save_airport_to_db(self, data):
        airport = Airport.objects.create(
            iata=data['iata'],
            name=data['name'],
            country=data['country'],
            city=data['city'],
            latitude=data['location']['lat'],
            longitude=data['location']['lon']
        )
        return airport
