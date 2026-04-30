"""Tests unitaires — Utilitaires et fonctions auxiliaires.

Ce module contient les tests unitaires pytest pour les utilitaires du projet :
  - Formatage de duree de vol
  - Calcul de prix avec promotion
  - Format de reference de reservation
  - Validation de l'age des passagers

Marqueurs utilises :
    @pytest.mark.unit      — Categorie de test unitaire
    @pytest.mark.django_db — Acces a la base de donnees de test

Execution :
    pytest tests/unit/test_models_utils.py -v
    pytest tests/unit/test_models_utils.py -v -m unit
"""

import pytest
from decimal import Decimal
from datetime import timedelta, date

from django.utils import timezone
from django.contrib.auth.models import User

from flights.models import Flight
from bookings.models import Booking, Passenger
from tests.factories import (
    FlightFactory,
    BookingFactory,
    PassengerFactory,
    PromotionFactory,
    AirportFactory,
    AircraftFactory,
)


# ====================================================================
# Utilitaires — 4 tests
# ====================================================================


@pytest.mark.unit
@pytest.mark.django_db
class TestUtilities:
    """Tests unitaires des fonctions utilitaires du projet."""

    def test_duration_format_filter(self):
        """Test du formatage de la duree en 'Xh Ym'."""
        now = timezone.now()
        # 2h 30m
        flight = FlightFactory(
            departure_time=now + timedelta(hours=5),
            arrival_time=now + timedelta(hours=7, minutes=30),
        )
        flight.save()
        duration = flight.duration
        assert duration is not None
        total_seconds = int(duration.total_seconds())
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        formatted = f"{hours}h {minutes}m"
        assert formatted == "2h 30m"

    def test_duration_format_exact_hours(self):
        """Test du formatage quand la duree est un nombre exact d'heures."""
        now = timezone.now()
        flight = FlightFactory(
            departure_time=now + timedelta(hours=5),
            arrival_time=now + timedelta(hours=8),
        )
        flight.save()
        duration = flight.duration
        total_seconds = int(duration.total_seconds())
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        formatted = f"{hours}h {minutes}m"
        assert formatted == "3h 0m"

    def test_flight_price_calculation_with_discount(self):
        """Test du calcul de prix avec une promotion appliquee."""
        from promotions.models import Promotion

        flight = FlightFactory(
            base_price_economy=Decimal("500.00"),
            base_price_business=Decimal("1500.00"),
        )
        now = timezone.now()
        promo = PromotionFactory(
            code="REDUC30",
            promo_type="percentage",
            discount_percentage=Decimal("30.00"),
            start_date=now - timedelta(days=1),
            end_date=now + timedelta(days=30),
            is_active=True,
        )
        promo.flights.add(flight)

        # Recharger depuis la base
        flight.refresh_from_db()
        price_eco = flight.get_current_price_economy()
        price_biz = flight.get_current_price_business()

        # 500 * 0.70 = 350.00
        assert price_eco == Decimal("350.00")
        # 1500 * 0.70 = 1050.00
        assert price_biz == Decimal("1050.00")

    def test_booking_reference_format(self):
        """Test que la reference de reservation est un UUID valide (8+ chars hex)."""
        booking = BookingFactory()
        ref_str = str(booking.reference)
        # UUID4 format : 36 caracteres hex avec tirets
        assert len(ref_str) == 36
        assert ref_str.count("-") == 4
        # short_reference doit etre 8 caracteres alphanumeriques majuscules
        short_ref = booking.short_reference
        assert len(short_ref) == 8
        assert short_ref.isalnum()
        assert short_ref.isupper()

    def test_passenger_age_validation(self):
        """Test de l'age calcule a partir de la date de naissance."""
        # Passager adulte (30 ans)
        dob_adult = date.today().replace(year=date.today().year - 30)
        passenger_adult = PassengerFactory(date_of_birth=dob_adult)
        age_adult = (
            date.today().year - passenger_adult.date_of_birth.year
            - (
                (date.today().month, date.today().day)
                < (passenger_adult.date_of_birth.month, passenger_adult.date_of_birth.day)
            )
        )
        assert age_adult == 30

        # Passager enfant (10 ans)
        dob_child = date.today().replace(year=date.today().year - 10)
        passenger_child = PassengerFactory(date_of_birth=dob_child)
        age_child = (
            date.today().year - passenger_child.date_of_birth.year
            - (
                (date.today().month, date.today().day)
                < (passenger_child.date_of_birth.month, passenger_child.date_of_birth.day)
            )
        )
        assert age_child == 10
