"""
Application Flights - Gestion des vols et aéroports.
"""
from django.apps import AppConfig


class FlightsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'flights'
    verbose_name = 'Vols'
