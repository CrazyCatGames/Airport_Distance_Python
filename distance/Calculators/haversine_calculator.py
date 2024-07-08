import math
from .base_calculator import BaseCalculator


class HaversineCalculator(BaseCalculator):
    def CalculateDistance(self, latitude1, longitude1, latitude2, longitude2):
        R = 6378160  # Радиус Земли в метрах
        lat1_rad = math.radians(latitude1)
        lon1_rad = math.radians(longitude1)
        lat2_rad = math.radians(latitude2)
        lon2_rad = math.radians(longitude2)

        dlat = lat2_rad - lat1_rad
        dlon = lon2_rad - lon1_rad

        a = math.sin(dlat / 2) ** 2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(
            dlon / 2) ** 2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

        return R * c
