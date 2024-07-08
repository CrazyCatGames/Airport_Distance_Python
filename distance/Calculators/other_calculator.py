from .base_calculator import BaseCalculator


class OtherCalculator(BaseCalculator):
    def CalculateDistance(self, latitude1, longitude1, latitude2, longitude2):
        return {'error': 'Calculator not implemented'}
