from django.db import models


class Carriers(models.Model):
    carrier = models.CharField(unique=True, max_length=100)

    class Meta:
        managed = False
        db_table = 'carriers'


class Cities(models.Model):
    city = models.CharField(unique=True, max_length=100)

    class Meta:
        managed = False
        db_table = 'cities'


class Classes(models.Model):
    class_field = models.CharField(unique=True, max_length=100)

    class Meta:
        managed = False
        db_table = 'classes'


class Currencies(models.Model):
    currency = models.CharField(unique=True, max_length=100)

    class Meta:
        managed = False
        db_table = 'currencies'


class PricedItineraries(models.Model):
    priced_itinerary = models.CharField(unique=True, max_length=100)

    class Meta:
        managed = False
        db_table = 'priced_itineraries'


class TicketTypes(models.Model):
    ticket_type = models.CharField(unique=True, max_length=100)

    class Meta:
        managed = False
        db_table = 'ticket_types'


class Containers(models.Model):
    container_count = models.IntegerField(unique=True)
    adult_price = models.FloatField(blank=True, null=True)
    child_price = models.FloatField(blank=True, null=True)
    infant_price = models.FloatField(blank=True, null=True)
    currency = models.ForeignKey('Currencies', models.DO_NOTHING, blank=True, null=True)
    request_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'containers'


class Itineraries(models.Model):
    itinerary_count = models.IntegerField(unique=True)
    container_count = models.ForeignKey(Containers, models.DO_NOTHING, to_field='container_count')
    total_flight_time = models.IntegerField()
    priced_itinerary = models.ForeignKey('PricedItineraries', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'itineraries'


class Flights(models.Model):
    itinerary_count = models.ForeignKey('Itineraries', models.DO_NOTHING, to_field='itinerary_count')
    flight_part = models.IntegerField()
    direct_flight = models.BooleanField()
    carrier = models.ForeignKey(Carriers, models.DO_NOTHING, blank=True, null=True)
    flight_num = models.IntegerField(blank=True, null=True)
    source = models.ForeignKey(Cities, models.DO_NOTHING, related_name='city_source', blank=True, null=True)
    destination = models.ForeignKey(Cities, models.DO_NOTHING, related_name='city_destination', blank=True, null=True)
    departure_time = models.DateTimeField(blank=True, null=True)
    arrival_time = models.DateTimeField(blank=True, null=True)
    flight_time = models.IntegerField(blank=True, null=True)
    class_field = models.ForeignKey(Classes, models.DO_NOTHING, blank=True, null=True)
    num_stops = models.IntegerField(blank=True, null=True)
    ticket_type = models.ForeignKey('TicketTypes', models.DO_NOTHING, blank=True, null=True)
    created = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'flights'