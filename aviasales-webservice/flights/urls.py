from django.urls import path

from . import views


urlpatterns = [
    path('', views.flights, name='flights'),
    path('stats', views.stats, name='stats'),
    path('best-options', views.best_options, name='best_options'),
]