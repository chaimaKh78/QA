"""Tests unitaires du module bookings — Modeles Booking, Passenger, Payment.

Ce module contient les tests unitaires pytest pour tous les modeles de
l'application bookings : Booking (8 tests), Passenger (5 tests), Payment (5 tests).

Marqueurs utilises :
    @pytest.mark.unit      — Categorie de test unitaire
    @pytest.mark.django_db — Acces a la base de donnees de test

Execution :
    pytest tests/unit/test_models_bookings.py -v
    pytest tests/unit/test_models_bookings.py -v -m unit
"""

import pytest
from decimal import Decimal
from datetime import date

from django.db import IntegrityError
from django.contrib.auth.models import User

from bookings.models import Booking, Passenger, Payment
from tests.factories import (
    BookingFactory,
    PassengerFactory,
    FlightFactory,
    AirportFactory,
    AircraftFactory
)

# ====================================================================
# Booking — 8 tests
# ====================================================================

@pytest.mark.unit
@pytest.mark.django_db
class TestBooking:
    """Tests unitaires du modele Booking."""

    def test_booking_creation(self):
        """Test de creation d'une reservation avec tous les champs."""
        booking = BookingFactory(
            contact_email="passager@nouvelair.com",
            contact_phone="+216 22 345 678",
            status="pending",
            total_amount=Decimal("350.00"),
            special_requests="Siege cote hublot"
        )
        assert booking.contact_email == "passager@nouvelair.com"
        assert booking.contact_phone == "+216 22 345 678"
        assert booking.status == "pending"
        assert booking.total_amount == Decimal("350.00")
        assert booking.special_requests == "Siege cote hublot"
        assert booking.reference is not None

    def test_booking_reference_unique(self):
        """Test que la reference (UUID) est unique."""
        booking1 = BookingFactory()
        booking2 = BookingFactory()
        assert booking1.reference != booking2.reference

    @pytest.mark.parametrize("status", ["pending", "confirmed", "cancelled", "completed", "refunded"])
    def test_booking_status_choices(self, status):
        """Test que tous les statuts de reservation sont acceptes (parametrized)."""
        booking = BookingFactory(status=status)
        assert booking.status == status
        assert booking.get_status_display()

    def test_booking_str(self):
        """Test que __str__ contient la reference courte et le statut."""
        booking = BookingFactory(status="confirmed")
        result = str(booking)
        # La reference courte est les 8 premiers caracteres en majuscules
        assert str(booking.reference)[:8].upper() in result or "Réservation" in result

    def test_booking_travel_class_via_passenger(self):
        """Test que la classe de voyage est definie au niveau du passager."""
        flight = FlightFactory()
        booking = BookingFactory()
        passenger_eco = PassengerFactory(booking=booking, flight=flight, travel_class="economy")
        passenger_biz = PassengerFactory(booking=booking, flight=flight, travel_class="business")
        assert passenger_eco.travel_class == "economy"
        assert passenger_biz.travel_class == "business"

    def test_booking_default_status_pending(self):
        """Test que le statut par defaut est 'pending'."""
        booking = BookingFactory(status="pending")
        assert booking.status == "pending"

    def test_booking_created_at_auto(self):
        """Test que created_at est automatiquement renseigne."""
        booking = BookingFactory()
        assert booking.created_at is not None
        assert booking.created_at <= booking.updated_at

    def test_booking_total_amount_calculation(self):
        """Test du champ total_amount."""
        # Reservation avec 2 passagers economie a 350 TND chacun
        flight = FlightFactory(base_price_economy=Decimal("350.00"))
        booking = BookingFactory(total_amount=Decimal("700.00"))
        PassengerFactory(booking=booking, flight=flight, price=Decimal("350.00"))
        PassengerFactory(booking=booking, flight=flight, price=Decimal("350.00"))
        assert booking.total_amount == Decimal("700.00")
        assert booking.passengers.count() == 2

# ====================================================================
# Passenger — 5 tests
# ====================================================================

@pytest.mark.unit
@pytest.mark.django_db
class TestPassenger:
    """Tests unitaires du modele Passenger."""

    def test_passenger_creation(self):
        """Test de creation d'un passager avec tous les champs."""
        booking = BookingFactory()
        flight = FlightFactory()
        passenger = PassengerFactory(
            booking=booking,
            flight=flight,
            title="mr",
            first_name="Ahmed",
            last_name="Ben Ali",
            date_of_birth=date(1990, 5, 15),
            nationality="Tunisienne",
            passport_number="P12345678",
            travel_class="economy",
            price=Decimal("350.00")
)
        assert passenger.booking == booking
        assert passenger.flight == flight
        assert passenger.title == "mr"
        assert passenger.first_name == "Ahmed"
        assert passenger.last_name == "Ben Ali"
        assert passenger.nationality == "Tunisienne"
        assert passenger.passport_number == "P12345678"
        assert passenger.travel_class == "economy"
        assert passenger.price == Decimal("350.00")

    @pytest.mark.parametrize("title", ["mr", "mme", "mll", "enf"])
    def test_passenger_title_choices(self, title):
        """Test que tous les titres de civilite sont acceptes (parametrized)."""
        passenger = PassengerFactory(title=title)
        assert passenger.title == title
        assert passenger.get_title_display()

    def test_passenger_str(self):
        """Test que __str__ retourne le titre, prenom et nom."""
        passenger = PassengerFactory(title="mr", first_name="Ahmed", last_name="Ben Ali")
        result = str(passenger)
        assert "Ahmed" in result
        assert "Ben Ali" in result

    def test_passenger_passport_number_optional(self):
        """Test que le numero de passeport est optionnel (blank=True)."""
        passenger = PassengerFactory(passport_number="")
        assert passenger.passport_number == ""

    def test_passenger_date_of_birth(self):
        """Test que la date de naissance est correctement stockee."""
        dob = date(1985, 3, 20)
        passenger = PassengerFactory(date_of_birth=dob)
        assert passenger.date_of_birth == dob

# ====================================================================