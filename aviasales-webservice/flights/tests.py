# from django.test import TestCase
from datetime import datetime

def convert_flight_date(d1: str, d2: str) -> tuple[datetime | float]:
    pattern = '%Y-%m-%dT%H%M'
    departure_time = datetime.strptime(d1, pattern)
    arrival_time = datetime.strptime(d2, pattern)
    hours = (arrival_time - departure_time).total_seconds() / 3600
    minutes = (arrival_time - departure_time).total_seconds() / 60
    return hours, minutes


print(convert_flight_date('2018-10-27T0005', '2018-10-27T0445'))