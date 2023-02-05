from datetime import datetime
from django.shortcuts import render

from .models import Flights
from .utils import paginate_flights, get_stats, SORT_OPTIONS, DEFAULT_SORT, PAGES_NUM


def flights(request):
    if onward_only := request.GET.get('onward_only'):
        all_flights = Flights.objects.filter(itinerary_count__priced_itinerary=onward_only)
    else:
        all_flights = Flights.objects.all()

    sort = request.GET.get('sort', DEFAULT_SORT)
    flights = all_flights.order_by(SORT_OPTIONS[sort]['key'], 'itinerary_count')

    flights, custom_range = paginate_flights(request, flights, PAGES_NUM)

    context = {
        'sort_options': SORT_OPTIONS,
        'flights': flights,
        'custom_range': custom_range,
    }

    return render(request, 'flights/flights.html', context)


def stats(request):
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