"""
Fixtures communes pour les tests du projet NouvelAir.

Ce fichier centralise toutes les fixtures partagees entre les differents
modules de test (unitaires, integration, API, e2e).

Utilisation :
    pytest                        # execute tous les tests
    pytest -m unit                # execute uniquement les tests unitaires
    pytest -m integration         # execute uniquement les tests d'integration
    pytest --cov=. --cov-report=html
"""

import pytest
from datetime import date, timedelta
from django.utils import timezone
from django.test import Client
from django.contrib.auth.models import User
from accounts.models import UserProfile
from flights.models import Airport, Aircraft, Flight
from bookings.models import Booking, Passenger, Payment


# ====================================================================
# Enregistrement des marqueurs pytest
# ====================================================================


def pytest_configure(config):
    """Enregistre les marqueurs personnalises pour les tests."""
    config.addinivalue_line(
        "markers", "unit: tests unitaires (modeles, formulaires, utils)"
    )
    config.addinivalue_line(
        "markers", "integration: tests d'integration (vues, workflows)"
    )
    config.addinivalue_line(
        "markers", "api: tests API (endpoints, requetes HTTP)"
    )


# ====================================================================
# Fixtures de base - base de donnees
# ====================================================================





@pytest.fixture(scope='session', autouse=True)
def _disconnect_userprofile_signal(django_db_setup, django_db_blocker):
    """
    Disconnect UserProfile post_save signal for the entire test session.

    This prevents UNIQUE constraint conflicts when tests (or factories)
    also create a UserProfile for the same user, because the signal
    auto-creates one on User post_save.

    The signal is reconnected after all tests complete.
    """
    with django_db_blocker.unblock():
        disconnected = False
        try:
            from django.db.models.signals import post_save
            from django.contrib.auth import get_user_model
            User = get_user_model()

            candidates = [
                'accounts.signals',
                'nouvelair.accounts.signals',
                'accounts.models',
                'nouvelair.accounts.models',
            ]
            for module_path in candidates:
                try:
                    mod = __import__(module_path, fromlist=['create_user_profile'])
                    handler = getattr(mod, 'create_user_profile', None)
                    if handler:
                        post_save.disconnect(
                            receiver=handler,
                            sender=User,
                            dispatch_uid='create_user_profile',
                        )
                        disconnected = True
                        break
                except (ImportError, AttributeError):
                    continue

            if not disconnected:
                try:
                    post_save.disconnect(
                        sender=User,
                        dispatch_uid='create_user_profile',
                    )
                except Exception:
                    pass
        except Exception:
            pass

    yield

    # Reconnect after session
    with django_db_blocker.unblock():
        try:
            from django.db.models.signals import post_save
            from django.contrib.auth import get_user_model
            User = get_user_model()

            for module_path in [
                'accounts.signals',
                'nouvelair.accounts.signals',
                'accounts.models',
                'nouvelair.accounts.models',
            ]:
                try:
                    mod = __import__(
                        module_path, fromlist=['create_user_profile']
                    )
                    handler = getattr(mod, 'create_user_profile', None)
                    if handler:
                        post_save.connect(
                            receiver=handler,
                            sender=User,
                            dispatch_uid='create_user_profile',
                        )
                        break
                except (ImportError, AttributeError):
                    continue
        except Exception:
            pass


@pytest.fixture(scope="function")
def db_fixture(db):
    """
    Fournit un acces direct a la base de donnees de test.
    Alias court pour le fixture 'db' de pytest-django.
    """
    return db


# ====================================================================
# Fixtures d'authentification
# ====================================================================


@pytest.fixture
def authenticated_client(db):
    """
    Cree un utilisateur de test avec un profil complet et retourne
    un client Django deja authentifie.

    Returns:
        django.test.Client: Client authentifie avec session active.
    """
    user = User.objects.create_user(
        username="testuser",
        email="test@nouvelair.com",
        password="SecurePass123!",
        first_name="Ahmed",
        last_name="Ben Ali",
    )
    profile, _ = UserProfile.objects.get_or_create(
        user=user,
        defaults={
            "phone": "+216 22 345 678",
            "city": "Tunis",
            "country": "Tunisie",
            "nationality": "Tunisienne",
            "date_of_birth": date(1990, 5, 15),
            "gender": "M",
            "newsletter": True,
        }
    )
    client = Client()
    client.login(username="testuser", password="SecurePass123!")
    return client


# ====================================================================
# Fixtures de donnees de reference - Aeroports
# ====================================================================


@pytest.fixture
def sample_airport(db):
    """
    Cree l'aeroport de Tunis-Carthage (TUN).

    Returns:
        Airport: Instance de l'aeroport TUN.
    """
    airport, _ = Airport.objects.get_or_create(
        code="TUN",
        defaults={
            "name": "Aeroport International Tunis-Carthage",
            "city": "Tunis",
            "country": "Tunisie",
            "latitude": 36.851000,
            "longitude": 10.227000,
            "is_active": True,
        },
    )
    return airport


@pytest.fixture
def sample_airport_paris(db):
    """
    Cree l'aeroport de Paris-Charles de Gaulle (CDG).

    Returns:
        Airport: Instance de l'aeroport CDG.
    """
    return Airport.objects.create(
        code="CDG",
        name="Aeroport de Paris-Charles de Gaulle",
        city="Paris",
        country="France",
        latitude=49.009700,
        longitude=2.547900,
        is_active=True,
    )


# ====================================================================
# Fixtures de donnees de reference - Aeronefs
# ====================================================================


@pytest.fixture
def sample_aircraft(db):
    """
    Cree un aeronef Airbus A320neo.

    Returns:
        Aircraft: Instance de l'aeronef A320neo.
    """
    return Aircraft.objects.create(
        model_name="Airbus A320neo",
        registration="TS-INA",
        total_seats=180,
        economy_seats=150,
        business_seats=30,
        is_active=True,
    )


# ====================================================================
# Fixtures de donnees de reference - Vols
# ====================================================================


@pytest.fixture
def sample_flight(db, sample_airport, sample_airport_paris, sample_aircraft):
    """
    Cree un vol programme TUN -> CDG avec un depart dans 5 jours.

    Returns:
        Flight: Instance du vol programme.
    """
    now = timezone.now()
    departure = now + timedelta(days=5, hours=8, minutes=30)
    arrival = now + timedelta(days=5, hours=11, minutes=15)

    return Flight.objects.create(
        flight_number="BJ520",
        origin=sample_airport,
        destination=sample_airport_paris,
        aircraft=sample_aircraft,
        departure_time=departure,
        arrival_time=arrival,
        status="scheduled",
        base_price_economy=350.00,
        base_price_business=1200.00,
        available_seats_economy=150,
        available_seats_business=30,
        is_active=True,
    )


# ====================================================================
# Fixtures de donnees de reference - Reservations
# ====================================================================


@pytest.fixture
def sample_booking(db, sample_flight, authenticated_client):
    """
    Cree une reservation en attente (pending) pour le vol TUN -> CDG.

    Returns:
        Booking: Instance de la reservation creee.
    """
    user = User.objects.get(username="testuser")

    booking = Booking.objects.create(
        user=user,
        contact_email="test@nouvelair.com",
        contact_phone="+216 22 345 678",
        status="pending",
        total_amount=350.00,
        special_requests="Siege cote hublot",
    )
    return booking


# ====================================================================
# Fixtures utilitaires
# ====================================================================


@pytest.fixture
def api_client(db):
    """
    Fournit un client de test Django pour les requetes API.

    Returns:
        django.test.Client: Client de test non authentifie.
    """
    return Client()


@pytest.fixture
def future_date():
    """
    Retourne une date future (5 jours a partir d'aujourd'hui).

    Returns:
        datetime.date: Date dans 5 jours.
    """
    return date.today() + timedelta(days=5)
