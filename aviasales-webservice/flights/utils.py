from django.db.models import Avg, Count, Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from .models import Flights


SORT_OPTIONS = {
    'price_asc': {
        'view': 'price ↑',
        'key': 'itinerary_count__container_count__adult_price'
    },
    'price_desc': {
        'view': 'price ↓',
        'key': '-itinerary_count__container_count__adult_price'
    },
    'flight_time_asc': {
        'view': 'flight time ↑',
        'key': 'itinerary_count__total_flight_time'
    },
    'flight_time_desc': {
        'view': 'flight time ↓',
        'key': '-itinerary_count__total_flight_time'
    },
}

DEFAULT_SORT = 'price_asc'
PAGES_NUM = 12


def paginate_flights(request, flights, results):
    page = request.GET.get('page')
    paginator = Paginator(flights, results)

    try:
        flights = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        flights = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        flights = paginator.page(page)

    left_index = (int(page) - 4)
    if left_index < 1:
        left_index = 1

    right_index = (int(page) + 5)
    if right_index > paginator.num_pages:
        right_index = paginator.num_pages + 1

    custom_range = range(left_index, right_index)
    
    return flights, custom_range


def get_stats(date):
    req = Flights.objects.filter(itinerary_count__container_count__request_time=date)
    total_itineraries = req.aggregate(Count('itinerary_count'))

    direct_num = req.filter(
        (Q(source_id__city='DXB') and Q(destination_id__city='BKK'))
        | (Q(source_id__city='BKK') and Q(destination_id__city='DXB'))
    ).aggregate(Count('id'))

    avg_price = req.aggregate(Avg('itinerary_count__container_count__adult_price'))
    avg_flight_time = req.aggregate(Avg('itinerary_count__total_flight_time'))

    return total_itineraries, direct_num, avg_price, avg_flight_time