from django.urls import path
from .views import DistanceView

urlpatterns = [
    path('distance_between/', DistanceView.as_view(), name='distance-between'),
]
