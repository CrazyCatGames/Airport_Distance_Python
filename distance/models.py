from django.db import models


class Airport(models.Model):
    iata = models.CharField(max_length=3, unique=True)
    name = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return f"{self.iata}: {self.name}, {self.country}, {self.city}"
