from datetime import datetime
from django.db.models import Avg, Count, Q
from django.core.paginator import Paginator, EmptyPage
from django.http import HttpRequest
from django.db.models.query import QuerySet

from .models import Flights, Containers


SORT_OPTIONS = {
    'price_asc': {
        'view': 'price ↑',
        'key': 'adult_price'
    },
    'price_desc': {
        'view': 'price ↓',
        'key': '-adult_price'
    },
    'flight_time_asc': {
        'view': 'flight time ↑',
        'key': 'itineraries__flights__itinerary_count__total_flight_time'
    },
    'flight_time_desc': {
        'view': 'flight time ↓',
        'key': '-itineraries__flights__itinerary_count__total_flight_time'
    },
}

DEFAULT_SORT = 'price_asc'
PER_PAGE = 3


def paginate_objects(request: HttpRequest, 
                    objects: QuerySet[Containers], 
                    per_page: int) -> QuerySet[Containers]:
    page = int(request.GET.get('page', 1))
    paginator = Paginator(objects, per_page)

    try:
        objects = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        objects = paginator.page(page)

    return objects


def get_stats(date: datetime) -> tuple[int, int, float, float]:
    req = Flights.objects.filter(itinerary_count__container_count__request_time=date)
    total_itineraries = req.aggregate(Count('itinerary_count'))

    direct_num = req.filter(
        (Q(source_id__city='DXB') and Q(destination_id__city='BKK'))
        | (Q(source_id__city='BKK') and Q(destination_id__city='DXB'))
    ).aggregate(Count('id'))

    avg_price = req.aggregate(Avg('itinerary_count__container_count__adult_price'))
    avg_flight_time = req.aggregate(Avg('itinerary_count__total_flight_time'))

    return total_itineraries, direct_num, avg_price, avg_flight_time