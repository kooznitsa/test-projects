from django.urls import path

from . import views


urlpatterns = [
    path('', views.populate_database, name='database'),
]