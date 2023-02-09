import re
from datetime import datetime
import xml.etree.ElementTree as ET
from collections import defaultdict
from django.utils import timezone

from flights.models import (Carriers, Cities, Classes, Containers, 
                            Currencies, Flights, Itineraries, 
                            PricedItineraries, TicketTypes)


class Database:
    def __init__(self, file: str) -> None:
        self.file = file

    def convert_request_date(self, string: str) -> datetime:
        pattern = '%d-%m-%Y %H:%M:%S'
        return datetime.strptime(string, pattern)

    def convert_flight_date(self, d1: str, d2: str) -> tuple[datetime, datetime, int]:
        pattern = '%Y-%m-%dT%H%M'
        departure_time = datetime.strptime(d1, pattern)
        arrival_time = datetime.strptime(d2, pattern)
        flight_time = int((arrival_time - departure_time).total_seconds() // 60)
        return departure_time, arrival_time, flight_time

    def from_camel_case(self, string: str) -> str:
        return re.sub(r'([A-Z])', r' \1', string).lower().strip()
    
    def get_prices(self, el: ET.Element) -> list:
        price_types = ('SingleAdult', 'SingleChild', 'SingleInfant')
        prices_dict = defaultdict.fromkeys(price_types, None)
        for price in el.findall('ServiceCharges'):
            if price.attrib['ChargeType'] == 'TotalAmount':
                prices_dict[price.get('type')] = float(price.text)
        return [prices_dict[k] for k in price_types]
    
    def parse_xml(self, 
                  container_count: list[int] = [0], 
                  itinerary_count: list[int] = [0]) -> None:
        root = ET.parse(self.file).getroot()
        
        request_time = self.convert_request_date(root.attrib['RequestTime'])

        wrappers = root.find('PricedItineraries')
        for wrapper in wrappers.findall('Flights'):
            container_count[0] += 1

            pricing = wrapper.find('Pricing')

            currency, _ = Currencies.objects.update_or_create(
                currency=pricing.attrib['currency'],
            )
            adult_price, child_price, infant_price = self.get_prices(pricing)

            container, _ = Containers.objects.update_or_create(
                container_count=container_count[0],
                defaults={
                    'request_time': request_time,
                    'adult_price': adult_price,
                    'child_price': child_price,
                    'infant_price': infant_price,
                    'currency': currency,
                }
            )
            
            for route in wrapper:
                if route.tag in ('OnwardPricedItinerary', 'ReturnPricedItinerary'):
                    itinerary_count[0] += 1
                    total_flight_time = 0

                    priced_itinerary, _ = PricedItineraries.objects.update_or_create(
                        priced_itinerary=self.from_camel_case(route.tag),
                    )

                    itinerary, _ = Itineraries.objects.update_or_create(
                        itinerary_count=itinerary_count[0],
                        defaults={
                            'container_count': container,
                            'total_flight_time': total_flight_time,
                            'priced_itinerary': priced_itinerary,
                        }
                    )

                    for idx, f in enumerate(route.iter('Flight'), 1):
                        carrier, _ = Carriers.objects.update_or_create(
                            carrier=f.find('Carrier').text
                        )
                        class_field, _ = Classes.objects.update_or_create(
                            class_field=f.find('Class').text
                        )
                        ticket_type, _ = TicketTypes.objects.update_or_create(
                            ticket_type=f.find('TicketType').text
                        )

                        source_city = f.find('Source').text
                        destination_city = f.find('Destination').text
                        direct_flight = (source_city == 'DXB' and destination_city == 'BKK') \
                                    or (source_city == 'BKK' and destination_city == 'DXB')

                        source, _ = Cities.objects.update_or_create(
                            city=source_city
                        )
                        destination, _ = Cities.objects.update_or_create(
                            city=destination_city
                        )

                        departure_time, arrival_time, flight_time = self.convert_flight_date(
                            f.find('DepartureTimeStamp').text, 
                            f.find('ArrivalTimeStamp').text
                        )

                        total_flight_time += flight_time
                        Itineraries.objects.filter(id=itinerary.id).update(
                                total_flight_time=total_flight_time)

                        flight = Flights.objects.create(
                            itinerary_count=itinerary,
                            flight_part=idx,
                            direct_flight=direct_flight,
                            carrier=carrier,
                            flight_num=int(f.find('FlightNumber').text),
                            source=source,
                            destination=destination,
                            departure_time=departure_time,
                            arrival_time=arrival_time,
                            flight_time=flight_time,
                            class_field=class_field,
                            num_stops=int(f.find('NumberOfStops').text),
                            ticket_type=ticket_type,
                            created=timezone.now(),
                        )
        return