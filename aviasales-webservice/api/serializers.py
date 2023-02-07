from rest_framework import serializers
from rest_framework.utils.serializer_helpers import ReturnList

from flights.models import Flights, Itineraries, Containers


class FlightsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flights
        fields = '__all__'
        depth=3


class ItinerariesSerializer(serializers.ModelSerializer):
    flights = serializers.SerializerMethodField()

    def get_flights(self, obj: Itineraries) -> ReturnList:
        flights = obj.flights_set.all()
        serializer = FlightsSerializer(flights, many=True)
        return serializer.data

    class Meta:
        model = Itineraries
        fields = '__all__'
        depth=3


class ContainersSerializer(serializers.ModelSerializer):
    itineraries = serializers.SerializerMethodField()

    def get_itineraries(self, obj: Containers) -> ReturnList:
        itineraries = obj.itineraries_set.all()
        serializer = ItinerariesSerializer(itineraries, many=True)
        print(type(serializer.data))
        return serializer.data

    class Meta:
        model = Containers
        fields = '__all__'
        depth=3