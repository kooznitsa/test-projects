from datetime import datetime
from django.shortcuts import render
from django.db.models import Q
from django.http import HttpRequest, HttpResponse

from .models import Containers
from .utils import paginate_flights, get_stats, SORT_OPTIONS, DEFAULT_SORT, PAGES_NUM


def flights(request: HttpRequest) -> HttpResponse:
    all_flights = Containers.objects.distinct()
    if onward_only := request.GET.get('onward_only'):
        all_flights = all_flights.filter(itineraries__flights__itinerary_count__priced_itinerary=onward_only)

    sort = request.GET.get('sort', DEFAULT_SORT)
    containers = all_flights.order_by(SORT_OPTIONS[sort]['key'])

    containers, custom_range = paginate_flights(request, containers, PAGES_NUM)

    context = {
        'containers': containers,
        'sort_options': SORT_OPTIONS,
        'custom_range': custom_range,
    }

    return render(request, 'flights/flights.html', context)


def best_options(request: HttpRequest) -> HttpResponse:
    """Best flights criteria:
    - direct flights or
    - total adult price less than SGD 450 or
    - total flight time less than 550 min
    """

    MAX_PRICE = 450
    MAX_FLIGHT_TIME = 550

    best_options = Containers.objects.filter(
        Q(itineraries__flights__itinerary_count__priced_itinerary=1)
        & (Q(itineraries__flights__direct_flight=True)
        | Q(itineraries__flights__itinerary_count__container_count__adult_price__lte=MAX_PRICE)
        | Q(itineraries__flights__itinerary_count__total_flight_time__lte=MAX_FLIGHT_TIME))
    ).distinct()

    best_options, custom_range = paginate_flights(request, best_options, PAGES_NUM)

    context = {
        'best_options': best_options,
        'custom_range': custom_range,
        'max_price': MAX_PRICE,
        'max_flight_time': MAX_FLIGHT_TIME,
    }

    return render(request, 'flights/best_options.html', context)


def stats(request: HttpRequest) -> HttpResponse:
    req_time_1 = datetime(2015, 9, 28, 20, 23, 49)
    req_time_2 = datetime(2015, 9, 28, 20, 30, 19)

    context = {'req_time_1': req_time_1, 'req_time_2': req_time_2}

    context['total_itineraries_1'],\
    context['direct_num_1'],\
    context['avg_price_1'],\
    context['avg_flight_time_1'] = get_stats(req_time_1)

    context['total_itineraries_2'],\
    context['direct_num_2'],\
    context['avg_price_2'],\
    context['avg_flight_time_2'] = get_stats(req_time_2)

    return render(request, 'flights/stats.html', context)