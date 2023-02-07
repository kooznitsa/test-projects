from django.urls import path

from . import views
from api.views import (
    CheapestFlightsListAPIView, 
    ExpensiveFlightsListAPIView,
    FastestFlightsListAPIView,
    LongestFlightsListAPIView,
    DirectListAPIView,
)


urlpatterns = [
    path('', views.get_routes),
    path('cheapest-flights', CheapestFlightsListAPIView.as_view()),
    path('expensive-flights', ExpensiveFlightsListAPIView.as_view()),
    path('fastest-flights', FastestFlightsListAPIView.as_view()),
    path('longest-flights', LongestFlightsListAPIView.as_view()),
    path('direct-flights', DirectListAPIView.as_view()),
]