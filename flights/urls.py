"""
Configuration des URLs pour l'application Flights.
"""

from django.urls import path
from . import views

app_name = 'flights'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('recherche/', views.FlightSearchResultsView.as_view(), name='search_results'),
    path('vol/<str:flight_number>/', views.FlightDetailView.as_view(), name='flight_detail'),
    path('aeroports/', views.AirportListView.as_view(), name='airport_list'),
    path('api/airports/autocomplete/', views.airport_autocomplete, name='airport_autocomplete'),
]
