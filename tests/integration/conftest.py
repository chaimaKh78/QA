"""
conftest.py — Fixtures partagées pour les tests d'intégration.

Toutes les fixtures définies ici sont automatiquement disponibles
dans les fichiers de tests du répertoire tests/integration/.
"""

import pytest
from datetime import date, timedelta

from django.utils import timezone
from django.contrib.auth.models import User
from django.test import Client

from flights.models import Airport, Aircraft, Flight
from accounts.models import UserProfile
from bookings.models import Booking, Passenger, Payment
from destinations.models import Destination, DestinationReview
from promotions.models import Promotion, NewsletterSubscription


# ── Fixtures principales ─────────────────────────────────────────────────────


@pytest.fixture
def setup_db(db):
    """
    Crée les données de test de base via l'ORM Django.

    Retourne un dictionnaire contenant toutes les instances créées :
        airports, aircraft, flights, user, profile,
        airport_tun, airport_par, airport_mar, flight1, flight2
    """
    # --- Aéroports ---
    airport_tun = Airport.objects.create(
        code="TUN",
        name="Aéroport International Tunis-Carthage",
        city="Tunis",
        country="Tunisie",
        latitude=36.851000,
        longitude=10.227000,
        is_active=True,
    )
    airport_par = Airport.objects.create(
        code="CDG",
        name="Aéroport Charles de Gaulle",
        city="Paris",
        country="France",
        latitude=49.009700,
        longitude=2.547900,
        is_active=True,
    )
    airport_mar = Airport.objects.create(
        code="MRS",
        name="Aéroport de Marseille Provence",
        city="Marseille",
        country="France",
        latitude=43.436400,
        longitude=5.215700,
        is_active=True,
    )

    # --- Aéronef ---
    aircraft = Aircraft.objects.create(
        model_name="Airbus A320",
        registration="TS-ABC",
        total_seats=180,
        economy_seats=150,
        business_seats=30,
        is_active=True,
    )

    # --- Vols (dates futures) ---
    now = timezone.now()
    future = now + timedelta(days=7)
    future_return = now + timedelta(days=14)

    flight1 = Flight.objects.create(
        flight_number="BJ101",
        origin=airport_tun,
        destination=airport_par,
        aircraft=aircraft,
        departure_time=future.replace(hour=8, minute=0, second=0, microsecond=0),
        arrival_time=future.replace(hour=11, minute=30, second=0, microsecond=0),
        status="scheduled",
        base_price_economy=250.00,
        base_price_business=600.00,
        available_seats_economy=150,
        available_seats_business=30,
        is_active=True,
    )
    flight2 = Flight.objects.create(
        flight_number="BJ202",
        origin=airport_tun,
        destination=airport_mar,
        aircraft=aircraft,
        departure_time=future.replace(hour=14, minute=0, second=0, microsecond=0),
        arrival_time=future.replace(hour=16, minute=30, second=0, microsecond=0),
        status="scheduled",
        base_price_economy=180.00,
        base_price_business=450.00,
        available_seats_economy=150,
        available_seats_business=30,
        is_active=True,
    )
    # Vol retour (pour recherche aller-retour)
    flight_return = Flight.objects.create(
        flight_number="BJ103",
        origin=airport_par,
        destination=airport_tun,
        aircraft=aircraft,
        departure_time=future_return.replace(hour=12, minute=0, second=0, microsecond=0),
        arrival_time=future_return.replace(hour=15, minute=30, second=0, microsecond=0),
        status="scheduled",
        base_price_economy=230.00,
        base_price_business=550.00,
        available_seats_economy=150,
        available_seats_business=30,
        is_active=True,
    )

    # --- Utilisateur + profil ---
    user = User.objects.create_user(
        username="testuser",
        email="test@example.com",
        password="TestPassword123!",
        first_name="Test",
        last_name="User",
    )
    profile, _ = UserProfile.objects.get_or_create(user=user)

    return {
        "airports": [airport_tun, airport_par, airport_mar],
        "aircraft": aircraft,
        "flights": [flight1, flight2, flight_return],
        "user": user,
        "profile": profile,
        "airport_tun": airport_tun,
        "airport_par": airport_par,
        "airport_mar": airport_mar,
        "flight1": flight1,
        "flight2": flight2,
        "flight_return": flight_return,
    }


@pytest.fixture
def search_form_data(setup_db):
    """
    Retourne un dictionnaire de données POST valides pour FlightSearchForm.

    Utilise les aéroports créés par ``setup_db`` et une date de départ
    correspondant au vol futur BJ101 (TUN → CDG).
    """
    future_date = (date.today() + timedelta(days=7)).strftime("%Y-%m-%d")
    return {
        "trip_type": "oneway",
        "origin": str(setup_db["airport_tun"].pk),
        "destination": str(setup_db["airport_par"].pk),
        "departure_date": future_date,
        "passengers": "1",
        "travel_class": "economy",
    }


@pytest.fixture
def authenticated_client(db, setup_db):
    """
    Retourne un Client Django authentifié en tant que ``testuser``.
    """
    client = Client()
    client.login(username="testuser", password="TestPassword123!")
    return client
