from rest_framework.decorators import api_view
from rest_framework import generics
from rest_framework.response import Response
from django.http import HttpRequest, JsonResponse

from flights.models import Containers
from .serializers import ContainersSerializer


@api_view(['GET'])
def get_routes(request: HttpRequest) -> JsonResponse:
    routes = [
        {'GET': '/api/cheapest-flights'},
        {'GET': '/api/expensive-flights'},
        {'GET': '/api/fastest-flights'},
        {'GET': '/api/longest-flights'},
        {'GET': '/api/direct-flights'},
    ]
    return Response(routes)


class FlightsListAPIView(generics.ListAPIView):
    queryset = Containers.objects.distinct()
    serializer_class = ContainersSerializer

    def __init__(self) -> None:
        self.order_by = 'itineraries__flights__itinerary_count__container_count__adult_price'
        self.num_flights = 10

    def list(self, request: HttpRequest) -> JsonResponse:
        queryset = self.get_queryset().order_by(self.order_by)[:self.num_flights]
        serializer = ContainersSerializer(queryset, many=True)
        return Response(serializer.data)


class CheapestFlightsListAPIView(FlightsListAPIView):
    def __init__(self) -> None:
        super().__init__()
    

class ExpensiveFlightsListAPIView(FlightsListAPIView):
    def __init__(self) -> None:
        super().__init__()
        self.order_by = '-itineraries__flights__itinerary_count__container_count__adult_price'


class FastestFlightsListAPIView(FlightsListAPIView):
    def __init__(self) -> None:
        super().__init__()
        self.order_by = 'itineraries__total_flight_time'


class LongestFlightsListAPIView(FlightsListAPIView):
    def __init__(self) -> None:
        super().__init__()
        self.order_by = '-itineraries__total_flight_time'
    

class DirectListAPIView(generics.ListAPIView):
    queryset = Containers.objects.filter(
        itineraries__flights__direct_flight=True
    ).order_by('itineraries__flights__itinerary_count__container_count__adult_price')
    serializer_class = ContainersSerializer