import re
from datetime import datetime
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import xml.etree.ElementTree as ET
from collections import defaultdict
from typing import Any, Optional, Type
from typing_extensions import Literal
from types import TracebackType

from confidential import DATABASE_CONNECTION


class Containers: pass
class Itineraries: pass
class Flights: pass


class Data:
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

    def parse_xml(self) -> list[dict[str, Optional[Any]]]:
        """Separate flight parts go to the Flights class.
        Common flights on the same itinerary go to the Itineraries class.
        Itineraries go to the Containers.
        Everything is returned in a list of dictionaries.
        """
        data = []

        root = ET.parse(self.file).getroot()

        request_time = self.convert_request_date(root.attrib['RequestTime'])

        wrappers = root.find('PricedItineraries')
        for containers in wrappers.findall('Flights'):
            c = Containers()
            c.request_time = request_time

            for itinerary in containers:
                if itinerary.tag in ('OnwardPricedItinerary', 'ReturnPricedItinerary'):
                    it = Itineraries()
                    it.priced_itinerary = self.from_camel_case(itinerary.tag)
                    it.total_flight_time = 0
                    c.__dict__.setdefault('itineraries', []).append(it.__dict__)

                    for idx, flight in enumerate(itinerary.iter('Flight'), 1):
                        f = Flights()
                        f.flight_part = idx
                        f.carrier = flight.find('Carrier').text
                        f.flight_num = int(flight.find('FlightNumber').text)
                        f.source = flight.find('Source').text
                        f.destination = flight.find('Destination').text
                        f.direct_flight = True 

                        direct_filter = (f.source == 'DXB' and f.destination == 'BKK') \
                                or (f.destination == 'DXB' and f.source == 'BKK')
                        f.direct_flight = True if direct_filter else False

                        f.departure_time, f.arrival_time, f.flight_time = self.convert_flight_date(
                            flight.find('DepartureTimeStamp').text, 
                            flight.find('ArrivalTimeStamp').text
                        )
                        it.total_flight_time += f.flight_time
                        f.class_field = flight.find('Class').text
                        f.num_stops = int(flight.find('NumberOfStops').text)
                        f.ticket_type = flight.find('TicketType').text
                        f.created = datetime.now()

                        it.__dict__.setdefault('flights', []).append(f.__dict__)

                elif itinerary.tag == 'Pricing':
                    c.currency = itinerary.attrib['currency']
                    price_types = ('SingleAdult', 'SingleChild', 'SingleInfant')
                    prices = defaultdict.fromkeys(price_types, None)
                    for price in itinerary.findall('ServiceCharges'):
                        if price.attrib['ChargeType'] == 'TotalAmount':
                            prices[price.get('type')] = float(price.text)
                    c.adult_price, c.child_price, c.infant_price = [prices[k] for k in price_types]

                    data.append(c.__dict__)
        return data
        

class Connection:  
    def __init__(self) -> None:
        self.connection = psycopg2.connect(**DATABASE_CONNECTION)
        self.connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        self.cursor = self.connection.cursor()
        print('CONNECTION ESTABLISHED')

    def __enter__(self) -> psycopg2.extensions.cursor:
        return self.cursor

    def __exit__(self, exc_type: Optional[Type[BaseException]], 
                exc_val: Optional[BaseException], 
                exc_tb: Optional[TracebackType]) -> Literal[False]:
        if exc_type and exc_val:
            self.connection.rollback()
        self.cursor.close()
        self.connection.close()
        print('CONNECTION CLOSED')
        return False


class Database:
    def __init__(self, data: dict) -> None:
        self.data = data
        self.num = 0

    def template(self, 
                table_name: str, 
                col_name: str, 
                var_name: Optional[str] = None) -> str:
        self.num += 1
        if var_name is None:
            var_name = col_name
        return f"""
            ins{self.num} AS (
                INSERT INTO {table_name} ({col_name})
                VALUES (%s)
                ON CONFLICT ({col_name}) DO UPDATE
                SET {col_name} = excluded.{col_name}
                RETURNING id AS {var_name}_id
            ),
        """

    def write_to_db(self, 
                    container_count: list = [0], 
                    itinerary_count: list = [0]) -> None:
        with Connection() as cursor:
            query = 'WITH' \
                + self.template('priced_itineraries', 'priced_itinerary') \
                + self.template('carriers', 'carrier') \
                + self.template('cities', 'city', 'source') \
                + self.template('cities', 'city', 'destination') \
                + self.template('currencies', 'currency') \
                + self.template('classes', 'class_field') \
                + self.template('ticket_types', 'ticket_type') \
                + """
                ins8 AS (INSERT INTO containers (container_count, adult_price, child_price, infant_price, currency_id, request_time)
                    VALUES (%s, %s, %s, %s, (SELECT currency_id FROM ins5), %s)
                    ON CONFLICT (container_count) DO UPDATE
                    SET container_count = excluded.container_count
                    RETURNING container_count as container_count_id
                ),
                ins9 AS (INSERT INTO itineraries (itinerary_count, container_count_id, total_flight_time, priced_itinerary_id)
                    VALUES (%s, (SELECT container_count_id FROM ins8), %s, (SELECT priced_itinerary_id FROM ins1))
                    ON CONFLICT (itinerary_count) DO UPDATE
                    SET itinerary_count = excluded.itinerary_count
                    RETURNING itinerary_count as itinerary_count_id
                )
                INSERT INTO flights (itinerary_count_id, flight_part, direct_flight, carrier_id, flight_num, source_id, destination_id, departure_time, arrival_time, flight_time, class_field_id, num_stops, ticket_type_id, created)
                    VALUES ((SELECT itinerary_count_id FROM ins9), %s, %s, (SELECT carrier_id FROM ins2), %s, (SELECT source_id FROM ins3), (SELECT destination_id FROM ins4), %s, %s, %s, (SELECT class_field_id FROM ins6), %s, (SELECT ticket_type_id FROM ins7), %s);
                """

            for d in self.data:
                adult_price = d['adult_price']
                child_price = d['child_price']
                infant_price = d['infant_price']
                currency = d['currency']
                request_time = d['request_time']
                container_count[0] += 1

                for it in d['itineraries']:
                    total_flight_time = it['total_flight_time']
                    priced_itinerary = it['priced_itinerary']
                    itinerary_count[0] += 1

                    for f in it['flights']:
                        cursor.execute(query, (
                            priced_itinerary,
                            f['carrier'],
                            f['source'],
                            f['destination'],
                            currency,
                            f['class_field'],
                            f['ticket_type'],
                            container_count[0],
                            adult_price,
                            child_price,
                            infant_price,
                            request_time,
                            itinerary_count[0],
                            total_flight_time,
                            f['flight_part'],
                            f['direct_flight'],
                            f['flight_num'],
                            f['departure_time'], 
                            f['arrival_time'], 
                            f['flight_time'],
                            f['num_stops'],
                            f['created'],
                        ))
        print('DATA INSERTED')
        return


if __name__ == '__main__':
    files = ['files/RS_ViaOW.xml', 'files/RS_Via-3.xml',]
    for file in files:
        data = Data(file).parse_xml()
        database = Database(data)
        database.write_to_db()