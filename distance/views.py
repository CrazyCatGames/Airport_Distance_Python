import asyncio
from django.http import JsonResponse
from django.views import View
from .Services.airport_service import AirportService
from .Calculators.haversine_calculator import HaversineCalculator


class DistanceView(View):
    async def get(self, request):
        from_iata = request.GET.get('fromIata')
        to_iata = request.GET.get('toIata')

        if not from_iata or not to_iata:
            return JsonResponse({"error": "Both fromIata and toIata must be provided"},
                                status=400)

        airport_service = AirportService()

        try:
            from_airport_task = airport_service.GetAirportData(from_iata)
            to_airport_task = airport_service.GetAirportData(to_iata)

            from_airport, to_airport = await asyncio.gather(from_airport_task, to_airport_task)
        except ValueError as e:
            return JsonResponse({"error": str(e)}, status=400)

        calculator = HaversineCalculator()  # Выбранный калькулятор
        distance = calculator.CalculateDistance(
            from_airport.latitude, from_airport.longitude,
            to_airport.latitude, to_airport.longitude
        )

        return JsonResponse({
            "distance": distance,
            "from_airport": {
                "iata": from_airport.iata,
                "country": from_airport.country,
                "city": from_airport.city,
                "location": {
                    "lat": from_airport.latitude,
                    "lon": from_airport.longitude
                }
            },
            "to_airport": {
                "iata": to_airport.iata,
                "country": to_airport.country,
                "city": to_airport.city,
                "location": {
                    "lat": to_airport.latitude,
                    "lon": to_airport.longitude
                }
            }
        })
