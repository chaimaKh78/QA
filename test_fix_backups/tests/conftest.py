"""
Fixtures communes pour les tests du projet NouvelAir.

Ce fichier centralise toutes les fixtures partagées entre les différents
modules de test (unitaires, intégration, API, e2e).

Utilisation :
    pytest                        # exécute tous les tests
    pytest -m unit                # exécute uniquement les tests unitaires
    pytest -m integration         # exécute uniquement les tests d'intégration
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
# Fixtures de base — base de données
# ====================================================================


# =====================================================================
# Disconnect UserProfile auto-creation signal to avoid UNIQUE constraint
# conflicts when tests create UserProfile manually or via factories.
# =====================================================================
@pytest.fixture(scope='session', autouse=True)
def _disconnect_userprofile_signal(django_db_setup, django_db_blocker):
    """Disconnect UserProfile post_save signal for the entire test session."""
    with django_db_blocker.unblock():
        try:
            from django.contrib.auth import get_user_model
            User = get_user_model()
            # Try all common signal locations
            for module_path in [
                'nouvelair.accounts.signals',
                'accounts.signals',
                'nouvelair.accounts.models',
                'accounts.models',
            ]:
                try:
                    signals_module = __import__(module_path, fromlist=['create_user_profile'])
                    if hasattr(signals_module, 'create_user_profile'):
                        from django.db.models.signals import post_save
                        post_save.disconnect(
                            receiver=signals_module.create_user_profile,
                            sender=User,
                            dispatch_uid='create_user_profile',
                        )
                        break
                except (ImportError, AttributeError):
                    continue
        except Exception:
            pass

    yield

    # Reconnect after all tests
    with django_db_blocker.unblock():
        try:
            from django.contrib.auth import get_user_model
            User = get_user_model()
            for module_path in [
                'nouvelair.accounts.signals',
                'accounts.signals',
                'nouvelair.accounts.models',
                'accounts.models',
            ]:
                try:
                    signals_module = __import__(module_path, fromlist=['create_user_profile'])
                    if hasattr(signals_module, 'create_user_profile'):
                        from django.db.models.signals import post_save
                        post_save.connect(
                            receiver=signals_module.create_user_profile,
                            sender=User,
                            dispatch_uid='create_user_profile',
                        )
                        break
                except (ImportError, AttributeError):
                    continue
        except Exception:
            pass

@pytest.fixture(scope="session")
def django_db_setup():
    """
    Configuration de la base de données de test.
    Utilise la base SQLite en mémoire pour des performances optimales.
    """
    pass


@pytest.fixture(scope="function")
def db_fixture(db):
    """
    Fournit un accès direct à la base de données de test.
    La base est vidée et recréée pour chaque fonction de test.
    Alias court pour le fixture 'db' de pytest-django.
    """
    return db


# ====================================================================
# Fixtures d'authentification
# ====================================================================

@pytest.fixture
def authenticated_client(db):
    """
    Crée un utilisateur de test avec un profil complet et retourne
    un client Django déjà authentifié.

    Returns:
        django.test.Client: Client authentifié avec session active.
    """
    # Création de l'utilisateur Django
    user = User.objects.create_user(
        username="testuser",
        email="test@nouvelair.com",
        password="SecurePass123!",
        first_name="Ahmed",
        last_name="Ben Ali",
    )
    # Création du profil utilisateur associé
    UserProfile.objects.create(
        user=user,
        phone="+216 22 345 678",
        city="Tunis",
        country="Tunisie",
        nationality="Tunisienne",
        date_of_birth=date(1990, 5, 15),
        gender="M",
        newsletter=True,
    )
    # Authentification du client de test
    client = Client()
    client.login(username="testuser", password="SecurePass123!")
    return client


# ====================================================================
# Fixtures de données de référence — Aéroports
# ====================================================================

@pytest.fixture
def sample_airport(db):
    """
    Crée l'aéroport de Tunis-Carthage (TUN).

    Returns:
        Airport: Instance de l'aéroport TUN.
    """
    return Airport.objects.create(
        code="TUN",
        name="Aéroport International Tunis-Carthage",
        city="Tunis",
        country="Tunisie",
        latitude=36.851000,
        longitude=10.227000,
        is_active=True,
    )


@pytest.fixture
def sample_airport_paris(db):
    """
    Crée l'aéroport de Paris-Charles de Gaulle (CDG).

    Returns:
        Airport: Instance de l'aéroport CDG.
    """
    return Airport.objects.create(
        code="CDG",
        name="Aéroport de Paris-Charles de Gaulle",
        city="Paris",
        country="France",
        latitude=49.009700,
        longitude=2.547900,
        is_active=True,
    )


# ====================================================================
# Fixtures de données de référence — Aéronefs
# ====================================================================

@pytest.fixture
def sample_aircraft(db):
    """
    Crée un aéronef Airbus A320neo.

    Returns:
        Aircraft: Instance de l'aéronef A320neo.
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
# Fixtures de données de référence — Vols
# ====================================================================

@pytest.fixture
def sample_flight(db, sample_airport, sample_airport_paris, sample_aircraft):
    """
    Crée un vol programmé TUN → CDG avec un départ dans 5 jours.

    Returns:
        Flight: Instance du vol programmé.
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
# Fixtures de données de référence — Réservations
# ====================================================================

@pytest.fixture
def sample_booking(db, sample_flight, authenticated_client):
    """
    Crée une réservation en attente (pending) pour le vol TUN → CDG.

    Returns:
        Booking: Instance de la réservation créée.
    """
    # Récupérer l'utilisateur associé au client authentifié
    user = User.objects.get(username="testuser")

    booking = Booking.objects.create(
        user=user,
        contact_email="test@nouvelair.com",
        contact_phone="+216 22 345 678",
        status="pending",
        total_amount=350.00,
        special_requests="Siège côté hublot",
    )
    return booking


# ====================================================================
# Fixtures utilitaires
# ====================================================================

@pytest.fixture
def api_client(db):
    """
    Fournit un client de test Django pour les requêtes API.
    Équivalent à authenticated_client mais sans authentification,
    utile pour tester les endpoints publics.

    Returns:
        django.test.Client: Client de test non authentifié.
    """
    return Client()


@pytest.fixture
def future_date():
    """
    Retourne une date future (5 jours à partir d'aujourd'hui).

    Returns:
        datetime.date: Date dans 5 jours.
    """
    return date.today() + timedelta(days=5)
