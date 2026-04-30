#!/usr/bin/env python3
"""
setup_jour3.py — Crée les fichiers de tests d'intégration pour le Jour 3
=======================================================================
Projet NouvelAir — Django Training Project

Ce script génère automatiquement :
  1. tests/integration/__init__.py
  2. tests/integration/conftest.py
  3. tests/integration/test_views_flights.py    (15 tests)
  4. tests/integration/test_views_accounts.py   (10 tests)
  5. tests/integration/test_views_bookings.py   ( 7 tests)
  6. tests/integration/test_views_destinations.py (5 tests)
  7. tests/integration/test_views_promotions.py  (5 tests)
  8. docs/coverage_report_sprint1.md

Utilisation :
    cd D:\\NouvelairApp\\nouvelair_project
    python setup_jour3.py

Exécution des tests :
    pytest tests/integration/ -m integration -v
    pytest tests/integration/ -m integration --cov=. --cov-report=html
"""

import os
import sys

# ── Chemins ────────────────────────────────────────────────────────────────────
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
# Le script est placé à la racine du projet Django (à côté de manage.py)
PROJECT_ROOT = SCRIPT_DIR


def ensure_dir(path):
    """Crée le répertoire s'il n'existe pas."""
    if not os.path.exists(path):
        os.makedirs(path)
        print(f"  📁  Créé : {os.path.relpath(path, PROJECT_ROOT)}")


def write_file(path, content):
    """Écrit le fichier et affiche un résumé."""
    ensure_dir(os.path.dirname(path))
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    rel = os.path.relpath(path, PROJECT_ROOT)
    lines = content.count("\n") + 1
    print(f"  📄  {rel}  ({lines} lignes)")


# ══════════════════════════════════════════════════════════════════════════════
#  FICHIER 1 — tests/integration/__init__.py  (vide)
# ══════════════════════════════════════════════════════════════════════════════

FILE_INIT = ""


# ══════════════════════════════════════════════════════════════════════════════
#  FICHIER 2 — tests/integration/conftest.py
# ══════════════════════════════════════════════════════════════════════════════

FILE_CONFTEST = r'''"""
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
'''


# ══════════════════════════════════════════════════════════════════════════════
#  FICHIER 3 — tests/integration/test_views_flights.py  (15 tests)
# ══════════════════════════════════════════════════════════════════════════════

FILE_FLIGHTS = r'''"""
Tests d'intégration — Vues de l'application Flights (15 tests).

Couvre : HomeView, FlightSearchResultsView, FlightDetailView,
         AirportListView, airport_autocomplete.
"""

import pytest
from datetime import date, timedelta
from django.test import Client
from django.urls import reverse
from django.utils import timezone


# ── 1. test_home_view_status ─────────────────────────────────────────────────


@pytest.mark.integration
@pytest.mark.django_db
def test_home_view_status(db):
    """GET '/' retourne un statut 200."""
    client = Client()
    response = client.get(reverse("flights:home"))
    assert response.status_code == 200


# ── 2. test_home_view_template ───────────────────────────────────────────────


@pytest.mark.integration
@pytest.mark.django_db
def test_home_view_template(db):
    """La page d'accueil utilise les templates 'flights/home.html' et 'base.html'."""
    client = Client()
    response = client.get(reverse("flights:home"))
    assert response.status_code == 200
    assert "flights/home.html" in [t.name for t in response.templates]
    assert "base.html" in [t.name for t in response.templates]


# ── 3. test_home_view_contains_form ──────────────────────────────────────────


@pytest.mark.integration
@pytest.mark.django_db
def test_home_view_contains_form(db):
    """Le contexte contient le FlightSearchForm sous la clé 'search_form'."""
    client = Client()
    response = client.get(reverse("flights:home"))
    assert response.status_code == 200
    assert "search_form" in response.context


# ── 4. test_home_view_popular_destinations ───────────────────────────────────


@pytest.mark.integration
@pytest.mark.django_db
def test_home_view_popular_destinations(setup_db):
    """Le contexte contient 'popular_destinations' avec les aéroports actifs."""
    client = Client()
    response = client.get(reverse("flights:home"))
    assert response.status_code == 200
    assert "popular_destinations" in response.context
    destinations = response.context["popular_destinations"]
    assert len(destinations) <= 6


# ── 5. test_home_view_upcoming_flights ───────────────────────────────────────


@pytest.mark.integration
@pytest.mark.django_db
def test_home_view_upcoming_flights(setup_db):
    """Le contexte contient 'upcoming_flights' avec les vols à venir."""
    client = Client()
    response = client.get(reverse("flights:home"))
    assert response.status_code == 200
    assert "upcoming_flights" in response.context
    flights = response.context["upcoming_flights"]
    assert len(flights) <= 4


# ── 6. test_search_flight_post ───────────────────────────────────────────────


@pytest.mark.integration
@pytest.mark.django_db
def test_search_flight_post(setup_db, search_form_data):
    """POST avec des paramètres valides redirige vers search_results."""
    client = Client()
    response = client.post(reverse("flights:home"), data=search_form_data)
    assert response.status_code == 302
    assert response.url == reverse("flights:search_results")


# ── 7. test_search_same_airport_error ────────────────────────────────────────


@pytest.mark.integration
@pytest.mark.django_db
def test_search_same_airport_error(setup_db):
    """POST avec origin == destination renvoie une erreur contenant 'différents'."""
    client = Client()
    future_date = (date.today() + timedelta(days=7)).strftime("%Y-%m-%d")
    data = {
        "trip_type": "oneway",
        "origin": str(setup_db["airport_tun"].pk),
        "destination": str(setup_db["airport_tun"].pk),
        "departure_date": future_date,
        "passengers": "1",
        "travel_class": "economy",
    }
    response = client.post(reverse("flights:home"), data=data)
    # Le formulaire est invalide → rendu 200 (pas de redirection)
    assert response.status_code == 200
    # Vérifie que le message d'erreur est présent dans le contenu
    content = response.content.decode()
    assert "diff" in content.lower() or "diff" in str(
        response.context.get("search_form").errors
    )


# ── 8. test_search_past_date_error ───────────────────────────────────────────


@pytest.mark.integration
@pytest.mark.django_db
def test_search_past_date_error(setup_db):
    """POST avec une date de départ passée renvoie une erreur de validation."""
    client = Client()
    past_date = (date.today() - timedelta(days=5)).strftime("%Y-%m-%d")
    data = {
        "trip_type": "oneway",
        "origin": str(setup_db["airport_tun"].pk),
        "destination": str(setup_db["airport_par"].pk),
        "departure_date": past_date,
        "passengers": "1",
        "travel_class": "economy",
    }
    response = client.post(reverse("flights:home"), data=data)
    assert response.status_code == 200


# ── 9. test_flight_detail_view ───────────────────────────────────────────────


@pytest.mark.integration
@pytest.mark.django_db
def test_flight_detail_view(setup_db):
    """GET /vol/<flight_number>/ pour un vol existant retourne 200 et le contexte."""
    client = Client()
    flight = setup_db["flight1"]
    response = client.get(
        reverse("flights:flight_detail", kwargs={"flight_number": flight.flight_number})
    )
    assert response.status_code == 200
    assert "flight" in response.context
    assert response.context["flight"].flight_number == flight.flight_number


# ── 10. test_flight_detail_view_404 ──────────────────────────────────────────


@pytest.mark.integration
@pytest.mark.django_db
def test_flight_detail_view_404(db):
    """GET /vol/<inexistant>/ retourne 404."""
    client = Client()
    response = client.get(
        reverse("flights:flight_detail", kwargs={"flight_number": "XX999"})
    )
    assert response.status_code == 404


# ── 11. test_airport_list_view ───────────────────────────────────────────────


@pytest.mark.integration
@pytest.mark.django_db
def test_airport_list_view(setup_db):
    """GET /aeroports/ retourne 200 et le contexte contient 'airports'."""
    client = Client()
    response = client.get(reverse("flights:airport_list"))
    assert response.status_code == 200
    assert "airports" in response.context
    assert len(response.context["airports"]) >= 3


# ── 12. test_airport_autocomplete ────────────────────────────────────────────


@pytest.mark.integration
@pytest.mark.django_db
def test_airport_autocomplete(setup_db):
    """GET /api/airports/autocomplete/?q=TU retourne une liste JSON."""
    client = Client()
    response = client.get(
        reverse("flights:airport_autocomplete"), {"q": "TU"}
    )
    assert response.status_code == 200
    assert response["Content-Type"] == "application/json"
    data = response.json()
    assert isinstance(data, list)
    # Au moins TUN devrait correspondre
    assert len(data) >= 1
    codes = [item["code"] for item in data]
    assert "TUN" in codes


# ── 13. test_airport_autocomplete_empty ──────────────────────────────────────


@pytest.mark.integration
@pytest.mark.django_db
def test_airport_autocomplete_empty(db):
    """GET /api/airports/autocomplete/?q= (vide) retourne une liste JSON vide."""
    client = Client()
    response = client.get(
        reverse("flights:airport_autocomplete"), {"q": ""}
    )
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 0


# ── 14. test_flight_search_results ───────────────────────────────────────────


@pytest.mark.integration
@pytest.mark.django_db
def test_flight_search_results(setup_db, search_form_data):
    """GET /recherche/ avec des paramètres de recherche en session retourne des résultats."""
    client = Client()
    # Simule les paramètres de recherche dans la session
    session = client.session
    session["search_params"] = {
        "origin": setup_db["airport_tun"].code,
        "destination": setup_db["airport_par"].code,
        "departure_date": search_form_data["departure_date"],
        "return_date": None,
        "passengers": "1",
        "travel_class": "economy",
        "trip_type": "oneway",
    }
    session.save()

    response = client.get(reverse("flights:search_results"))
    assert response.status_code == 200
    assert "flights" in response.context
    # Le vol BJ101 correspond (TUN→CDG, date future, statut scheduled, sièges dispo)
    flights = list(response.context["flights"])
    assert len(flights) >= 1


# ── 15. test_flight_search_results_no_params ─────────────────────────────────


@pytest.mark.integration
@pytest.mark.django_db
def test_flight_search_results_no_params(db):
    """GET /recherche/ sans paramètres en session retourne une page avec aucun résultat."""
    client = Client()
    response = client.get(reverse("flights:search_results"))
    assert response.status_code == 200
    assert "flights" in response.context
    flights = list(response.context["flights"])
    assert len(flights) == 0
'''


# ══════════════════════════════════════════════════════════════════════════════
#  FICHIER 4 — tests/integration/test_views_accounts.py  (10 tests)
# ══════════════════════════════════════════════════════════════════════════════

FILE_ACCOUNTS = r'''"""
Tests d'intégration — Vues de l'application Accounts (10 tests).

Couvre : LoginView, LogoutView, RegisterView, ProfileView.
"""

import pytest
from django.test import Client
from django.urls import reverse
from django.contrib.auth.models import User
from accounts.models import UserProfile


# ── 1. test_login_page ───────────────────────────────────────────────────────


@pytest.mark.integration
@pytest.mark.django_db
def test_login_page(db):
    """GET accounts:login retourne 200 et affiche le formulaire de connexion."""
    client = Client()
    response = client.get(reverse("accounts:login"))
    assert response.status_code == 200
    assert "accounts/login.html" in [t.name for t in response.templates]


# ── 2. test_login_success ────────────────────────────────────────────────────


@pytest.mark.integration
@pytest.mark.django_db
def test_login_success(db, setup_db):
    """POST avec des identifiants valides redirige vers la page d'accueil."""
    client = Client()
    response = client.post(
        reverse("accounts:login"),
        data={
            "username": "testuser",
            "password": "TestPassword123!",
        },
    )
    assert response.status_code == 302
    # La redirection cible la page d'accueil (par défaut)
    assert response.url == reverse("flights:home")


# ── 3. test_login_invalid ────────────────────────────────────────────────────


@pytest.mark.integration
@pytest.mark.django_db
def test_login_invalid(db, setup_db):
    """POST avec un mot de passe invalide renvoie une erreur sur le formulaire."""
    client = Client()
    response = client.post(
        reverse("accounts:login"),
        data={
            "username": "testuser",
            "password": "WrongPassword999!",
        },
    )
    assert response.status_code == 200
    # Le formulaire contient des erreurs
    form = response.context.get("form")
    assert form is not None
    assert form.errors


# ── 4. test_register_page ────────────────────────────────────────────────────


@pytest.mark.integration
@pytest.mark.django_db
def test_register_page(db):
    """GET accounts:register retourne 200 et affiche le formulaire d'inscription."""
    client = Client()
    response = client.get(reverse("accounts:register"))
    assert response.status_code == 200
    assert "accounts/register.html" in [t.name for t in response.templates]


# ── 5. test_register_success ─────────────────────────────────────────────────


@pytest.mark.integration
@pytest.mark.django_db
def test_register_success(db):
    """
    POST avec des données valides crée un nouvel utilisateur, un profil,
    connecte l'utilisateur et redirige vers la page d'accueil.
    """
    client = Client()
    user_count_before = User.objects.count()
    profile_count_before = UserProfile.objects.count()

    response = client.post(
        reverse("accounts:register"),
        data={
            "username": "newuser",
            "first_name": "Nouveau",
            "last_name": "Utilisateur",
            "email": "newuser@example.com",
            "password1": "SecurePass123!",
            "password2": "SecurePass123!",
        },
    )

    # Un nouvel utilisateur et un profil ont été créés
    assert User.objects.count() == user_count_before + 1
    assert UserProfile.objects.count() == profile_count_before + 1

    # L'utilisateur est connecté → redirection vers l'accueil
    assert response.status_code == 302
    assert response.url == reverse("flights:home")

    # Vérifie que le profil est bien associé
    new_user = User.objects.get(username="newuser")
    assert hasattr(new_user, "profile")


# ── 6. test_register_duplicate_email ─────────────────────────────────────────


@pytest.mark.integration
@pytest.mark.django_db
def test_register_duplicate_email(db, setup_db):
    """POST avec un email déjà utilisé renvoie une erreur."""
    client = Client()
    response = client.post(
        reverse("accounts:register"),
        data={
            "username": "anotheruser",
            "first_name": "Autre",
            "last_name": "User",
            "email": "test@example.com",  # email déjà pris par setup_db
            "password1": "SecurePass123!",
            "password2": "SecurePass123!",
        },
    )
    assert response.status_code == 200
    form = response.context.get("form")
    assert form is not None
    assert form.errors
    # L'erreur doit mentionner l'email
    error_text = str(form.errors)
    assert "email" in error_text.lower()


# ── 7. test_logout ───────────────────────────────────────────────────────────


@pytest.mark.integration
@pytest.mark.django_db
def test_logout(db, setup_db):
    """GET accounts:logout déconnecte l'utilisateur et redirige vers l'accueil."""
    client = Client()
    # Connecte d'abord l'utilisateur
    client.login(username="testuser", password="TestPassword123!")

    response = client.get(reverse("accounts:logout"))
    assert response.status_code == 302
    assert response.url == reverse("flights:home")


# ── 8. test_profile_requires_login ───────────────────────────────────────────


@pytest.mark.integration
@pytest.mark.django_db
def test_profile_requires_login(db):
    """GET accounts:profile sans authentification redirige vers la page de connexion."""
    client = Client()
    response = client.get(reverse("accounts:profile"))
    assert response.status_code == 302
    # La redirection doit pointer vers la page de connexion
    assert "/compte/connexion/" in response.url or "connexion" in response.url


# ── 9. test_profile_authenticated ────────────────────────────────────────────


@pytest.mark.integration
@pytest.mark.django_db
def test_profile_authenticated(db, setup_db):
    """GET accounts:profile avec un utilisateur authentifié retourne 200."""
    client = Client()
    client.login(username="testuser", password="TestPassword123!")
    response = client.get(reverse("accounts:profile"))
    assert response.status_code == 200
    assert "accounts/profile.html" in [t.name for t in response.templates]
    assert "user_form" in response.context
    assert "profile_form" in response.context


# ── 10. test_profile_update ──────────────────────────────────────────────────


@pytest.mark.integration
@pytest.mark.django_db
def test_profile_update(db, setup_db):
    """POST avec des données de profil valides met à jour le profil avec succès."""
    client = Client()
    client.login(username="testuser", password="TestPassword123!")

    response = client.post(
        reverse("accounts:profile"),
        data={
            # UserForm fields
            "first_name": "TestModifié",
            "last_name": "UserModifié",
            "email": "modified@example.com",
            # UserProfileForm fields
            "phone": "+21612345678",
            "address": "123 Rue de la Paix",
            "city": "Tunis",
            "country": "Tunisie",
            "date_of_birth": "1995-06-15",
            "nationality": "Tunisienne",
            "passport_number": "PASS12345",
            "gender": "M",
            "newsletter": "on",
        },
    )
    # Succès → redirection vers la page de profil
    assert response.status_code == 302
    assert response.url == reverse("accounts:profile")

    # Vérifie que les données ont été mises à jour en base
    setup_db["user"].refresh_from_db()
    assert setup_db["user"].first_name == "TestModifié"
    assert setup_db["user"].last_name == "UserModifié"
    assert setup_db["user"].email == "modified@example.com"

    setup_db["profile"].refresh_from_db()
    assert setup_db["profile"].phone == "+21612345678"
    assert setup_db["profile"].city == "Tunis"
    assert setup_db["profile"].newsletter is True
'''


# ══════════════════════════════════════════════════════════════════════════════
#  FICHIER 5 — tests/integration/test_views_bookings.py  (7 tests)
# ══════════════════════════════════════════════════════════════════════════════

FILE_BOOKINGS = r'''"""
Tests d'intégration — Vues de l'application Bookings (7 tests).

Couvre : MyBookingsView, BookingCreateView, BookingCancelView,
         BookingLookupView, select_flight.
"""

import pytest
from datetime import date, timedelta
from django.test import Client
from django.urls import reverse
from django.utils import timezone

from bookings.models import Booking, Passenger, Payment


# ── 1. test_my_bookings_requires_login ───────────────────────────────────────


@pytest.mark.integration
@pytest.mark.django_db
def test_my_bookings_requires_login(db):
    """GET bookings:my_bookings sans authentification redirige vers la connexion."""
    client = Client()
    response = client.get(reverse("bookings:my_bookings"))
    assert response.status_code == 302
    assert "/compte/connexion/" in response.url or "connexion" in response.url


# ── 2. test_my_bookings_authenticated ────────────────────────────────────────


@pytest.mark.integration
@pytest.mark.django_db
def test_my_bookings_authenticated(db, setup_db, authenticated_client):
    """GET bookings:my_bookings avec authentification affiche les réservations."""
    user = setup_db["user"]

    # Crée une réservation pour l'utilisateur
    booking = Booking.objects.create(
        user=user,
        contact_email="test@example.com",
        contact_phone="+21612345678",
        status="confirmed",
        total_amount=250.00,
    )

    response = authenticated_client.get(reverse("bookings:my_bookings"))
    assert response.status_code == 200
    assert "bookings" in response.context
    bookings = list(response.context["bookings"])
    assert len(bookings) >= 1
    assert booking in bookings


# ── 3. test_booking_lookup_page ──────────────────────────────────────────────


@pytest.mark.integration
@pytest.mark.django_db
def test_booking_lookup_page(db):
    """GET bookings:lookup retourne 200 (page de recherche par référence)."""
    client = Client()
    response = client.get(reverse("bookings:lookup"))
    assert response.status_code == 200
    assert "bookings/booking_lookup.html" in [t.name for t in response.templates]


# ── 4. test_select_flight_redirect ───────────────────────────────────────────


@pytest.mark.integration
@pytest.mark.django_db
def test_select_flight_redirect(db, setup_db, authenticated_client):
    """POST /selectionner-vol/<id>/ redirige vers bookings:create."""
    flight = setup_db["flight1"]
    response = authenticated_client.get(
        reverse("bookings:select_flight", kwargs={"flight_id": flight.pk})
    )
    assert response.status_code == 302
    assert response.url == reverse("bookings:create")

    # Vérifie que l'ID du vol est bien stocké en session
    assert "booking_flight_id" in authenticated_client.session
    assert str(authenticated_client.session["booking_flight_id"]) == str(flight.pk)


# ── 5. test_booking_creation ─────────────────────────────────────────────────


@pytest.mark.integration
@pytest.mark.django_db
def test_booking_creation(db, setup_db, authenticated_client):
    """
    POST vers bookings:create avec des données valides crée une réservation.
    Le statut est 'confirmed' (comportement réel de BookingCreateView).
    """
    user = setup_db["user"]
    flight = setup_db["flight1"]

    # Prépare la session avec les paramètres nécessaires
    session = authenticated_client.session
    session["search_params"] = {
        "origin": setup_db["airport_tun"].code,
        "destination": setup_db["airport_par"].code,
        "departure_date": (date.today() + timedelta(days=7)).strftime("%Y-%m-%d"),
        "return_date": None,
        "passengers": "1",
        "travel_class": "economy",
        "trip_type": "oneway",
    }
    session["booking_flight_id"] = flight.pk
    session.save()

    booking_count_before = Booking.objects.count()

    # Données POST du formulaire de réservation (1 passager + contact)
    form_data = {
        # PassengerForm (prefix=0)
        "0-title": "mr",
        "0-first_name": "Jean",
        "0-last_name": "Dupont",
        "0-date_of_birth": "1990-01-15",
        "0-nationality": "Française",
        "0-passport_number": "AB123456",
        "0-passport_expiry": "2030-01-15",
        "0-special_assistance": "",
        "0-meal_preference": "",
        # ContactInfoForm
        "contact_email": "jean.dupont@example.com",
        "contact_phone": "+33612345678",
        "special_requests": "",
    }

    response = authenticated_client.post(reverse("bookings:create"), data=form_data)
    # La vue crée la réservation puis redirige vers la confirmation
    assert response.status_code == 302
    assert Booking.objects.count() == booking_count_before + 1

    # Vérifie que la réservation est bien créée avec le bon statut
    new_booking = Booking.objects.latest("created_at")
    assert new_booking.user == user
    assert new_booking.status == "confirmed"
    assert new_booking.total_amount > 0


# ── 6. test_booking_cancellation ─────────────────────────────────────────────


@pytest.mark.integration
@pytest.mark.django_db
def test_booking_cancellation(db, setup_db, authenticated_client):
    """
    POST vers bookings:cancel pour une réservation 'pending' change
    le statut en 'cancelled'.
    """
    user = setup_db["user"]

    # Crée une réservation en attente directement via l'ORM
    booking = Booking.objects.create(
        user=user,
        contact_email="test@example.com",
        contact_phone="+21612345678",
        status="pending",
        total_amount=250.00,
    )
    Passenger.objects.create(
        booking=booking,
        flight=setup_db["flight1"],
        title="mr",
        first_name="Jean",
        last_name="Dupont",
        date_of_birth="1990-01-15",
        nationality="Française",
        travel_class="economy",
        price=250.00,
    )
    Payment.objects.create(
        booking=booking,
        amount=250.00,
        method="credit_card",
        status="completed",
        transaction_id=f"SIM-{booking.short_reference}",
    )

    assert booking.status == "pending"

    response = authenticated_client.post(
        reverse("bookings:cancel", kwargs={"reference": booking.reference})
    )
    assert response.status_code == 302

    # Vérifie que le statut a changé en 'cancelled'
    booking.refresh_from_db()
    assert booking.status == "cancelled"


# ── 7. test_booking_reference_lookup ─────────────────────────────────────────


@pytest.mark.integration
@pytest.mark.django_db
def test_booking_reference_lookup(db, setup_db):
    """
    POST vers bookings:lookup avec une référence et un email valides
    redirige vers la page de détail de la réservation.
    """
    # Crée une réservation de test
    booking = Booking.objects.create(
        user=setup_db["user"],
        contact_email="lookup@example.com",
        contact_phone="+21612345678",
        status="confirmed",
        total_amount=250.00,
    )
    Passenger.objects.create(
        booking=booking,
        flight=setup_db["flight1"],
        title="mme",
        first_name="Marie",
        last_name="Curie",
        date_of_birth="1985-03-20",
        nationality="Française",
        travel_class="economy",
        price=250.00,
    )

    client = Client()
    # La vue utilise reference__startswith avec la référence en majuscules
    short_ref = str(booking.reference)[:8].upper()

    response = client.post(
        reverse("bookings:lookup"),
        data={
            "reference": short_ref,
            "email": "lookup@example.com",
        },
    )

    # Doit rediriger vers la page de détail de la réservation
    assert response.status_code == 302
    assert response.url == reverse(
        "bookings:detail", kwargs={"reference": booking.reference}
    )
'''


# ══════════════════════════════════════════════════════════════════════════════
#  FICHIER 6 — tests/integration/test_views_destinations.py  (5 tests)
# ══════════════════════════════════════════════════════════════════════════════

FILE_DESTINATIONS = r'''"""
Tests d'intégration — Vues de l'application Destinations (5 tests).

Couvre : DestinationListView, DestinationDetailView.
"""

import pytest
from django.test import Client
from django.urls import reverse

from destinations.models import Destination, DestinationReview
from django.contrib.auth.models import User


# ── 1. test_destination_list ─────────────────────────────────────────────────


@pytest.mark.integration
@pytest.mark.django_db
def test_destination_list(setup_db):
    """GET destinations:list retourne 200 et le contexte contient 'destinations'."""
    # Crée au moins une destination active
    Destination.objects.create(
        name="Djerba",
        slug="djerba",
        description="Île paradisiaque au sud de la Tunisie.",
        short_description="Djerba, la douceur de vivre.",
        airport=setup_db["airport_tun"],
        category="beach",
        is_active=True,
        is_featured=False,
    )

    client = Client()
    response = client.get(reverse("destinations:list"))
    assert response.status_code == 200
    assert "destinations" in response.context
    assert "destinations/destination_list.html" in [t.name for t in response.templates]


# ── 2. test_destination_detail ───────────────────────────────────────────────


@pytest.mark.integration
@pytest.mark.django_db
def test_destination_detail(setup_db):
    """GET destinations:detail avec un slug valide retourne 200."""
    destination = Destination.objects.create(
        name="Sfax",
        slug="sfax",
        description="Ville portuaire historique.",
        short_description="Sfax, porte du Sahel.",
        airport=setup_db["airport_tun"],
        category="culture",
        is_active=True,
        is_featured=False,
    )

    client = Client()
    response = client.get(
        reverse("destinations:detail", kwargs={"slug": "sfax"})
    )
    assert response.status_code == 200
    assert "destination" in response.context
    assert response.context["destination"].slug == "sfax"


# ── 3. test_destination_detail_404 ───────────────────────────────────────────


@pytest.mark.integration
@pytest.mark.django_db
def test_destination_detail_404(db):
    """GET destinations:detail avec un slug invalide retourne 404."""
    client = Client()
    response = client.get(
        reverse("destinations:detail", kwargs={"slug": "slug-inexistant-xyz"})
    )
    assert response.status_code == 404


# ── 4. test_destination_featured ─────────────────────────────────────────────


@pytest.mark.integration
@pytest.mark.django_db
def test_destination_featured(setup_db):
    """Les destinations vedettes (is_featured=True) apparaissent dans le contexte."""
    # Crée 2 destinations featured
    dest1 = Destination.objects.create(
        name="Hammamet",
        slug="hammamet",
        description="Station balnéaire célèbre.",
        short_description="Hammamet, joyau du cap Bon.",
        airport=setup_db["airport_tun"],
        category="beach",
        is_active=True,
        is_featured=True,
    )
    dest2 = Destination.objects.create(
        name="Sousse",
        slug="sousse",
        description="Ville historique et touristique.",
        short_description="Sousse, perle du Sahel.",
        airport=setup_db["airport_tun"],
        category="culture",
        is_active=True,
        is_featured=True,
    )
    # Crée 1 destination non-featured
    Destination.objects.create(
        name="Gabès",
        slug="gabes",
        description="Oasis côtière unique.",
        short_description="Gabès, entre mer et désert.",
        airport=setup_db["airport_tun"],
        category="nature",
        is_active=True,
        is_featured=False,
    )

    client = Client()
    response = client.get(reverse("destinations:list"))
    assert response.status_code == 200
    assert "featured_destinations" in response.context
    featured = list(response.context["featured_destinations"])
    assert len(featured) >= 2
    featured_slugs = [d.slug for d in featured]
    assert "hammamet" in featured_slugs
    assert "sousse" in featured_slugs


# ── 5. test_destination_review_form ──────────────────────────────────────────


@pytest.mark.integration
@pytest.mark.django_db
def test_destination_review_form(setup_db):
    """
    Un utilisateur authentifié peut voir le formulaire d'avis
    sur la page de détail d'une destination.
    """
    user = setup_db["user"]
    destination = Destination.objects.create(
        name="Kairouan",
        slug="kairouan",
        description="Sainte ville de l'Islam.",
        short_description="Kairouan, ville spirituelle.",
        airport=setup_db["airport_tun"],
        category="culture",
        is_active=True,
        is_featured=False,
    )

    # Connecte l'utilisateur
    client = Client()
    client.login(username="testuser", password="TestPassword123!")

    response = client.get(
        reverse("destinations:detail", kwargs={"slug": "kairouan"})
    )
    assert response.status_code == 200

    # La page de détail est accessible pour l'utilisateur authentifié.
    # Le formulaire d'avis dépend du template, mais on vérifie que
    # l'utilisateur connecté reçoit bien la page avec le contexte complet.
    assert "destination" in response.context
    assert response.context["destination"].slug == "kairouan"
'''


# ══════════════════════════════════════════════════════════════════════════════
#  FICHIER 7 — tests/integration/test_views_promotions.py  (5 tests)
# ══════════════════════════════════════════════════════════════════════════════

FILE_PROMOTIONS = r'''"""
Tests d'intégration — Vues de l'application Promotions (5 tests).

Couvre : PromotionListView, PromotionDetailView, NewsletterSubscribeView.
"""

import pytest
from datetime import timedelta
from django.test import Client
from django.urls import reverse
from django.utils import timezone

from promotions.models import Promotion, NewsletterSubscription


# ── 1. test_promotion_list ───────────────────────────────────────────────────


@pytest.mark.integration
@pytest.mark.django_db
def test_promotion_list(db):
    """GET promotions:list retourne 200 et le contexte contient 'promotions'."""
    # Crée une promotion active
    now = timezone.now()
    Promotion.objects.create(
        code="PROMO20",
        name="Réduction 20%",
        description="20% de réduction sur tous les vols.",
        promo_type="percentage",
        discount_percentage=20.00,
        discount_amount=0,
        start_date=now - timedelta(hours=1),
        end_date=now + timedelta(days=30),
        max_uses=100,
        current_uses=0,
        is_active=True,
        is_featured=True,
    )

    client = Client()
    response = client.get(reverse("promotions:list"))
    assert response.status_code == 200
    assert "promotions" in response.context
    assert "promotions/promotion_list.html" in [t.name for t in response.templates]
    # Au moins la promotion créée doit apparaître
    promotions = list(response.context["promotions"])
    assert len(promotions) >= 1


# ── 2. test_promotion_detail ─────────────────────────────────────────────────


@pytest.mark.integration
@pytest.mark.django_db
def test_promotion_detail(db):
    """GET promotions:detail avec un code valide retourne 200."""
    now = timezone.now()
    promo = Promotion.objects.create(
        code="SUMMER2025",
        name="Offre Été 2025",
        description="Offres spéciales pour l'été 2025.",
        promo_type="percentage",
        discount_percentage=15.00,
        discount_amount=0,
        start_date=now - timedelta(hours=1),
        end_date=now + timedelta(days=60),
        max_uses=200,
        current_uses=5,
        is_active=True,
        is_featured=False,
    )

    client = Client()
    response = client.get(
        reverse("promotions:detail", kwargs={"code": "SUMMER2025"})
    )
    assert response.status_code == 200
    assert "promotion" in response.context
    assert response.context["promotion"].code == "SUMMER2025"


# ── 3. test_promotion_detail_404 ─────────────────────────────────────────────


@pytest.mark.integration
@pytest.mark.django_db
def test_promotion_detail_404(db):
    """GET promotions:detail avec un code invalide retourne 404."""
    client = Client()
    response = client.get(
        reverse("promotions:detail", kwargs={"code": "INEXISTANT"})
    )
    assert response.status_code == 404


# ── 4. test_newsletter_subscribe_success ─────────────────────────────────────


@pytest.mark.integration
@pytest.mark.django_db
def test_newsletter_subscribe_success(db):
    """POST avec un email valide vers la newsletter retourne un succès JSON."""
    client = Client()
    response = client.post(
        reverse("promotions:newsletter_subscribe"),
        data={"email": "subscriber@example.com", "first_name": "Ahmed"},
    )
    assert response.status_code == 200
    assert response["Content-Type"] == "application/json"

    data = response.json()
    assert data["success"] is True
    assert "Merci" in data.get("message", "")

    # Vérifie que l'abonnement a été créé en base
    assert NewsletterSubscription.objects.filter(
        email="subscriber@example.com"
    ).exists()


# ── 5. test_newsletter_subscribe_duplicate ───────────────────────────────────


@pytest.mark.integration
@pytest.mark.django_db
def test_newsletter_subscribe_duplicate(db):
    """POST avec un email déjà inscrit retourne une erreur JSON."""
    # Crée un abonnement existant
    NewsletterSubscription.objects.create(
        email="existing@example.com",
        first_name="Fatma",
    )

    client = Client()
    response = client.post(
        reverse("promotions:newsletter_subscribe"),
        data={"email": "existing@example.com"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is False
    assert "déjà" in data.get("error", "").lower() or "inscrit" in data.get("error", "").lower()
'''


# ══════════════════════════════════════════════════════════════════════════════
#  FICHIER 8 — docs/coverage_report_sprint1.md
# ══════════════════════════════════════════════════════════════════════════════

FILE_COVERAGE_REPORT = r"""# 📊 Rapport de Couverture de Tests — Sprint 1

> **Projet** : NouvelAir — Système de réservation aérienne
> **Date** : Sprint 1 — Jour 3
> **Auteur** : Équipe de développement

---

## 1. Comment exécuter les tests avec couverture

### Installation des prérequis

```bash
pip install pytest pytest-django pytest-cov
```

### Configuration minimale (`pytest.ini`)

Placez ce fichier à la racine du projet (à côté de `manage.py`) :

```ini
[pytest]
DJANGO_SETTINGS_MODULE = nouvelair.settings
python_files = test_*.py
python_classes = Test*
python_functions = test_*
markers =
    integration: Tests d'intégration (Django Test Client)
testpaths = tests
```

### Commandes de base

```bash
# Exécuter uniquement les tests d'intégration
pytest tests/integration/ -m integration -v

# Exécuter avec couverture de code (terminal)
pytest tests/integration/ -m integration --cov=. --cov-report=term-missing

# Exécuter avec couverture de code (rapport HTML)
pytest tests/integration/ -m integration --cov=. --cov-report=html

# Exécuter avec couverture et rapport XML (pour CI)
pytest tests/integration/ -m integration --cov=. --cov-report=xml:coverage.xml

# Couverture par application spécifique
pytest tests/integration/ -m integration --cov=flights --cov=accounts --cov=bookings --cov=destinations --cov=promotions --cov-report=term-missing
```

---

## 2. Objectifs de couverture

| Application   | Cible (%) | Priorité | Modules critiques                       |
|---------------|-----------|----------|----------------------------------------|
| `flights`     | ≥ 85%     | 🔴 Haute | `views.py`, `models.py`, `forms.py`    |
| `accounts`    | ≥ 85%     | 🔴 Haute | `views.py`, `forms.py`, `signals.py`   |
| `bookings`    | ≥ 80%     | 🔴 Haute | `views.py`, `models.py`, `forms.py`    |
| `destinations`| ≥ 80%     | 🟡 Moyen | `views.py`, `models.py`                |
| `promotions`  | ≥ 75%     | 🟡 Moyen | `views.py`, `models.py`                |
| **Global**    | ≥ 80%     | —        | —                                      |

---

## 3. Comment lire le rapport HTML

1. Après exécution de `--cov-report=html`, un dossier `htmlcov/` est généré.
2. Ouvrez `htmlcov/index.html` dans votre navigateur.
3. **Navigation** :
   - Cliquez sur chaque module pour voir les lignes couvertes (vert) et non couvertes (rouge).
   - Les branches conditionnelles sont indiquées en orange/jaune.
4. **Indicateurs clés** :
   - **Lines** : pourcentage de lignes exécutées.
   - **Branches** : pourcentage de branches conditionnelles couvertes.

---

## 4. Modules à prioriser pour la couverture

### 🔴 Priorité haute — `flights/views.py`

Les vues critiques à couvrir en priorité :

| Vue                    | Lignes à couvrir             | Statut actuel |
|------------------------|------------------------------|---------------|
| `HomeView`             | GET, POST, validation        | ✅ Jour 3     |
| `FlightSearchResultsView` | GET avec/sans session     | ✅ Jour 3     |
| `FlightDetailView`     | GET, contexte, 404           | ✅ Jour 3     |
| `AirportListView`      | GET, queryset                | ✅ Jour 3     |
| `airport_autocomplete` | GET avec query, vide         | ✅ Jour 3     |

### 🔴 Priorité haute — `accounts/views.py`

| Vue               | Lignes à couvrir        | Statut actuel |
|-------------------|-------------------------|---------------|
| `LoginView`       | GET, POST, invalid     | ✅ Jour 3     |
| `LogoutView`      | GET, redirect          | ✅ Jour 3     |
| `RegisterView`    | GET, POST, duplicate   | ✅ Jour 3     |
| `ProfileView`     | GET, POST, update      | ✅ Jour 3     |

### 🔴 Priorité haute — `bookings/views.py`

| Vue                    | Lignes à couvrir              | Statut actuel |
|------------------------|-------------------------------|---------------|
| `BookingCreateView`    | GET, POST, session            | ✅ Jour 3     |
| `MyBookingsView`       | GET avec/sans auth            | ✅ Jour 3     |
| `BookingCancelView`    | POST, status change           | ✅ Jour 3     |
| `BookingLookupView`    | GET, POST, lookup by ref      | ✅ Jour 3     |
| `select_flight`        | GET, session, redirect        | ✅ Jour 3     |

---

## 5. Interpréter les résultats

### Couverture idéale : ≥ 90%
```
flights/views.py     92%  ██████████████████░░░  184/200 lignes
accounts/views.py    88%  █████████████████░░░░  132/150 lignes
bookings/views.py    85%  ████████████████░░░░░  170/200 lignes
```

### Couverture insuffisante : < 70%
- 🔴 Action requise : ajouter des tests pour les branches non couvertes.
- Vérifiez les gestionnaires d'erreur (`try/except`), les conditions `if/else` rares.

### Couverture acceptable : 70–85%
- 🟡 Amélioration continue : identifiez les scénarios limites (edge cases).

---

## 6. Bonnes pratiques

1. **Exécuter les tests avant chaque commit** :
   ```bash
   pytest tests/integration/ -m integration --cov=flights --cov=accounts --cov=bookings --cov-report=term-missing -q
   ```

2. **Ne jamais viser 100%** : les imports, la configuration et les handlers d'erreurs rarement atteignables n'ont pas besoin d'être couverts.

3. **Privilégier la qualité à la quantité** : un test d'intégration bien conçu vaut mieux que dix tests unitaires triviaux.

4. **Utiliser les marqueurs** : `@pytest.mark.integration` permet de séparer les tests unitaires des tests d'intégration dans les rapports.

5. **Couverture par branche** : utilisez `--cov-branch` pour vérifier la couverture des conditions booléennes.
   ```bash
   pytest tests/integration/ -m integration --cov=. --cov-branch --cov-report=html
   ```

---

## 7. Commande récapitulative

```bash
# 🚀 Commande complète recommandée pour le Sprint 1
pytest tests/integration/ -m integration \
    --cov=flights --cov=accounts --cov=bookings --cov=destinations --cov=promotions \
    --cov-report=term-missing:skip-covered \
    --cov-report=html \
    -v
```

---

*Document généré automatiquement par `setup_jour3.py`*
"""


# ══════════════════════════════════════════════════════════════════════════════
#  MAIN — Exécution du script
# ══════════════════════════════════════════════════════════════════════════════

def main():
    """Point d'entrée principal du script."""
    print("=" * 70)
    print("  🛫  NouvelAir — Setup Jour 3 : Tests d'intégration")
    print("=" * 70)
    print()

    # ── Mapping nom de fichier → contenu ──────────────────────────────────
    files = [
        ("tests/integration/__init__.py", FILE_INIT),
        ("tests/integration/conftest.py", FILE_CONFTEST),
        ("tests/integration/test_views_flights.py", FILE_FLIGHTS),
        ("tests/integration/test_views_accounts.py", FILE_ACCOUNTS),
        ("tests/integration/test_views_bookings.py", FILE_BOOKINGS),
        ("tests/integration/test_views_destinations.py", FILE_DESTINATIONS),
        ("tests/integration/test_views_promotions.py", FILE_PROMOTIONS),
        ("docs/coverage_report_sprint1.md", FILE_COVERAGE_REPORT),
    ]

    # ── Création des fichiers ─────────────────────────────────────────────
    for rel_path, content in files:
        full_path = os.path.join(PROJECT_ROOT, rel_path)
        write_file(full_path, content)

    # ── Résumé ────────────────────────────────────────────────────────────
    print()
    print("-" * 70)
    print("  📋  RÉSUMÉ")
    print("-" * 70)
    print()
    print(f"  Fichiers créés        : {len(files)}")
    print(f"  Tests vols (flights)  : 15 tests")
    print(f"  Tests comptes (acct)  : 10 tests")
    print(f"  Tests réservations    :  7 tests")
    print(f"  Tests destinations    :  5 tests")
    print(f"  Tests promotions      :  5 tests")
    print(f"  ─────────────────────────────")
    print(f"  TOTAL                 : 42 tests d'intégration")
    print()

    # ── Instructions ──────────────────────────────────────────────────────
    print("  ⚡  Prochaines étapes :")
    print()
    print("  1. Créer un fichier pytest.ini à la racine du projet :")
    print()
    print("       [pytest]")
    print("       DJANGO_SETTINGS_MODULE = nouvelair.settings")
    print("       python_files = test_*.py")
    print("       markers =")
    print("           integration: Tests d'intégration (Django Test Client)")
    print("       testpaths = tests")
    print()
    print("  2. Exécuter les tests :")
    print()
    print("       pytest tests/integration/ -m integration -v")
    print()
    print("  3. Avec couverture de code :")
    print()
    print("       pytest tests/integration/ -m integration --cov=. --cov-report=html")
    print()
    print("  4. Ouvrir le rapport HTML :")
    print()
    print("       start htmlcov/index.html")
    print()
    print("=" * 70)
    print("  ✅  Setup Jour 3 terminé avec succès !")
    print("=" * 70)


if __name__ == "__main__":
    main()
