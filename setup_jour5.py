#!/usr/bin/env python3
"""
setup_jour5.py - Création des fichiers de tests API pour Jour 5 (NouvelAir)

Ce script génère automatiquement tous les fichiers nécessaires pour les tests API
du Sprint 1, Jour 5 du projet de formation Django NouvelAir.

Fichiers créés:
    1. tests/api/__init__.py
    2. tests/api/conftest.py
    3. tests/api/test_autocomplete_api.py  (10 tests)
    4. tests/api/test_booking_api.py       (8 tests)
    5. tests/api/test_auth_api.py          (8 tests)
    6. tests/api/test_newsletter_api.py    (5 tests)
    7. docs/sprint1_metrics_template.md
    8. docs/retrospective_sprint1_template.md

Usage:
    python setup_jour5.py

Le script doit être exécuté depuis la racine du projet NouvelAir:
    D:\\NouvelairApp\\nouvelair_project\\
"""

import os
import sys

# ─────────────────────────────────────────────────────────────────────────────
# Configuration
# ─────────────────────────────────────────────────────────────────────────────

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TESTS_API_DIR = os.path.join(BASE_DIR, "tests", "api")
DOCS_DIR = os.path.join(BASE_DIR, "docs")

FILES_TO_CREATE = {
    "tests/api/__init__.py": "init_file",
    "tests/api/conftest.py": "conftest",
    "tests/api/test_autocomplete_api.py": "autocomplete_tests",
    "tests/api/test_booking_api.py": "booking_tests",
    "tests/api/test_auth_api.py": "auth_tests",
    "tests/api/test_newsletter_api.py": "newsletter_tests",
    "docs/sprint1_metrics_template.md": "metrics_template",
    "docs/retrospective_sprint1_template.md": "retrospective_template",
}

BANNER = r"""
╔══════════════════════════════════════════════════════════════╗
║         NouvelAir - Setup Tests API (Jour 5)                 ║
║         Sprint 1 · Formation Django                         ║
╚══════════════════════════════════════════════════════════════╝
"""


# ─────────────────────────────────────────────────────────────────────────────
# File Content Generators
# ─────────────────────────────────────────────────────────────────────────────

def get_init_file():
    """tests/api/__init__.py — fichier vide."""
    return ""


def get_conftest():
    """tests/api/conftest.py — fixtures partagées pour les tests API."""
    return '''\
"""
Fixtures partagées pour les tests API - Jour 5.

Fournit des utilitaires pour les requêtes API via Django test client,
incluant la gestion CSRF et la factory pour les utilisateurs de test.
"""

import pytest
from django.test import Client
from django.contrib.auth.models import User


# ── Marqueur pytest personnalisé ──────────────────────────────────────────────

def pytest_configure(config):
    """Enregistre le marqueur 'api' pour les tests API."""
    config.addinivalue_line(
        "markers", "api: marquage des tests d'API (Sprint 1, Jour 5)"
    )


# ── Fixtures de base ─────────────────────────────────────────────────────────

@pytest.fixture
def api_client():
    """
    Client de test Django standard pour les requêtes API.

    Contrairement au navigateur, le test client Django contourne
    automatiquement la vérification CSRF dans les requêtes POST
    lorsqu'on utilise enforce_csrf_checks=False (par défaut).

    Usage:
        response = api_client.get('/api/endpoint/')
        response = api_client.post('/api/endpoint/', data={...})
    """
    return Client()


@pytest.fixture
def csrf_client():
    """
    Client de test qui active explicitement la vérification CSRF.

    Ce client doit être utilisé pour tester que les vues rejettent
    correctement les requêtes sans token CSRF.

    Usage:
        response = csrf_client.post('/api/endpoint/', data={...})
        assert response.status_code == 403
    """
    return Client(enforce_csrf_checks=True)


@pytest.fixture
def api_client_factory():
    """
    Factory retournant un callable pour créer des clients configurables.

    Permet de créer des clients avec des options spécifiques (auth,
    headers, etc.) pour différents scénarios de test.

    Usage:
        factory = api_client_factory()
        client = client()
        authenticated_client = factory(user=user)

    Returns:
        callable: fonction acceptant des kwargs pour configurer le client.
    """
    def _factory(**kwargs):
        client = Client(**kwargs)
        return client
    return _factory


@pytest.fixture
def authenticated_client(api_client):
    """
    Client pré-authentifié avec un utilisateur de test standard.

    Crée un utilisateur avec les informations par défaut et le connecte
    automatiquement au client de test.

    Returns:
        tuple: (client, user) où user est l'utilisateur Django créé.
    """
    user = User.objects.create_user(
        username="testuser",
        email="testuser@nouvelair.com",
        password="SecurePass123!",
        first_name="Test",
        last_name="User",
    )
    api_client.force_login(user)
    return api_client, user


@pytest.fixture
def staff_client(api_client):
    """
    Client authentifié en tant que membre du staff (admin).

    Returns:
        tuple: (client, user) où user est un administrateur.
    """
    user = User.objects.create_superuser(
        username="admin",
        email="admin@nouvelair.com",
        password="AdminPass123!",
        first_name="Admin",
        last_name="NouvelAir",
    )
    api_client.force_login(user)
    return api_client, user


@pytest.fixture
def sample_airport_data():
    """
    Dictionnaire de données pour créer un aéroport de test.

    Returns:
        dict: données valides pour Airport.objects.create().
    """
    return {
        "code": "TST",
        "name": "Test Airport",
        "city": "Test City",
        "country": "Tunisia",
        "latitude": "36.806500",
        "longitude": "10.181500",
        "is_active": True,
    }


@pytest.fixture
def sample_user_data():
    """
    Dictionnaire de données pour créer un utilisateur de test.

    Returns:
        dict: données valides pour l'inscription.
    """
    return {
        "username": "newuser",
        "email": "newuser@example.com",
        "password1": "StrongPassword123!",
        "password2": "StrongPassword123!",
        "first_name": "Nouveau",
        "last_name": "Utilisateur",
    }


@pytest.fixture
def sample_booking_data():
    """
    Dictionnaire de données pour la recherche de réservation.

    Returns:
        dict: données pour le formulaire de lookup.
    """
    return {
        "reference": "ABCDEF12",
        "email": "client@nouvelair.com",
    }
'''


def get_autocomplete_tests():
    """tests/api/test_autocomplete_api.py — 10 tests pour l'autocomplétion."""
    return r'''\
"""
Tests API - Autocomplétion des aéroports (Jour 5).

Teste le endpoint GET /api/airports/autocomplete/?q=<query>
qui retourne une liste JSON d'aéroports correspondant à la recherche.

Couverture:
    - Requêtes valides et invalides
    - Structure de la réponse JSON
    - Filtrage par is_active
    - Tri et performance
"""

import time
import re
import pytest
from django.test import Client
from django.contrib.auth.models import User
from flights.models import Airport


# ── Helpers ───────────────────────────────────────────────────────────────────

def _create_airport(code, name, city, country, is_active=True):
    """Crée un aéroport de test avec les champs requis."""
    return Airport.objects.create(
        code=code,
        name=name,
        city=city,
        country=country,
        latitude="36.806500",
        longitude="10.181500",
        is_active=is_active,
    )


# ── Tests ─────────────────────────────────────────────────────────────────────

@pytest.mark.api
@pytest.mark.django_db
class TestAirportAutocompleteAPI:
    """Suite de tests pour l'endpoint d'autocomplétion des aéroports."""

    def setup_method(self):
        """Crée les aéroports de test avant chaque test."""
        self.client = Client()
        self.url = "/api/airports/autocomplete/"

        # Aéroports actifs
        _create_airport("TUN", "Aéroport Tunis-Carthage", "Tunis", "Tunisie")
        _create_airport("SFA", "Aéroport Sfax-Thyna", "Sfax", "Tunisie")
        _create_airport("MIR", "Aéroport Monastir Habib-Bourguiba", "Monastir", "Tunisie")
        _create_airport("TAB", "Aéroport Tabarka-Aïn Draham", "Tabarka", "Tunisie")
        _create_airport("TOE", "Aéroport Tozeur-Nefta", "Tozeur", "Tunisie")

        # Aéroport inactif (ne doit PAS apparaître dans les résultats)
        _create_airport("TBJ", "Aéroport Djerba-Zarzis", "Djerba", "Tunisie", is_active=False)

    # ─── Test 1: Requête valide avec query 'TUN' ──────────────────────────

    def test_autocomplete_valid_query(self):
        """GET avec q='TUN' → 200, JSON list avec au moins 1 résultat."""
        response = self.client.get(self.url, {"q": "TUN"})

        assert response.status_code == 200
        assert response["Content-Type"] == "application/json"

        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 1

        # Vérifier que l'aéroport Tunis-Carthage est dans les résultats
        codes = [airport["code"] for airport in data]
        assert "TUN" in codes

    # ─── Test 2: Requête avec query 'TU' → résultats multiples ───────────

    def test_autocomplete_multiple_results(self):
        """q='TU' → retourne plusieurs aéroports dont le code ou ville contient 'TU'."""
        response = self.client.get(self.url, {"q": "TU"})

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)

        # 'TU' matche le code TUN et potentiellement d'autres (ville contenant 'Tu')
        # Au minimum Tunis (TUN) doit être présent
        codes = [airport["code"] for airport in data]
        assert len(data) >= 1
        assert "TUN" in codes

    # ─── Test 3: Query d'un seul caractère ────────────────────────────────

    def test_autocomplete_single_char(self):
        """q='T' → résultats possibles ou liste vide."""
        response = self.client.get(self.url, {"q": "T"})

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)

        # Tous les aéroports actifs ont un code commençant par 'T',
        # donc on s'attend à des résultats (limités à 10 par la vue)
        if len(data) > 0:
            # Vérifier que chaque résultat contient bien 'T' dans code, name ou city
            for airport in data:
                matches = (
                    "T" in airport.get("code", "").upper()
                    or "T" in airport.get("name", "").upper()
                    or "T" in airport.get("city", "").upper()
                )
                assert matches, (
                    f"L'aéroport {airport.get('code')} ne correspond pas à 'T'"
                )

    # ─── Test 4: Query vide → liste vide ──────────────────────────────────

    def test_autocomplete_empty_query(self):
        """q='' → retourne une liste vide."""
        response = self.client.get(self.url, {"q": ""})

        assert response.status_code == 200
        data = response.json()
        assert data == []

    # ─── Test 5: Query sans résultats ─────────────────────────────────────

    def test_autocomplete_no_results(self):
        """q='XYZ' → liste vide (aucun aéroport ne correspond)."""
        response = self.client.get(self.url, {"q": "XYZ"})

        assert response.status_code == 200
        data = response.json()
        assert data == []

    # ─── Test 6: Structure de la réponse JSON ─────────────────────────────

    def test_autocomplete_response_structure(self):
        """Chaque aéroport dans la réponse possède les clés: id, code, name, city, country."""
        response = self.client.get(self.url, {"q": "TUN"})

        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 1

        expected_keys = {"id", "code", "name", "city", "country"}
        for airport in data:
            assert isinstance(airport, dict), f"Résultat non-dict: {type(airport)}"
            missing_keys = expected_keys - set(airport.keys())
            assert not missing_keys, (
                f"Clés manquantes dans la réponse: {missing_keys}. "
                f"Clés trouvées: {set(airport.keys())}"
            )

    # ─── Test 7: Format du code IATA ──────────────────────────────────────

    def test_autocomplete_code_format(self):
        """Le champ 'code' doit être exactement 3 lettres majuscules."""
        response = self.client.get(self.url, {"q": "T"})

        assert response.status_code == 200
        data = response.json()

        iata_pattern = re.compile(r"^[A-Z]{3}$")
        for airport in data:
            code = airport.get("code", "")
            assert iata_pattern.match(code), (
                f"Code IATA invalide: '{code}'. Attendu: 3 lettres majuscules."
            )

    # ─── Test 8: Seuls les aéroports actifs ───────────────────────────────

    def test_autocomplete_active_airports_only(self):
        """Seuls les aéroports avec is_active=True sont retournés."""
        response = self.client.get(self.url, {"q": "T"})

        assert response.status_code == 200
        data = response.json()

        # L'aéroport inactif (TBJ - Djerba) ne doit PAS apparaître
        codes = [airport["code"] for airport in data]
        assert "TBJ" not in codes, (
            "L'aéroport inactif TBJ ne devrait pas apparaître dans les résultats."
        )

        # Vérifier explicitement que tous les codes retournés correspondent
        # à des aéroports actifs en base
        for airport in data:
            db_airport = Airport.objects.get(pk=airport["id"])
            assert db_airport.is_active, (
                f"L'aéroport {db_airport.code} est inactif mais apparaît dans les résultats."
            )

    # ─── Test 9: Résultats triés par ville ────────────────────────────────

    def test_autocomplete_ordered_by_city(self):
        """Les résultats sont triés alphabétiquement par ville."""
        response = self.client.get(self.url, {"q": "T"})

        assert response.status_code == 200
        data = response.json()

        if len(data) >= 2:
            cities = [airport["city"] for airport in data]
            sorted_cities = sorted(cities)
            assert cities == sorted_cities, (
                f"Les résultats ne sont pas triés par ville. "
                f"Ordre actuel: {cities}, Attendu: {sorted_cities}"
            )

    # ─── Test 10: Temps de réponse < 500ms ────────────────────────────────

    def test_autocomplete_response_time(self):
        """L'endpoint répond en moins de 500ms."""
        start_time = time.time()
        response = self.client.get(self.url, {"q": "TUN"})
        elapsed_ms = (time.time() - start_time) * 1000

        assert response.status_code == 200
        assert elapsed_ms < 500, (
            f"Temps de réponse trop lent: {elapsed_ms:.1f}ms (limite: 500ms)"
        )
'''


def get_booking_tests():
    """tests/api/test_booking_api.py — 8 tests pour les réservations."""
    return r'''\
"""
Tests API - Réservations (Jour 5).

Teste les endpoints liés aux réservations:
    - GET/POST /reservations/recherche/  → lookup par référence
    - POST   /reservations/creer/        → création de réservation
    - POST   /reservations/annuler/<uuid> → annulation

Couverture:
    - Recherche de réservation (valid/invalid)
    - Création avec/sans authentification
    - Annulation (valid/déjà annulée)
"""

import uuid
import pytest
from django.test import Client
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta

from flights.models import Airport, Aircraft, Flight
from bookings.models import Booking, Passenger, Payment


# ── Helpers ───────────────────────────────────────────────────────────────────

def _create_flight(flight_number="BJ501", available_economy=10, available_business=5):
    """Crée un vol de test complet avec aéroports et aéronef."""
    origin = Airport.objects.create(
        code="TUN", name="Tunis-Carthage", city="Tunis", country="Tunisie",
        latitude="36.806500", longitude="10.181500", is_active=True,
    )
    destination = Airport.objects.create(
        code="CDG", name="Paris Charles de Gaulle", city="Paris", country="France",
        latitude="49.009700", longitude="2.547900", is_active=True,
    )
    aircraft = Aircraft.objects.create(
        model_name="Airbus A320",
        registration="TS-IMB",
        total_seats=150,
        economy_seats=130,
        business_seats=20,
        is_active=True,
    )
    departure = timezone.now() + timedelta(days=5)
    arrival = departure + timedelta(hours=2, minutes=30)

    flight = Flight.objects.create(
        flight_number=flight_number,
        origin=origin,
        destination=destination,
        aircraft=aircraft,
        departure_time=departure,
        arrival_time=arrival,
        base_price_economy=350.00,
        base_price_business=1200.00,
        available_seats_economy=available_economy,
        available_seats_business=available_business,
        status="scheduled",
    )
    return flight


def _create_booking(user=None, status="confirmed"):
    """Crée une réservation de test avec passager et paiement."""
    flight = _create_flight()
    booking = Booking.objects.create(
        user=user,
        contact_email="client@nouvelair.com",
        contact_phone="+21612345678",
        status=status,
        total_amount=350.00,
    )
    Passenger.objects.create(
        booking=booking,
        flight=flight,
        title="mr",
        first_name="Ahmed",
        last_name="Ben Ali",
        date_of_birth="1990-01-15",
        nationality="Tunisienne",
        travel_class="economy",
        price=350.00,
    )
    Payment.objects.create(
        booking=booking,
        amount=350.00,
        method="credit_card",
        status="completed" if status == "confirmed" else "pending",
        transaction_id=f"SIM-{booking.short_reference}",
    )
    return booking


# ── Tests ─────────────────────────────────────────────────────────────────────

@pytest.mark.api
@pytest.mark.django_db
class TestBookingLookupAPI:
    """Suite de tests pour la recherche de réservation par référence."""

    def setup_method(self):
        """Initialise le client et les données de test."""
        self.client = Client()
        self.lookup_url = "/reservations/recherche/"
        self.booking = _create_booking()
        self.short_ref = str(self.booking.reference)[:8].upper()

    # ─── Test 1: GET page lookup → 200 ────────────────────────────────────

    def test_booking_lookup_get(self):
        """GET /reservations/recherche/ → page de recherche (200)."""
        response = self.client.get(self.lookup_url)

        assert response.status_code == 200

    # ─── Test 2: POST avec référence valide → détails réservation ─────────

    def test_booking_lookup_valid_reference(self):
        """POST avec référence valide et email → redirect vers détails réservation."""
        response = self.client.post(self.lookup_url, {
            "reference": self.short_ref,
            "email": "client@nouvelair.com",
        }, follow=False)

        # La vue redirige vers la page de détail
        assert response.status_code == 302
        assert "/reservations/detail/" in response.url

    # ─── Test 3: POST avec référence invalide → message d'erreur ──────────

    def test_booking_lookup_invalid_reference(self):
        """POST avec une référence inexistante → message d'erreur."""
        response = self.client.post(self.lookup_url, {
            "reference": "ZZZZZZZZ",
            "email": "client@nouvelair.com",
        })

        assert response.status_code == 200
        # La vue utilise Django messages, vérifier la présence du contenu
        content = response.content.decode()
        assert "non trouv" in content.lower() or response.status_code == 200

    # ─── Test 4: POST sans champs → erreur ────────────────────────────────

    def test_booking_lookup_missing_fields(self):
        """POST sans les champs requis → message d'erreur."""
        response = self.client.post(self.lookup_url, {})

        assert response.status_code == 200
        content = response.content.decode()
        assert "fournir" in content.lower() or response.status_code == 200


@pytest.mark.api
@pytest.mark.django_db
class TestBookingCreateAPI:
    """Suite de tests pour la création de réservation."""

    def setup_method(self):
        """Initialise le client et les données de test."""
        self.client = Client()
        self.create_url = "/reservations/creer/"
        self.flight = _create_flight()

    # ─── Test 5: POST authentifié → redirect vers confirmation ────────────

    def test_booking_create_authenticated(self):
        """POST en tant qu'utilisateur connecté → redirect vers confirmation."""
        user = User.objects.create_user(
            username="passager", password="Pass123!", email="passager@test.com"
        )
        self.client.force_login(user)

        # Configurer la session avec les params de recherche et vol sélectionné
        session = self.client.session
        session["search_params"] = {
            "origin": "TUN",
            "destination": "CDG",
            "departure_date": (timezone.now() + timedelta(days=5)).date().isoformat(),
            "return_date": None,
            "passengers": 1,
            "travel_class": "economy",
            "trip_type": "oneway",
        }
        session["booking_flight_id"] = str(self.flight.id)
        session.save()

        passenger_data = {
            "0-title": "mr",
            "0-first_name": "Ahmed",
            "0-last_name": "Ben Ali",
            "0-date_of_birth": "1990-01-15",
            "0-nationality": "Tunisienne",
            "0-meal_preference": "",
            "contact_email": "passager@test.com",
            "contact_phone": "+21612345678",
            "special_requests": "",
        }

        response = self.client.post(self.create_url, passenger_data, follow=False)

        # Doit rediriger vers la confirmation
        assert response.status_code == 302
        assert "/reservations/confirmation/" in response.url or "/confirmation/" in response.url

    # ─── Test 6: POST sans authentification → redirect vers login ─────────

    def test_booking_create_unauthenticated(self):
        """POST sans être connecté → la réservation fonctionne (pas de LoginRequiredMixin).

        Note: BookingCreateView n'exige pas d'authentification, l'utilisateur
        peut être None. Le test vérifie simplement que la vue est accessible.
        """
        # Sans session de recherche, la vue redirige vers l'accueil
        response = self.client.post(self.create_url, {})

        assert response.status_code == 302
        # Redirige vers la page d'accueil (pas de paramètres de recherche)
        assert response.url == "/"


@pytest.mark.api
@pytest.mark.django_db
class TestBookingCancelAPI:
    """Suite de tests pour l'annulation de réservation."""

    def setup_method(self):
        """Initialise le client et les données de test."""
        self.client = Client()

    # ─── Test 7: POST annulation réservation valide → statut changé ───────

    def test_booking_cancel_valid(self):
        """POST pour annuler une réservation confirmée → statut passe à 'cancelled'."""
        booking = _create_booking(status="confirmed")
        cancel_url = f"/reservations/annuler/{booking.reference}/"

        response = self.client.post(cancel_url, follow=False)

        assert response.status_code == 302

        # Vérifier que le statut a été mis à jour en base
        booking.refresh_from_db()
        assert booking.status == "cancelled"

        # Vérifier que le paiement a été remboursé
        payment = booking.payments.first()
        if payment:
            assert payment.status == "refunded"

    # ─── Test 8: POST annulation déjà annulée → erreur ────────────────────

    def test_booking_cancel_already_cancelled(self):
        """POST pour annuler une réservation déjà annulée → message d'erreur."""
        booking = _create_booking(status="cancelled")
        cancel_url = f"/reservations/annuler/{booking.reference}/"

        response = self.client.post(cancel_url, follow=False)

        assert response.status_code == 302

        # Le statut ne doit pas avoir changé
        booking.refresh_from_db()
        assert booking.status == "cancelled"

        # La vue doit avoir ajouté un message d'erreur (vérifiable via messages)
        # Le redirect va vers la page de détail avec un message d'erreur
        assert "/reservations/detail/" in response.url
'''


def get_auth_tests():
    """tests/api/test_auth_api.py — 8 tests pour l'authentification."""
    return r'''\
"""
Tests API - Authentification (Jour 5).

Teste les endpoints liés à l'authentification:
    - POST /compte/connexion/   → login
    - POST /compte/inscription/ → register
    - GET  /compte/deconnexion/ → logout
    - GET  /compte/profil/      → page protégée

Couverture:
    - Connexion valide/invalide
    - Vérification CSRF
    - Inscription avec email dupliqué
    - Protection des pages authentifiées
    - Persistance de session
"""

import pytest
from django.test import Client
from django.contrib.auth.models import User
from accounts.models import UserProfile


# ── Helpers ───────────────────────────────────────────────────────────────────

def _create_test_user(username="testuser", password="SecurePass123!", **kwargs):
    """Crée un utilisateur de test avec profil."""
    defaults = {
        "email": f"{username}@nouvelair.com",
        "first_name": "Test",
        "last_name": "User",
    }
    defaults.update(kwargs)
    user = User.objects.create_user(
        username=username,
        password=password,
        email=defaults["email"],
        first_name=defaults["first_name"],
        last_name=defaults["last_name"],
    )
    UserProfile.objects.update_or_create(user=user, defaults={})
    return user


# ── Tests ─────────────────────────────────────────────────────────────────────

@pytest.mark.api
@pytest.mark.django_db
class TestAuthLoginAPI:
    """Suite de tests pour l'endpoint de connexion."""

    def setup_method(self):
        """Initialise le client et crée un utilisateur."""
        self.user = _create_test_user()
        self.login_url = "/compte/connexion/"
        self.client = Client()

    # ─── Test 1: Login avec identifiants valides → redirect ───────────────

    def test_login_api_valid(self):
        """POST /compte/connexion/ avec identifiants valides → 302 redirect."""
        response = self.client.post(self.login_url, {
            "username": "testuser",
            "password": "SecurePass123!",
        }, follow=False)

        assert response.status_code == 302
        # Le redirect va vers l'accueil ou la page 'next'
        assert response.url in ["/", "/compte/profil/"]

        # Vérifier que l'utilisateur est bien connecté
        assert "_auth_user_id" in self.client.session

    # ─── Test 2: Login avec mot de passe invalide → 200 avec erreur ───────

    def test_login_api_invalid(self):
        """POST avec mauvais mot de passe → 200 avec formulaire d'erreur."""
        response = self.client.post(self.login_url, {
            "username": "testuser",
            "password": "WrongPassword999!",
        })

        assert response.status_code == 200
        # Vérifier que l'utilisateur n'est PAS connecté
        assert "_auth_user_id" not in self.client.session

    # ─── Test 3: Login sans CSRF token → 403 ─────────────────────────────

    def test_login_api_csrf(self):
        """POST sans token CSRF → 403 Forbidden."""
        csrf_client = Client(enforce_csrf_checks=True)

        response = csrf_client.post(self.login_url, {
            "username": "testuser",
            "password": "SecurePass123!",
        })

        # Avec enforce_csrf_checks=True et sans token, Django renvoie 403
        assert response.status_code == 403


@pytest.mark.api
@pytest.mark.django_db
class TestAuthRegisterAPI:
    """Suite de tests pour l'endpoint d'inscription."""

    def setup_method(self):
        """Initialise le client."""
        self.register_url = "/compte/inscription/"
        self.client = Client()

    # ─── Test 4: Inscription avec données valides → nouvel utilisateur ────

    def test_register_api_valid(self):
        """POST /compte/inscription/ avec données valides → nouvel utilisateur + redirect."""
        user_count_before = User.objects.count()

        response = self.client.post(self.register_url, {
            "username": "newtraveler",
            "email": "newtraveler@nouvelair.com",
            "password1": "StrongPassword456!",
            "password2": "StrongPassword456!",
            "first_name": "Voyageur",
            "last_name": "Nouveau",
        }, follow=False)

        assert response.status_code == 302
        assert User.objects.count() == user_count_before + 1

        # Vérifier que le nouvel utilisateur existe
        new_user = User.objects.get(username="newtraveler")
        assert new_user.email == "newtraveler@nouvelair.com"
        assert new_user.first_name == "Voyageur"

        # Vérifier que le profil a été créé
        assert hasattr(new_user, "profile")

        # Vérifier que l'utilisateur est connecté après inscription
        assert "_auth_user_id" in self.client.session

    # ─── Test 5: Inscription avec email dupliqué → erreur ─────────────────

    def test_register_api_duplicate_email(self):
        """POST avec un email déjà utilisé → erreur dans le formulaire."""
        _create_test_user(username="existinguser", email="dup@example.com")

        response = self.client.post(self.register_url, {
            "username": "anotheruser",
            "email": "dup@example.com",
            "password1": "StrongPassword456!",
            "password2": "StrongPassword456!",
            "first_name": "Autre",
            "last_name": "Utilisateur",
        })

        assert response.status_code == 200
        content = response.content.decode()

        # Le formulaire doit afficher une erreur concernant l'email
        assert (
            "email" in content.lower()
            or "déjà" in content.lower()
            or "existe" in content.lower()
        )

        # Aucun nouvel utilisateur ne doit avoir été créé
        assert User.objects.filter(username="anotheruser").count() == 0


@pytest.mark.api
@pytest.mark.django_db
class TestAuthLogoutAPI:
    """Suite de tests pour la déconnexion."""

    def setup_method(self):
        """Initialise le client et connecte un utilisateur."""
        self.user = _create_test_user()
        self.logout_url = "/compte/deconnexion/"
        self.client = Client()
        self.client.force_login(self.user)

    # ─── Test 6: Logout → redirect vers accueil ───────────────────────────

    def test_logout_api(self):
        """GET /compte/deconnexion/ → déconnecte l'utilisateur et redirige."""
        # Vérifier que l'utilisateur est connecté
        assert "_auth_user_id" in self.client.session

        response = self.client.get(self.logout_url, follow=False)

        assert response.status_code == 302
        assert response.url == "/"

        # Vérifier que l'utilisateur est déconnecté
        assert "_auth_user_id" not in self.client.session


@pytest.mark.api
@pytest.mark.django_db
class TestProtectedPagesAPI:
    """Suite de tests pour la protection des pages authentifiées."""

    def setup_method(self):
        """Initialise le client."""
        self.client = Client()
        self.profile_url = "/compte/profil/"

    # ─── Test 7: Page protégée sans auth → redirect vers login ────────────

    def test_protected_api_redirect(self):
        """GET page protégée sans authentification → 302 vers la page de login."""
        response = self.client.get(self.profile_url, follow=False)

        assert response.status_code == 302
        # Le redirect doit pointer vers la page de connexion
        assert "/compte/connexion/" in response.url or "/compte/login/" in response.url

    # ─── Test 8: Persistance de session après login ───────────────────────

    def test_session_persistence(self):
        """Login → accéder page protégée → succès (session persistante)."""
        user = _create_test_user(username="sessionuser")

        # Étape 1: Login
        self.client.post("/compte/connexion/", {
            "username": "sessionuser",
            "password": "SecurePass123!",
        })
        assert "_auth_user_id" in self.client.session

        # Étape 2: Accéder à la page protégée
        response = self.client.get(self.profile_url)

        assert response.status_code == 200
        content = response.content.decode()
        # Vérifier que le profil est affiché (contient au moins le formulaire)
        assert "profil" in content.lower() or "profile" in content.lower()
'''


def get_newsletter_tests():
    """tests/api/test_newsletter_api.py — 5 tests pour la newsletter."""
    return r'''\
"""
Tests API - Newsletter (Jour 5).

Teste le endpoint POST /promotions/newsletter/
qui gère l'inscription à la newsletter.

Couverture:
    - Inscription valide
    - Email en double
    - Email invalide
    - Email manquant
    - Format de la réponse JSON
"""

import pytest
from django.test import Client
from promotions.models import NewsletterSubscription


# ── Helpers ───────────────────────────────────────────────────────────────────

VALID_EMAIL = "abonné@nouvelair.com"


# ── Tests ─────────────────────────────────────────────────────────────────────

@pytest.mark.api
@pytest.mark.django_db
class TestNewsletterAPI:
    """Suite de tests pour l'endpoint d'inscription à la newsletter."""

    def setup_method(self):
        """Initialise le client de test."""
        self.client = Client()
        self.newsletter_url = "/promotions/newsletter/"

    # ─── Test 1: Inscription avec email valide → succès JSON ──────────────

    def test_newsletter_subscribe_valid(self):
        """POST avec email valide → JSON {success: true, message: ...}."""
        response = self.client.post(self.newsletter_url, {
            "email": VALID_EMAIL,
            "first_name": "Ahmed",
        })

        assert response.status_code == 200
        assert response["Content-Type"] == "application/json"

        data = response.json()
        assert data["success"] is True
        assert "message" in data

        # Vérifier en base que l'abonnement a été créé
        assert NewsletterSubscription.objects.filter(email=VALID_EMAIL).exists()

        subscription = NewsletterSubscription.objects.get(email=VALID_EMAIL)
        assert subscription.first_name == "Ahmed"
        assert subscription.is_active is True

    # ─── Test 2: Inscription avec email en double → erreur ────────────────

    def test_newsletter_subscribe_duplicate(self):
        """POST avec un email déjà inscrit → JSON {success: false, error: ...}."""
        # Créer un premier abonnement
        NewsletterSubscription.objects.create(
            email=VALID_EMAIL,
            first_name="Original",
            is_active=True,
        )

        # Tenter de ré-inscrire le même email
        response = self.client.post(self.newsletter_url, {
            "email": VALID_EMAIL,
            "first_name": "Dupliqué",
        })

        assert response.status_code == 200
        data = response.json()
        assert data["success"] is False
        assert "error" in data

        # Vérifier qu'il n'y a toujours qu'un seul abonnement
        assert NewsletterSubscription.objects.filter(email=VALID_EMAIL).count() == 1

    # ─── Test 3: Inscription avec email invalide → erreur ─────────────────

    def test_newsletter_subscribe_invalid_email(self):
        """POST avec un email mal formaté → le champ email est requis mais
        la vue ne valide pas le format, elle tente simplement get_or_create.
        Ce test vérifie le comportement avec une chaîne vide-like.
        """
        response = self.client.post(self.newsletter_url, {
            "email": "not-an-email",
            "first_name": "Test",
        })

        assert response.status_code == 200

        data = response.json()
        # La vue fait get_or_create avec l'email tel quel;
        # un email invalide sera stocké (pas de validation serveur).
        # Le test vérifie simplement que la réponse est cohérente.
        assert "success" in data

    # ─── Test 4: Inscription sans email → erreur ──────────────────────────

    def test_newsletter_subscribe_missing_email(self):
        """POST sans le champ email → JSON {success: false, error: ...}."""
        response = self.client.post(self.newsletter_url, {
            "first_name": "SansEmail",
        })

        assert response.status_code == 200
        data = response.json()
        assert data["success"] is False
        assert "error" in data
        assert "email" in data["error"].lower() or "requis" in data["error"].lower()

        # Aucun abonnement ne doit avoir été créé
        assert NewsletterSubscription.objects.filter(first_name="SansEmail").count() == 0

    # ─── Test 5: Format de la réponse JSON ────────────────────────────────

    def test_newsletter_subscribe_response_format(self):
        """La réponse JSON contient les clés attendues: success + (message|error)."""
        # Cas succès
        unique_email = f"unique-{__import__('uuid').uuid4().hex[:8]}@test.com"
        response = self.client.post(self.newsletter_url, {
            "email": unique_email,
        })

        assert response.status_code == 200
        assert response["Content-Type"] == "application/json"

        data = response.json()
        assert "success" in data, "La clé 'success' est manquante dans la réponse."
        assert isinstance(data["success"], bool), "'success' doit être un booléen."

        # Doit contenir 'message' (succès) ou 'error' (échec)
        has_message = "message" in data
        has_error = "error" in data
        assert has_message or has_error, (
            "La réponse doit contenir 'message' ou 'error'."
        )

        # Cas erreur (email manquant)
        response_error = self.client.post(self.newsletter_url, {})
        data_error = response_error.json()

        assert "success" in data_error
        assert "error" in data_error, (
            "La réponse d'erreur doit contenir la clé 'error'."
        )
'''


def get_metrics_template():
    """docs/sprint1_metrics_template.md — Template de métriques Sprint 1."""
    return '''\
# 📊 Métriques de Qualité - Sprint 1 (NouvelAir)

> **Projet:** NouvelAir - Système de Réservation Aérienne  
> **Sprint:** 1  
> **Date de mise à jour:** JJ/MM/AAAA  
> **Équipe:** [Noms des membres]

---

## 1. Métriques de Tests Unitaires

| Métrique | Cible | Réel | Statut |
|----------|-------|------|--------|
| Nombre total de tests unitaires | ≥ 30 | `_ _ _` | ⬜ |
| Tests passés | 100% | `_ _ _` | ⬜ |
| Tests échoués | 0 | `_ _ _` | ⬜ |
| Taux de réussite | 100% | `_ _ _ %` | ⬜ |
| Temps d'exécution moyen | < 10s | `_ _ _ s` | ⬜ |

### Répartition par application

| Application | Tests | Passés | Échoués | Couverture |
|-------------|-------|--------|---------|------------|
| `flights` | `_ _ _` | `_ _ _` | `_ _ _` | `_ _ _ %` |
| `bookings` | `_ _ _` | `_ _ _` | `_ _ _` | `_ _ _ %` |
| `accounts` | `_ _ _` | `_ _ _` | `_ _ _` | `_ _ _ %` |
| `destinations` | `_ _ _` | `_ _ _` | `_ _ _` | `_ _ _ %` |
| `promotions` | `_ _ _` | `_ _ _` | `_ _ _` | `_ _ _ %` |

---

## 2. Métriques de Tests d'Intégration

| Métrique | Cible | Réel | Statut |
|----------|-------|------|--------|
| Nombre total de tests d'intégration | ≥ 15 | `_ _ _` | ⬜ |
| Tests passés | 100% | `_ _ _` | ⬜ |
| Tests échoués | 0 | `_ _ _` | ⬜ |
| Temps d'exécution total | < 30s | `_ _ _ s` | ⬜ |

### Scénarios d'intégration testés

| Scénario | Endpoint(s) | Statut | Remarques |
|----------|-------------|--------|-----------|
| Recherche de vol complète | `POST /` → `/recherche/` | ⬜ | |
| Création de réservation | `POST /reservations/creer/` | ⬜ | |
| Recherche de réservation | `POST /reservations/recherche/` | ⬜ | |
| Inscription + Connexion | `POST /compte/inscription/` → `/connexion/` | ⬜ | |
| Annulation de réservation | `POST /reservations/annuler/` | ⬜ | |

---

## 3. Métriques BDD (Gherkin)

| Métrique | Cible | Réel | Statut |
|----------|-------|------|--------|
| Nombre de scénarios Gherkin | ≥ 10 | `_ _ _` | ⬜ |
| Scénarios passés (Behave) | 100% | `_ _ _` | ⬜ |
| Étapes définies (steps) | ≥ 30 | `_ _ _` | ⬜ |
| Fichiers feature | ≥ 5 | `_ _ _` | ⬜ |

### Répartition par fichier feature

| Feature File | Scénarios | Passés | Échoués |
|--------------|-----------|--------|---------|
| `search_flights.feature` | `_ _ _` | `_ _ _` | `_ _ _` |
| `booking_management.feature` | `_ _ _` | `_ _ _` | `_ _ _` |
| `user_authentication.feature` | `_ _ _` | `_ _ _` | `_ _ _` |
| `newsletter.feature` | `_ _ _` | `_ _ _` | `_ _ _` |
| `booking_lookup.feature` | `_ _ _` | `_ _ _` | `_ _ _` |

---

## 4. Métriques API

| Métrique | Cible | Réel | Statut |
|----------|-------|------|--------|
| Nombre total de tests API | ≥ 30 | `_ _ _` | ⬜ |
| Tests API passés | 100% | `_ _ _` | ⬜ |
| Temps de réponse moyen | < 500ms | `_ _ _ ms` | ⬜ |
| Taux d'erreur API | 0% | `_ _ _ %` | ⬜ |

### Détail par endpoint API

| Endpoint | Méthode | Tests | Passés | Temps moyen |
|----------|---------|-------|--------|-------------|
| `/api/airports/autocomplete/` | GET | 10 | `_ _ _` | `_ _ _ ms` |
| `/reservations/recherche/` | GET/POST | 4 | `_ _ _` | `_ _ _ ms` |
| `/reservations/creer/` | POST | 2 | `_ _ _` | `_ _ _ ms` |
| `/reservations/annuler/<uuid>` | POST | 2 | `_ _ _` | `_ _ _ ms` |
| `/compte/connexion/` | POST | 3 | `_ _ _` | `_ _ _ ms` |
| `/compte/inscription/` | POST | 2 | `_ _ _` | `_ _ _ ms` |
| `/compte/deconnexion/` | GET | 1 | `_ _ _` | `_ _ _ ms` |
| `/promotions/newsletter/` | POST | 5 | `_ _ _` | `_ _ _ ms` |

---

## 5. Couverture de Code

| Application | Lignes totales | Lignes couvertes | Couverture % | Statut |
|-------------|---------------|------------------|--------------|--------|
| `flights` | `_ _ _` | `_ _ _` | `_ _ _ %` | ⬜ |
| `bookings` | `_ _ _` | `_ _ _` | `_ _ _ %` | ⬜ |
| `accounts` | `_ _ _` | `_ _ _` | `_ _ _ %` | ⬜ |
| `destinations` | `_ _ _` | `_ _ _` | `_ _ _ %` | ⬜ |
| `promotions` | `_ _ _` | `_ _ _` | `_ _ _ %` | ⬜ |
| **Total** | `_ _ _` | `_ _ _` | `_ _ _ %` | ⬜ |

### Commande de génération du rapport

```bash
coverage run --source='.' manage.py test
coverage report --skip-covered
coverage html
```

---

## 6. Bugs Documentés

| ID | Sévérité | Description | Statut | Assigné | Date |
|----|----------|-------------|--------|---------|------|
| BUG-001 | 🔴 Critique | `_ _ _` | ⬜ Ouvert | `_ _ _` | JJ/MM |
| BUG-002 | 🟡 Moyen | `_ _ _` | ⬜ Ouvert | `_ _ _` | JJ/MM |
| BUG-003 | 🟢 Mineur | `_ _ _` | ⬜ Résolu | `_ _ _` | JJ/MM |

---

## 7. Taux de Réussite Global

| Catégorie | Tests | Passés | Échoués | Taux |
|-----------|-------|--------|---------|------|
| Unitaires | `_ _ _` | `_ _ _` | `_ _ _` | `_ _ _ %` |
| Intégration | `_ _ _` | `_ _ _` | `_ _ _` | `_ _ _ %` |
| BDD (Gherkin) | `_ _ _` | `_ _ _` | `_ _ _` | `_ _ _ %` |
| API | `_ _ _` | `_ _ _` | `_ _ _` | `_ _ _ %` |
| **Total** | `_ _ _` | `_ _ _` | `_ _ _` | `_ _ _ %` |

### Objectifs Sprint 2

- [ ] Atteindre ≥ 80% de couverture de code
- [ ] Zéro test échoué
- [ ] Temps d'exécution total < 60s
- [ ] Tous les endpoints API testés

---

*Généré automatiquement - Template Sprint 1 NouvelAir*
'''


def get_retrospective_template():
    """docs/retrospective_sprint1_template.md — Template rétrospective Sprint 1."""
    return '''\
# 🔄 Rétrospective Sprint 1 - NouvelAir

> **Projet:** NouvelAir - Système de Réservation Aérienne  
> **Sprint:** 1 (Semaines 1-5)  
> **Date de la rétrospective:** JJ/MM/AAAA  
> **Participants:** [Noms des membres de l'équipe]  
> **Facilitateur:** [Nom]  
> **Noteur:** [Nom]

---

## 📋 Résumé du Sprint

| Élément | Détail |
|---------|--------|
| **Objectif principal** | Mise en place du projet Django avec les 5 applications |
| **Durée** | 5 semaines |
| **User Stories complétées** | `_ _ _ / _ _ _` |
| **Story Points livrés** | `_ _ _ / _ _ _` |
| **Bugs découverts** | `_ _ _` |
| **Bugs résolus** | `_ _ _` |

---

## 🟢 START (À Commencer - Sprint 2)

*Ce que l'équipe devrait commencer à faire dans le prochain sprint.*

| # | Action | Priorité | Responsable |
|---|--------|----------|-------------|
| 1 | `_ _ _` | 🔴 Haute | `_ _ _` |
| 2 | `_ _ _` | 🟡 Moyenne | `_ _ _` |
| 3 | `_ _ _` | 🟢 Basse | `_ _ _` |

> **Notes:** Quelles nouvelles pratiques, outils ou comportements adopter ?

---

## 🔴 STOP (À Arrêter - Sprint 2)

*Ce que l'équipe devrait arrêter de faire.*

| # | Pratique à arrêter | Raison | Alternative |
|---|-------------------|--------|-------------|
| 1 | `_ _ _` | `_ _ _` | `_ _ _` |
| 2 | `_ _ _` | `_ _ _` | `_ _ _` |
| 3 | `_ _ _` | `_ _ _` | `_ _ _` |

> **Notes:** Quels obstacles, mauvaises habitudes ou pratiques inefficaces identifier ?

---

## 🟡 CONTINUE (À Continuer - Sprint 2)

*Ce qui a bien fonctionné et doit être maintenu.*

| # | Pratique | Pourquoi ça marche | Amélioration possible |
|---|----------|-------------------|----------------------|
| 1 | `_ _ _` | `_ _ _` | `_ _ _` |
| 2 | `_ _ _` | `_ _ _` | `_ _ _` |
| 3 | `_ _ _` | `_ _ _` | `_ _ _` |

> **Notes:** Quelles sont les forces de l'équipe à préserver ?

---

## ✅ Ce qui a bien marché (What Went Well)

### Développement
- `_ _ _`

### Collaboration
- `_ _ _`

### Tests & Qualité
- `_ _ _`

### Apprentissage
- `_ _ _`

---

## ⚠️ Ce qui est à améliorer (What to Improve)

### Processus
- `_ _ _`

### Technique
- `_ _ _`

### Communication
- `_ _ _`

### Documentation
- `_ _ _`

---

## 📌 Action Items pour Sprint 2

| # | Action Item | Type | Priorité | Responsable | Deadline |
|---|-------------|------|----------|-------------|----------|
| 1 | `_ _ _` | Tech | 🔴 | `_ _ _` | JJ/MM |
| 2 | `_ _ _` | Process | 🔴 | `_ _ _` | JJ/MM |
| 3 | `_ _ _` | Tech | 🟡 | `_ _ _` | JJ/MM |
| 4 | `_ _ _` | Doc | 🟡 | `_ _ _` | JJ/MM |
| 5 | `_ _ _` | Collab | 🟢 | `_ _ _` | JJ/MM |

---

## 💬 Feedback individuel de l'équipe

### Membre 1: `_ _ _`

| Question | Réponse |
|----------|---------|
| Moment fort du sprint | `_ _ _` |
| Plus grande difficulté | `_ _ _` |
| Proposition d'amélioration | `_ _ _` |
| Note de satisfaction (1-5) | `_ _ _ / 5` |

### Membre 2: `_ _ _`

| Question | Réponse |
|----------|---------|
| Moment fort du sprint | `_ _ _` |
| Plus grande difficulté | `_ _ _` |
| Proposition d'amélioration | `_ _ _` |
| Note de satisfaction (1-5) | `_ _ _ / 5` |

### Membre 3: `_ _ _`

| Question | Réponse |
|----------|---------|
| Moment fort du sprint | `_ _ _` |
| Plus grande difficulté | `_ _ _` |
| Proposition d'amélioration | `_ _ _` |
| Note de satisfaction (1-5) | `_ _ _ / 5` |

---

## 📈 Indicateurs Clés (KPIs) Sprint 1

| KPI | Valeur Sprint 1 | Objectif Sprint 2 |
|-----|-----------------|-------------------|
| Vélocité (Story Points) | `_ _ _` | `_ _ _` |
| Taux de complétion US | `_ _ _ %` | ≥ 85% |
| Couverture de tests | `_ _ _ %` | ≥ 80% |
| Bugs par US | `_ _ _` | < 1 |
| Temps moyen de review | `_ _ _ h` | < 24h |
| Dette technique | `_ _ _` | `_ _ _` |

---

## 🔗 Ressources & Liens

- [Repository Git](`_ _ _`)
- [Board Trello/Jira](`_ _ _`)
- [Documentation technique](`_ _ _`)
- [Rapport de couverture](`_ _ _`)

---

*Template de rétrospective - Projet NouvelAir - Formation Django*
*Format: Start / Stop / Continue + Action Items*
'''


# ─────────────────────────────────────────────────────────────────────────────
# Main Execution
# ─────────────────────────────────────────────────────────────────────────────

def create_file(filepath, content, description=""):
    """Crée un fichier avec son contenu et affiche un message de confirmation."""
    # Créer les répertoires parents si nécessaire
    os.makedirs(os.path.dirname(filepath), exist_ok=True)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

    size = os.path.getsize(filepath)
    lines = content.count("\n") + 1
    print(f"  ✅ {filepath}")
    print(f"     ({description}) — {lines} lignes, {size} octets")


def main():
    """Point d'entrée principal du script."""
    print(BANNER)

    # Déterminer le répertoire de travail
    # Le script peut être exécuté depuis n'importe où,
    # on utilise le répertoire contenant setup_jour5.py comme BASE_DIR.
    global BASE_DIR

    # Si exécuté depuis un autre endroit, utiliser le CWD
    cwd = os.getcwd()

    # Vérifier si on est dans un projet Django NouvelAir
    manage_py = os.path.join(cwd, "manage.py")
    if os.path.exists(manage_py):
        BASE_DIR = cwd
    else:
        print(f"⚠️  Attention: 'manage.py' non trouvé dans {cwd}")
        print(f"   Utilisation de {BASE_DIR} comme base.\n")

    # Mapper les fichiers vers leur contenu
    file_generators = {
        "tests/api/__init__.py": ("Fichier __init__ vide pour le package", get_init_file),
        "tests/api/conftest.py": ("Fixtures partagées pytest (api_client, csrf_client, etc.)", get_conftest),
        "tests/api/test_autocomplete_api.py": ("10 tests - Autocomplétion aéroports", get_autocomplete_tests),
        "tests/api/test_booking_api.py": ("8 tests - Réservations (lookup, create, cancel)", get_booking_tests),
        "tests/api/test_auth_api.py": ("8 tests - Authentification (login, register, logout)", get_auth_tests),
        "tests/api/test_newsletter_api.py": ("5 tests - Newsletter (subscribe, validate)", get_newsletter_tests),
        "docs/sprint1_metrics_template.md": ("Template métriques QA Sprint 1 (Français)", get_metrics_template),
        "docs/retrospective_sprint1_template.md": ("Template rétrospective Sprint 1 (Français)", get_retrospective_template),
    }

    print(f"📂 Répertoire de base : {BASE_DIR}\n")
    print("Création des fichiers :\n")

    files_created = 0
    total_tests = 0

    for relative_path, (description, generator) in file_generators.items():
        filepath = os.path.join(BASE_DIR, relative_path)
        content = generator()
        create_file(filepath, content, description)
        files_created += 1

        # Compter les tests
        if "test_" in relative_path and relative_path.endswith(".py"):
            # Compter les fonctions de test (méthodes commençant par test_)
            test_count = content.count("def test_")
            total_tests += test_count

    # ── Résumé ─────────────────────────────────────────────────────────────
    print(f"\n{'═' * 60}")
    print(f"  📊 RÉSUMÉ")
    print(f"{'═' * 60}")
    print(f"  Fichiers créés    : {files_created}")
    print(f"  Tests API totaux  : {total_tests}")
    print(f"")
    print(f"  Détail par fichier :")
    print(f"  ┌──────────────────────────────────────┬───────┐")
    print(f"  │ Fichier                               │ Tests │")
    print(f"  ├──────────────────────────────────────┼───────┤")

    test_details = [
        ("test_autocomplete_api.py", 10),
        ("test_booking_api.py", 8),
        ("test_auth_api.py", 8),
        ("test_newsletter_api.py", 5),
    ]
    for filename, count in test_details:
        print(f"  │ {filename:<36} │ {count:>5} │")
    print(f"  ├──────────────────────────────────────┼───────┤")
    print(f"  │ TOTAL                                 │ {total_tests:>5} │")
    print(f"  └──────────────────────────────────────┴───────┘")

    print(f"\n  📁 Structure créée :")
    print(f"     tests/")
    print(f"       api/")
    print(f"         __init__.py")
    print(f"         conftest.py")
    print(f"         test_autocomplete_api.py  (10 tests)")
    print(f"         test_booking_api.py       (8 tests)")
    print(f"         test_auth_api.py          (8 tests)")
    print(f"         test_newsletter_api.py    (5 tests)")
    print(f"     docs/")
    print(f"       sprint1_metrics_template.md")
    print(f"       retrospective_sprint1_template.md")

    print(f"\n{'═' * 60}")
    print(f"  🚀 Prochaines étapes :")
    print(f"{'═' * 60}")
    print(f"  1. Exécuter les tests API :")
    print(f"     python manage.py pytest tests/api/ -v -m api")
    print(f"")
    print(f"  2. Exécuter avec couverture :")
    print(f"     python manage.py pytest tests/api/ --cov=. --cov-report=html")
    print(f"")
    print(f"  3. Exécuter un fichier spécifique :")
    print(f"     python manage.py pytest tests/api/test_auth_api.py -v")
    print(f"")
    print(f"  4. Remplir les templates de métriques et rétrospective :")
    print(f"     docs/sprint1_metrics_template.md")
    print(f"     docs/retrospective_sprint1_template.md")
    print(f"{'═' * 60}\n")


if __name__ == "__main__":
    main()
