"""
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
    assert "/login/" in response.url or "login" in response.url or "connexion" in response.url


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
