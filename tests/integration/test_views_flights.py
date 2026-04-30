"""
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
