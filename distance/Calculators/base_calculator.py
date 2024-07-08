from abc import ABC, abstractmethod


class BaseCalculator(ABC):
    @abstractmethod
    def CalculateDistance(self, latitude1, longitude1, latitude2, longitude2):
        pass
