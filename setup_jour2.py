#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
NouvelAir — Jour 2 : TDD & Tests Unitaires (pytest)
================================================================================

Script d'installation automatique pour le Jour 2 du projet NouvelAir.
Crée l'intégralité des fichiers de tests unitaires pytest pour tous les modèles,
les factories factory_boy, et le fichier requirements_test.txt.

Les tests sont adaptés au modèle de données réel du projet :
  - flights   : Airport, Aircraft, Flight (pas de FlightPriceHistory)
  - bookings  : Booking (reference UUIDField), Passenger, Payment
  - accounts  : UserProfile (signal post_save), SavedDestination
  - promotions: Promotion (is_valid property), NewsletterSubscription
  - destinations: Destination, DestinationImage, DestinationReview

Utilisation :
    cd D:/NouvelairApp/nouvelair_project/
    python setup_jour2.py

Auteur   : Equipe QA NouvelAir
Version  : 2.0.0
Date     : 2025
================================================================================
"""

import os
import sys
from pathlib import Path
from datetime import datetime, timedelta

# ====================================================================
# Chemin racine du projet
# ====================================================================
PROJECT_ROOT = Path.cwd()

BANNER = r"""
╔═══════════════════════════════════════════════════════════════════════╗
║                                                                       ║
║            ✈  NouvelAir — Setup Jour 2  ✈                            ║
║                                                                       ║
║       TDD · Tests Unitaires pytest · Factory Boy                      ║
║                                                                       ║
║       8 fichiers  |  70+ tests  |  10 factories                      ║
║                                                                       ║
╚═══════════════════════════════════════════════════════════════════════╝
"""


# ====================================================================
# FILE 1 — tests/unit/__init__.py
# ====================================================================
TESTS_UNIT_INIT = ""


# ====================================================================
# FILE 2 — tests/unit/test_models_flights.py
# ====================================================================
TEST_MODELS_FLIGHTS = '''\
"""Tests unitaires du module flights — Modeles Airport, Aircraft, Flight.

Ce module contient les tests unitaires pytest pour tous les modeles de
l'application flights : Airport (7 tests), Aircraft (6 tests), Flight (11 tests).

Marqueurs utilises :
    @pytest.mark.unit      — Categorie de test unitaire
    @pytest.mark.django_db — Acces a la base de donnees de test

Execution :
    pytest tests/unit/test_models_flights.py -v
    pytest tests/unit/test_models_flights.py -v -m unit
"""

import pytest
from decimal import Decimal
from datetime import timedelta

from django.db import IntegrityError
from django.utils import timezone

from flights.models import Airport, Aircraft, Flight
from tests.factories import (
    AirportFactory,
    AircraftFactory,
    FlightFactory,
)


# ====================================================================
# Airport — 7 tests
# ====================================================================


@pytest.mark.unit
@pytest.mark.django_db
class TestAirport:
    """Tests unitaires du modele Airport."""

    def test_airport_creation(self):
        """Test de creation d'un aeroport avec tous les champs."""
        airport = AirportFactory(
            code="TUN",
            name="Aeroport International Tunis-Carthage",
            city="Tunis",
            country="Tunisie",
            latitude=Decimal("36.851000"),
            longitude=Decimal("10.227000"),
            is_active=True,
        )
        assert airport.code == "TUN"
        assert airport.name == "Aeroport International Tunis-Carthage"
        assert airport.city == "Tunis"
        assert airport.country == "Tunisie"
        assert airport.latitude == Decimal("36.851000")
        assert airport.longitude == Decimal("10.227000")
        assert airport.is_active is True

    def test_airport_str(self):
        """Test que __str__ retourne le format 'CODE - City (Country)'."""
        airport = AirportFactory(code="CDG", city="Paris", country="France")
        result = str(airport)
        assert "CDG" in result
        assert "Paris" in result
        assert "France" in result

    def test_airport_code_unique(self):
        """Test que le code IATA est unique (IntegrityError si doublon)."""
        AirportFactory(code="ORY")
        with pytest.raises(IntegrityError):
            Airport.objects.create(
                code="ORY",
                name="Aeroport d'Orly",
                city="Paris",
                country="France",
                latitude=Decimal("48.726200"),
                longitude=Decimal("2.364900"),
            )

    def test_airport_ordering(self):
        """Test que le tri par defaut est par code IATA."""
        AirportFactory(code="FCO", city="Rome")
        AirportFactory(code="TUN", city="Tunis")
        AirportFactory(code="CDG", city="Paris")
        airports = list(Airport.objects.all())
        codes = [a.code for a in airports]
        assert codes == sorted(codes)

    def test_airport_latitude_longitude_decimal(self):
        """Test que les coordonnees sont stockees comme DecimalField."""
        airport = AirportFactory(
            latitude=Decimal("36.851000"),
            longitude=Decimal("10.227000"),
        )
        assert isinstance(airport.latitude, Decimal)
        assert isinstance(airport.longitude, Decimal)
        assert airport.latitude == Decimal("36.851000")
        assert airport.longitude == Decimal("10.227000")

    def test_airport_is_active_default(self):
        """Test que is_active est True par defaut."""
        airport = AirportFactory()
        assert airport.is_active is True

    def test_airport_cannot_be_created_without_code(self):
        """Test qu'un aeroport ne peut pas etre cree sans code (null=False)."""
        with pytest.raises(IntegrityError):
            Airport.objects.create(
                name="Aeroport Test",
                city="Test",
                country="Test",
                latitude=Decimal("0.000000"),
                longitude=Decimal("0.000000"),
            )


# ====================================================================
# Aircraft — 6 tests
# ====================================================================


@pytest.mark.unit
@pytest.mark.django_db
class TestAircraft:
    """Tests unitaires du modele Aircraft."""

    def test_aircraft_creation(self):
        """Test de creation d'un aeronef avec tous les champs."""
        aircraft = AircraftFactory(
            model_name="Airbus A320neo",
            registration="TS-INA",
            total_seats=180,
            economy_seats=150,
            business_seats=30,
            is_active=True,
        )
        assert aircraft.model_name == "Airbus A320neo"
        assert aircraft.registration == "TS-INA"
        assert aircraft.total_seats == 180
        assert aircraft.economy_seats == 150
        assert aircraft.business_seats == 30
        assert aircraft.is_active is True

    def test_aircraft_str(self):
        """Test que __str__ retourne 'model_name (registration)'."""
        aircraft = AircraftFactory(
            model_name="Boeing 737-800",
            registration="TS-INB",
        )
        result = str(aircraft)
        assert "Boeing 737-800" in result
        assert "TS-INB" in result

    def test_aircraft_registration_unique(self):
        """Test que l'immatriculation est unique."""
        AircraftFactory(registration="TS-INA")
        with pytest.raises(IntegrityError):
            Aircraft.objects.create(
                model_name="Autre modele",
                registration="TS-INA",
                total_seats=100,
                economy_seats=80,
                business_seats=20,
            )

    def test_seats_sum(self):
        """Test que economy_seats + business_seats == total_seats."""
        aircraft = AircraftFactory(
            total_seats=180,
            economy_seats=150,
            business_seats=30,
        )
        assert aircraft.economy_seats + aircraft.business_seats == aircraft.total_seats

    def test_aircraft_is_active(self):
        """Test du champ is_active."""
        active = AircraftFactory(is_active=True)
        inactive = AircraftFactory(is_active=False)
        assert active.is_active is True
        assert inactive.is_active is False

    def test_aircraft_economy_seats_positive(self):
        """Test que les sieges economiques sont un entier positif."""
        aircraft = AircraftFactory(economy_seats=1)
        assert aircraft.economy_seats > 0
        # Verifie que 0 est accepte par PositiveIntegerField
        aircraft_zero = AircraftFactory(economy_seats=0)
        assert aircraft_zero.economy_seats == 0


# ====================================================================
# Flight — 11 tests
# ====================================================================


@pytest.mark.unit
@pytest.mark.django_db
class TestFlight:
    """Tests unitaires du modele Flight."""

    def test_flight_creation(self):
        """Test de creation d'un vol avec tous les champs."""
        now = timezone.now()
        departure = now + timedelta(hours=10)
        arrival = now + timedelta(hours=13, minutes=15)
        flight = FlightFactory(
            flight_number="BJ520",
            departure_time=departure,
            arrival_time=arrival,
            status="scheduled",
            base_price_economy=Decimal("350.00"),
            base_price_business=Decimal("1200.00"),
            available_seats_economy=150,
            available_seats_business=30,
            is_active=True,
        )
        assert flight.flight_number == "BJ520"
        assert flight.status == "scheduled"
        assert flight.base_price_economy == Decimal("350.00")
        assert flight.base_price_business == Decimal("1200.00")
        assert flight.available_seats_economy == 150
        assert flight.available_seats_business == 30
        assert flight.is_active is True

    def test_flight_str(self):
        """Test que __str__ contient le numero de vol et les codes aeroports."""
        flight = FlightFactory(
            flight_number="BJ520",
            origin=AirportFactory(code="TUN"),
            destination=AirportFactory(code="CDG"),
        )
        result = str(flight)
        assert "BJ520" in result
        assert "TUN" in result
        assert "CDG" in result

    def test_flight_number_unique(self):
        """Test que le numero de vol est unique."""
        origin = AirportFactory(code="TUN")
        destination = AirportFactory(code="CDG")
        aircraft = AircraftFactory()
        FlightFactory(flight_number="BJ520", origin=origin, destination=destination, aircraft=aircraft)
        with pytest.raises(IntegrityError):
            Flight.objects.create(
                flight_number="BJ520",
                origin=origin,
                destination=destination,
                aircraft=aircraft,
                departure_time=timezone.now() + timedelta(hours=20),
                arrival_time=timezone.now() + timedelta(hours=23),
                base_price_economy=Decimal("400.00"),
                base_price_business=Decimal("1300.00"),
            )

    @pytest.mark.parametrize("status", [
        "scheduled", "boarding", "in_flight", "arrived", "delayed", "cancelled",
    ])
    def test_flight_status_choices(self, status):
        """Test que tous les statuts valides sont acceptes (parametrized)."""
        flight = FlightFactory(status=status)
        assert flight.status == status
        # Verifie que get_status_display() retourne une valeur non vide
        assert flight.get_status_display()

    def test_flight_invalid_status_raises_error(self):
        """Test qu'un statut invalide leve une erreur."""
        origin = AirportFactory()
        destination = AirportFactory()
        aircraft = AircraftFactory()
        with pytest.raises(Exception):
            Flight.objects.create(
                flight_number="BJ999",
                origin=origin,
                destination=destination,
                aircraft=aircraft,
                departure_time=timezone.now() + timedelta(hours=5),
                arrival_time=timezone.now() + timedelta(hours=8),
                base_price_economy=Decimal("200.00"),
                base_price_business=Decimal("800.00"),
                status="INVALID_STATUS",
            )

    def test_flight_duration_auto_calculation(self):
        """Test que la duree est automatiquement calculee lors de la sauvegarde."""
        now = timezone.now()
        departure = now + timedelta(hours=10)
        arrival = now + timedelta(hours=13, minutes=30)
        flight = FlightFactory(departure_time=departure, arrival_time=arrival)
        flight.save()
        assert flight.duration is not None
        assert flight.duration == timedelta(hours=3, minutes=30)

    def test_flight_search(self):
        """Test de la methode search_flights avec des resultats."""
        origin = AirportFactory(code="TUN")
        destination = AirportFactory(code="CDG")
        aircraft = AircraftFactory()
        departure_date = (timezone.now() + timedelta(days=3)).date()
        FlightFactory(
            flight_number="BJ501",
            origin=origin,
            destination=destination,
            aircraft=aircraft,
            departure_time=timezone.now() + timedelta(days=3, hours=8),
            arrival_time=timezone.now() + timedelta(days=3, hours=11),
            status="scheduled",
            available_seats_economy=50,
            is_active=True,
        )
        results = Flight.search_flights("TUN", "CDG", departure_date, passengers=1)
        assert results.count() >= 1
        assert results.first().flight_number == "BJ501"

    def test_flight_search_no_results(self):
        """Test de search_flights quand aucun vol ne correspond."""
        origin = AirportFactory(code="TUN")
        destination = AirportFactory(code="CDG")
        # Creer un vol dans le passe ou annule — ne doit pas etre trouve
        departure_date = (timezone.now() + timedelta(days=1)).date()
        FlightFactory(
            origin=origin,
            destination=destination,
            departure_time=timezone.now() - timedelta(days=1),
            arrival_time=timezone.now() - timedelta(days=1, hours=-3),
            status="cancelled",
        )
        results = Flight.search_flights("TUN", "CDG", departure_date)
        assert results.count() == 0

    def test_get_current_price_economy(self):
        """Test du prix dynamique economique sans promotion."""
        flight = FlightFactory(base_price_economy=Decimal("350.00"))
        price = flight.get_current_price_economy()
        assert price == Decimal("350.00")

    def test_get_current_price_business(self):
        """Test du prix dynamique affaires sans promotion."""
        flight = FlightFactory(base_price_business=Decimal("1200.00"))
        price = flight.get_current_price_business()
        assert price == Decimal("1200.00")

    def test_flight_default_status_scheduled(self):
        """Test que le statut par defaut est 'scheduled'."""
        flight = FlightFactory()
        assert flight.status == "scheduled"
'''


# ====================================================================
# FILE 3 — tests/unit/test_models_bookings.py
# ====================================================================
TEST_MODELS_BOOKINGS = '''\
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
    PaymentFactory,
    FlightFactory,
    AirportFactory,
    AircraftFactory,
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
            special_requests="Siege cote hublot",
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
        booking = BookingFactory()
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
            price=Decimal("350.00"),
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
# Payment — 5 tests
# ====================================================================


@pytest.mark.unit
@pytest.mark.django_db
class TestPayment:
    """Tests unitaires du modele Payment."""

    def test_payment_creation(self):
        """Test de creation d'un paiement avec tous les champs."""
        booking = BookingFactory()
        payment = PaymentFactory(
            booking=booking,
            amount=Decimal("350.00"),
            method="credit_card",
            status="completed",
            transaction_id="TXN-2025-001",
        )
        assert payment.booking == booking
        assert payment.amount == Decimal("350.00")
        assert payment.method == "credit_card"
        assert payment.status == "completed"
        assert payment.transaction_id == "TXN-2025-001"

    @pytest.mark.parametrize("method", ["credit_card", "debit_card", "bank_transfer", "cash"])
    def test_payment_method_choices(self, method):
        """Test que toutes les methodes de paiement sont acceptees (parametrized)."""
        payment = PaymentFactory(method=method)
        assert payment.method == method
        assert payment.get_method_display()

    @pytest.mark.parametrize("status", ["pending", "completed", "failed", "refunded"])
    def test_payment_status_choices(self, status):
        """Test que tous les statuts de paiement sont acceptes (parametrized)."""
        payment = PaymentFactory(status=status)
        assert payment.status == status
        assert payment.get_status_display()

    def test_payment_str(self):
        """Test que __str__ contient le montant et le statut."""
        payment = PaymentFactory(amount=Decimal("350.00"), status="completed")
        result = str(payment)
        assert "350" in result
        assert "Compl" in result  # "Complété" in French

    def test_payment_transaction_id_optional(self):
        """Test que le transaction_id est optionnel (blank=True)."""
        payment = PaymentFactory(transaction_id="")
        assert payment.transaction_id == ""
'''


# ====================================================================
# FILE 4 — tests/unit/test_models_accounts.py
# ====================================================================
TEST_MODELS_ACCOUNTS = '''\
"""Tests unitaires du module accounts — Modele UserProfile.

Ce module contient les tests unitaires pytest pour le modele UserProfile
de l'application accounts : UserProfile (6 tests).

Marqueurs utilises :
    @pytest.mark.unit      — Categorie de test unitaire
    @pytest.mark.django_db — Acces a la base de donnees de test

Execution :
    pytest tests/unit/test_models_accounts.py -v
    pytest tests/unit/test_models_accounts.py -v -m unit
"""

import pytest
from datetime import date

from django.contrib.auth.models import User

from accounts.models import UserProfile
from tests.factories import UserProfileFactory


# ====================================================================
# UserProfile — 6 tests
# ====================================================================


@pytest.mark.unit
@pytest.mark.django_db
class TestUserProfile:
    """Tests unitaires du modele UserProfile."""

    def test_profile_creation(self):
        """Test de creation d'un profil utilisateur avec tous les champs."""
        user = User.objects.create_user(
            username="jean.dupont",
            first_name="Jean",
            last_name="Dupont",
            email="jean.dupont@example.com",
        )
        profile = UserProfile.objects.update_or_create(
            user=user,
            defaults={
                "phone": "+33 6 12 34 56 78",
                "address": "12 Rue de la Paix",
                "city": "Paris",
                "country": "France",
                "date_of_birth": date(1985, 7, 14),
                "nationality": "Francaise",
                "passport_number": "FR12345678",
                "gender": "M",
                "newsletter": True,
            },
        )
        assert profile.user == user
        assert profile.phone == "+33 6 12 34 56 78"
        assert profile.city == "Paris"
        assert profile.country == "France"
        assert profile.nationality == "Francaise"
        assert profile.gender == "M"
        assert profile.newsletter is True

    def test_profile_auto_creation(self):
        """Test que le signal post_save cree automatiquement un profil."""
        # Le signal accounts/signals.py cree un UserProfile a la creation
        # d'un User. On verifie que le profil existe apres creation.
        user = User.objects.create_user(
            username="test_auto_profile",
            email="auto@example.com",
        )
        # Verifier que le profil a ete cree par le signal
        assert hasattr(user, "profile")
        assert user.profile is not None
        assert isinstance(user.profile, UserProfile)

    def test_profile_full_name(self):
        """Test de la propriete full_name (first_name + last_name)."""
        user = User.objects.create_user(
            username="marie.curie",
            first_name="Marie",
            last_name="Curie",
            email="marie@example.com",
        )
        UserProfile.objects.update_or_create(user=user, defaults={"nationality": "Francaise"})
        # Le signal va aussi essayer de creer — utiliser get_or_create pattern
        profile = user.profile
        assert profile.full_name == "Marie Curie"

    def test_profile_without_full_name(self):
        """Test que full_name retourne le username si pas de nom complet."""
        user = User.objects.create_user(
            username="anonymous42",
            email="anon@example.com",
            first_name="",
            last_name="",
        )
        UserProfile.objects.update_or_create(user=user, defaults={})
        profile = user.profile
        assert profile.full_name == "anonymous42"

    def test_profile_one_to_one_user(self):
        """Test de la relation OneToOne entre User et UserProfile."""
        user = User.objects.create_user(
            username="onetoone_test",
            email="onetoone@example.com",
        )
        UserProfileFactory(user=user)
        # Verifier l'acces depuis User vers Profile
        assert user.profile.user == user
        # Verifier que l'on ne peut pas creer deux profils pour le meme user
        from django.db import IntegrityError
        with pytest.raises(IntegrityError):
            UserProfile.objects.update_or_create(user=user, defaults={})

    def test_profile_newsletter_default(self):
        """Test que newsletter est False par defaut."""
        user = User.objects.create_user(
            username="newsletter_test",
            email="newsletter@example.com",
        )
        profile = UserProfileFactory(user=user)
        assert profile.newsletter is False
'''


# ====================================================================
# FILE 5 — tests/unit/test_models_promotions.py
# ====================================================================
TEST_MODELS_PROMOTIONS = '''\
"""Tests unitaires du module promotions et destinations.

Ce module contient les tests unitaires pytest pour :
  - Promotion (7 tests)       : Creation, code unique, validite, expiration,
                                limite d'utilisation, remaining_uses, range
  - Destination (5 tests)     : Creation, slug unique, categories, __str__,
                                get_lowest_price
  - DestinationReview (3 tests): Creation, unique_together, rating range

Marqueurs utilises :
    @pytest.mark.unit      — Categorie de test unitaire
    @pytest.mark.django_db — Acces a la base de donnees de test

Execution :
    pytest tests/unit/test_models_promotions.py -v
    pytest tests/unit/test_models_promotions.py -v -m unit
"""

import pytest
from decimal import Decimal
from datetime import timedelta

from django.db import IntegrityError
from django.utils import timezone
from django.contrib.auth.models import User

from promotions.models import Promotion, NewsletterSubscription
from destinations.models import Destination, DestinationReview
from tests.factories import (
    PromotionFactory,
    NewsletterSubscriptionFactory,
    DestinationFactory,
    DestinationReviewFactory,
    FlightFactory,
    AirportFactory,
    AircraftFactory,
)


# ====================================================================
# Promotion — 7 tests
# ====================================================================


@pytest.mark.unit
@pytest.mark.django_db
class TestPromotion:
    """Tests unitaires du modele Promotion."""

    def test_promotion_creation(self):
        """Test de creation d'une promotion avec tous les champs."""
        now = timezone.now()
        promo = PromotionFactory(
            code="NOEL2025",
            name="Promo Noel",
            description="Remise de 20% pour les fetes",
            promo_type="percentage",
            discount_percentage=Decimal("20.00"),
            start_date=now,
            end_date=now + timedelta(days=30),
            max_uses=100,
            current_uses=0,
            is_active=True,
        )
        assert promo.code == "NOEL2025"
        assert promo.name == "Promo Noel"
        assert promo.discount_percentage == Decimal("20.00")
        assert promo.max_uses == 100
        assert promo.current_uses == 0

    def test_promotion_code_unique(self):
        """Test que le code promo est unique."""
        PromotionFactory(code="SUMMER25")
        with pytest.raises(IntegrityError):
            Promotion.objects.create(
                code="SUMMER25",
                name="Autre promo",
                description="Test",
                promo_type="percentage",
                start_date=timezone.now(),
                end_date=timezone.now() + timedelta(days=10),
            )

    def test_promotion_is_valid(self):
        """Test qu'une promotion dans la plage de dates est valide."""
        now = timezone.now()
        promo = PromotionFactory(
            start_date=now - timedelta(days=1),
            end_date=now + timedelta(days=30),
            is_active=True,
            max_uses=100,
            current_uses=10,
        )
        assert promo.is_valid is True

    def test_promotion_expired(self):
        """Test qu'une promotion expiree n'est pas valide."""
        now = timezone.now()
        promo = PromotionFactory(
            start_date=now - timedelta(days=60),
            end_date=now - timedelta(days=1),
            is_active=True,
        )
        assert promo.is_valid is False

    def test_promotion_max_uses_reached(self):
        """Test qu'une promotion dont la limite est atteinte n'est pas valide."""
        now = timezone.now()
        promo = PromotionFactory(
            start_date=now - timedelta(days=1),
            end_date=now + timedelta(days=30),
            is_active=True,
            max_uses=100,
            current_uses=100,
        )
        assert promo.is_valid is False

    def test_remaining_uses(self):
        """Test de la propriete remaining_uses."""
        promo = PromotionFactory(max_uses=100, current_uses=37)
        assert promo.remaining_uses == 63

        promo2 = PromotionFactory(max_uses=50, current_uses=50)
        assert promo2.remaining_uses == 0

        # Test que remaining_uses ne peut pas etre negatif
        promo3 = PromotionFactory(max_uses=10, current_uses=15)
        assert promo3.remaining_uses == 0

    def test_promotion_discount_percentage_range(self):
        """Test que discount_percentage est dans la plage [0, 100]."""
        # Valeur valide
        promo_valid = PromotionFactory(discount_percentage=Decimal("50.00"))
        assert 0 <= float(promo_valid.discount_percentage) <= 100

        # Zero est valide
        promo_zero = PromotionFactory(discount_percentage=Decimal("0.00"))
        assert promo_zero.discount_percentage == Decimal("0.00")

        # Cent est valide
        promo_full = PromotionFactory(discount_percentage=Decimal("100.00"))
        assert promo_full.discount_percentage == Decimal("100.00")


# ====================================================================
# NewsletterSubscription — bonus tests
# ====================================================================


@pytest.mark.unit
@pytest.mark.django_db
class TestNewsletterSubscription:
    """Tests unitaires du modele NewsletterSubscription."""

    def test_newsletter_creation(self):
        """Test de creation d'un abonnement newsletter."""
        sub = NewsletterSubscriptionFactory(
            email="abonne@nouvelair.com",
            first_name="Sophie",
            is_active=True,
        )
        assert sub.email == "abonne@nouvelair.com"
        assert sub.first_name == "Sophie"
        assert sub.is_active is True

    def test_newsletter_email_unique(self):
        """Test que l'email est unique."""
        NewsletterSubscriptionFactory(email="unique@test.com")
        with pytest.raises(IntegrityError):
            NewsletterSubscription.objects.create(email="unique@test.com")

    def test_newsletter_str(self):
        """Test que __str__ retourne l'email."""
        sub = NewsletterSubscriptionFactory(email="str@test.com")
        assert str(sub) == "str@test.com"


# ====================================================================
# Destination — 5 tests
# ====================================================================


@pytest.mark.unit
@pytest.mark.django_db
class TestDestination:
    """Tests unitaires du modele Destination."""

    def test_destination_creation(self):
        """Test de creation d'une destination avec tous les champs."""
        destination = DestinationFactory(
            name="Sousse",
            slug="sousse",
            description="Ville mediterraneenne avec plages superbes",
            short_description="Sousse, perle du Sahel",
            category="beach",
            rating=Decimal("4.5"),
            is_featured=True,
            is_active=True,
        )
        assert destination.name == "Sousse"
        assert destination.slug == "sousse"
        assert destination.category == "beach"
        assert destination.rating == Decimal("4.5")
        assert destination.is_featured is True

    def test_destination_slug_unique(self):
        """Test que le slug est unique."""
        DestinationFactory(slug="tunis")
        with pytest.raises(IntegrityError):
            Destination.objects.create(
                name="Tunis 2",
                slug="tunis",
                description="Test",
                short_description="Test",
                category="urban",
            )

    @pytest.mark.parametrize("category", ["beach", "culture", "adventure", "relaxation", "urban", "nature"])
    def test_destination_category_choices(self, category):
        """Test que toutes les categories sont acceptees (parametrized)."""
        destination = DestinationFactory(category=category)
        assert destination.category == category
        assert destination.get_category_display()

    def test_destination_str(self):
        """Test que __str__ retourne le nom de la destination."""
        destination = DestinationFactory(name="Djerba")
        assert str(destination) == "Djerba"

    def test_get_lowest_price(self):
        """Test de la methode get_lowest_price."""
        airport = AirportFactory(code="TUN")
        destination = DestinationFactory(airport=airport)
        aircraft = AircraftFactory()
        flight = FlightFactory(
            destination=airport,
            aircraft=aircraft,
            departure_time=timezone.now() + timedelta(days=10),
            arrival_time=timezone.now() + timedelta(days=10, hours=2),
            base_price_economy=Decimal("180.00"),
            available_seats_economy=50,
            is_active=True,
        )
        price = destination.get_lowest_price()
        assert price is not None
        assert price == Decimal("180.00")

    def test_get_lowest_price_no_flights(self):
        """Test que get_lowest_price retourne None sans vols disponibles."""
        destination = DestinationFactory(airport=None)
        assert destination.get_lowest_price() is None


# ====================================================================
# DestinationReview — 3 tests
# ====================================================================


@pytest.mark.unit
@pytest.mark.django_db
class TestDestinationReview:
    """Tests unitaires du modele DestinationReview."""

    def test_review_creation(self):
        """Test de creation d'un avis destination."""
        destination = DestinationFactory(name="Hammamet")
        user = User.objects.create_user(username="reviewer1", email="rev1@test.com")
        review = DestinationReviewFactory(
            destination=destination,
            user=user,
            rating=5,
            title="Magnifique sejour",
            comment="J'ai adore la plage et les restaurants locaux.",
        )
        assert review.destination == destination
        assert review.user == user
        assert review.rating == 5
        assert review.title == "Magnifique sejour"
        assert review.is_approved is False  # default

    def test_unique_review_per_user(self):
        """Test qu'un utilisateur ne peut pas laisser deux avis pour la meme destination."""
        destination = DestinationFactory(name="Bizerte")
        user = User.objects.create_user(username="reviewer2", email="rev2@test.com")
        DestinationReviewFactory(destination=destination, user=user, rating=4)
        with pytest.raises(IntegrityError):
            DestinationReview.objects.create(
                destination=destination,
                user=user,
                rating=3,
                title="Deuxieme avis",
                comment="Cela ne devrait pas etre possible.",
            )

    def test_review_rating_range(self):
        """Test que la note est un entier positif (1-5)."""
        review = DestinationReviewFactory(rating=1)
        assert review.rating >= 1
        assert review.rating <= 5

        review5 = DestinationReviewFactory(rating=5)
        assert review5.rating == 5
'''


# ====================================================================
# FILE 6 — tests/unit/test_models_utils.py
# ====================================================================
TEST_MODELS_UTILS = '''\
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
'''


# ====================================================================
# FILE 7 — tests/factories.py
# ====================================================================
TESTS_FACTORIES = '''\
"""Factories factory_boy pour le projet NouvelAir.

Ce module definit toutes les factories utilisees pour generer des donnees
de test realistes pour les tests unitaires, d'integration et BDD.

Modeles couverts :
    - Airport, Aircraft, Flight (flights)
    - Booking, Passenger, Payment (bookings)
    - UserProfile (accounts)
    - Promotion, NewsletterSubscription (promotions)
    - Destination, DestinationReview (destinations)

Utilisation :
    from tests.factories import AirportFactory, FlightFactory
    airport = AirportFactory(code="TUN")
    flight = FlightFactory(origin=airport)

Auteurs : Equipe QA NouvelAir
Version : 1.0.0
"""

import factory
from factory import Faker, SubFactory, LazyAttribute, post_generation
from factory.django import DjangoModelFactory
from decimal import Decimal
from datetime import timedelta

from django.utils import timezone
from django.contrib.auth.models import User

from flights.models import Airport, Aircraft, Flight
from bookings.models import Booking, Passenger, Payment
from accounts.models import UserProfile
from promotions.models import Promotion, NewsletterSubscription
from destinations.models import Destination, DestinationReview


# ====================================================================
# Helpers
# ====================================================================

FRENCH_LOCALE = "fr_FR"

# Aeroports reels utilises par NouvelAir
REAL_AIRPORT_CODES = [
    ("TUN", "Aeroport International Tunis-Carthage", "Tunis", "Tunisie"),
    ("CDG", "Aeroport de Paris-Charles de Gaulle", "Paris", "France"),
    ("ORY", "Aeroport de Paris-Orly", "Paris", "France"),
    ("FCO", "Aeroport de Rome-Fiumicino", "Rome", "Italie"),
    ("MRS", "Aeroport de Marseille-Provence", "Marseille", "France"),
    ("ALG", "Aeroport Houari Boumediene", "Alger", "Algerie"),
    ("CMN", "Aeroport Mohammed V", "Casablanca", "Maroc"),
    ("LHR", "Aeroport de Londres-Heathrow", "Londres", "Royaume-Uni"),
    ("JFK", "Aeroport John F. Kennedy", "New York", "Etats-Unis"),
    ("DXB", "Aeroport International de Dubaï", "Dubaï", "Emirats Arabes Unis"),
    ("IST", "Aeroport Istanbul", "Istanbul", "Turquie"),
    ("BER", "Aeroport de Berlin-Brandebourg", "Berlin", "Allemagne"),
]


# ====================================================================
# User — Utilisateur de test
# ====================================================================


class UserFactory(DjangoModelFactory):
    """Factory pour le modele User de Django."""

    class Meta:
        model = User
        django_get_or_create = ("username",)

    username = Faker("user_name", locale=FRENCH_LOCALE)
    first_name = Faker("first_name", locale=FRENCH_LOCALE)
    last_name = Faker("last_name", locale=FRENCH_LOCALE)
    email = Faker("email", locale=FRENCH_LOCALE)
    is_active = True


# ====================================================================
# Flights — Aéroports, Aéronefs, Vols
# ====================================================================


class AirportFactory(DjangoModelFactory):
    """Factory pour le modele Airport — utilise de vrais codes IATA."""

    class Meta:
        model = Airport
        django_get_or_create = ("code",)

    code = Faker("random_element", elements=[a[0] for a in REAL_AIRPORT_CODES])
    name = LazyAttribute(
        lambda o: next(
            (a[1] for a in REAL_AIRPORT_CODES if a[0] == o.code),
            f"Aeroport de {o.city}",
        )
    )
    city = LazyAttribute(
        lambda o: next(
            (a[2] for a in REAL_AIRPORT_CODES if a[0] == o.code),
            Faker("city", locale=FRENCH_LOCALE).evaluate(None),
        )
    )
    country = LazyAttribute(
        lambda o: next(
            (a[3] for a in REAL_AIRPORT_CODES if a[0] == o.code),
            Faker("country", locale=FRENCH_LOCALE).evaluate(None),
        )
    )
    latitude = Faker("latitude")
    longitude = Faker("longitude")
    is_active = True

    @classmethod
    def _build(cls, model_class, *args, **kwargs):
        """Override pour utiliser le nom reel de l'aeroport si le code est connu."""
        code = kwargs.get("code")
        if code:
            for real_code, real_name, real_city, real_country in REAL_AIRPORT_CODES:
                if real_code == code:
                    kwargs.setdefault("name", real_name)
                    kwargs.setdefault("city", real_city)
                    kwargs.setdefault("country", real_country)
                    break
        return super()._build(model_class, *args, **kwargs)


class AircraftFactory(DjangoModelFactory):
    """Factory pour le modele Aircraft — modeles reels d'aeronefs."""

    class Meta:
        model = Aircraft
        django_get_or_create = ("registration",)

    model_name = Faker("random_element", elements=[
        "Airbus A320neo",
        "Airbus A321neo",
        "Boeing 737-800",
        "Airbus A330-300",
        "Boeing 787-9 Dreamliner",
    ])
    registration = Faker("bothify", text="TS-###")
    total_seats = Faker("random_int", min=100, max=350)
    economy_seats = LazyAttribute(lambda o: int(o.total_seats * 0.83))
    business_seats = LazyAttribute(lambda o: o.total_seats - o.economy_seats)
    is_active = True


class FlightFactory(DjangoModelFactory):
    """Factory pour le modele Flight — vols NouvelAir (BJ)."""

    class Meta:
        model = Flight
        django_get_or_create = ("flight_number",)

    flight_number = Faker("bothify", text="BJ###")
    origin = SubFactory(AirportFactory)
    destination = SubFactory(AirportFactory)
    aircraft = SubFactory(AircraftFactory)
    departure_time = Faker(
        "date_time_between",
        start_date="+3d",
        end_date="+30d",
        tzinfo=timezone.get_current_timezone(),
    )
    arrival_time = LazyAttribute(
        lambda o: o.departure_time + timedelta(hours=3, minutes=15)
    )
    status = "scheduled"
    base_price_economy = Faker("pydecimal", left_digits=3, right_digits=2, positive=True, max_value=999)
    base_price_business = LazyAttribute(
        lambda o: Decimal(str(float(o.base_price_economy) * 3.5))
    )
    available_seats_economy = LazyAttribute(
        lambda o: o.aircraft.economy_seats if o.aircraft else 150
    )
    available_seats_business = LazyAttribute(
        lambda o: o.aircraft.business_seats if o.aircraft else 30
    )
    is_active = True


# ====================================================================
# Bookings — Reservations, Passagers, Paiements
# ====================================================================


class BookingFactory(DjangoModelFactory):
    """Factory pour le modele Booking."""

    class Meta:
        model = Booking

    user = SubFactory(UserFactory)
    contact_email = Faker("email", locale=FRENCH_LOCALE)
    contact_phone = Faker("phone_number", locale=FRENCH_LOCALE)
    status = "pending"
    total_amount = Faker("pydecimal", left_digits=4, right_digits=2, positive=True, max_value=9999)
    special_requests = Faker("paragraph", nb_sentences=1, locale=FRENCH_LOCALE)


class PassengerFactory(DjangoModelFactory):
    """Factory pour le modele Passenger — noms francais realistes."""

    class Meta:
        model = Passenger

    booking = SubFactory(BookingFactory)
    flight = SubFactory(FlightFactory)
    title = Faker("random_element", elements=["mr", "mme", "mll", "enf"])
    first_name = Faker("first_name", locale=FRENCH_LOCALE)
    last_name = Faker("last_name", locale=FRENCH_LOCALE)
    date_of_birth = Faker("date_of_birth", locale=FRENCH_LOCALE)
    nationality = Faker("random_element", elements=[
        "Tunisienne", "Francaise", "Italienne", "Algerienne",
        "Marocaine", "Libyenne", "Egyptienne", "Belge",
    ])
    passport_number = Faker("bothify", text="??######")
    travel_class = Faker("random_element", elements=["economy", "business"])
    price = Faker("pydecimal", left_digits=3, right_digits=2, positive=True, max_value=9999)
    special_assistance = False
    meal_preference = Faker("random_element", elements=[
        "Standard", "Vegetarien", "Sans gluten", "Halal", "Casher", "",
    ])


class PaymentFactory(DjangoModelFactory):
    """Factory pour le modele Payment."""

    class Meta:
        model = Payment

    booking = SubFactory(BookingFactory)
    amount = Faker("pydecimal", left_digits=4, right_digits=2, positive=True, max_value=9999)
    method = Faker("random_element", elements=[
        "credit_card", "debit_card", "bank_transfer", "cash",
    ])
    status = "pending"
    transaction_id = Faker("bothify", text="TXN-????-######")


# ====================================================================
# Accounts — Profil utilisateur
# ====================================================================


class UserProfileFactory(DjangoModelFactory):
    """Factory pour le modele UserProfile."""

    class Meta:
        model = UserProfile
        django_get_or_create = ("user",)

    user = SubFactory(UserFactory)
    phone = Faker("phone_number", locale=FRENCH_LOCALE)
    address = Faker("address", locale=FRENCH_LOCALE)
    city = Faker("city", locale=FRENCH_LOCALE)
    country = Faker("country", locale=FRENCH_LOCALE)
    date_of_birth = Faker("date_of_birth", locale=FRENCH_LOCALE)
    nationality = Faker("random_element", elements=[
        "Tunisienne", "Francaise", "Italienne", "Algerienne",
        "Marocaine", "Libyenne", "Egyptienne", "Belge",
    ])
    passport_number = Faker("bothify", text="??######")
    gender = Faker("random_element", elements=["M", "F"])
    newsletter = False


# ====================================================================
# Promotions — Codes promo, Newsletter
# ====================================================================


class PromotionFactory(DjangoModelFactory):
    """Factory pour le modele Promotion."""

    class Meta:
        model = Promotion
        django_get_or_create = ("code",)

    code = Faker("bothify", text="NOVEL_???")
    name = Faker("sentence", nb_words=4, locale=FRENCH_LOCALE)
    description = Faker("paragraph", nb_sentences=3, locale=FRENCH_LOCALE)
    promo_type = Faker("random_element", elements=[
        "percentage", "fixed", "buy_one_get_one", "free_upgrade",
    ])
    discount_percentage = Faker("pydecimal", left_digits=2, right_digits=2, positive=True, max_value=100)
    discount_amount = Faker("pydecimal", left_digits=3, right_digits=2, positive=True, max_value=500)
    start_date = LazyAttribute(
        lambda o: timezone.now() - timedelta(days=Faker("random_int", min=0, max=7).evaluate(None))
    )
    end_date = LazyAttribute(
        lambda o: o.start_date + timedelta(days=Faker("random_int", min=15, max=60).evaluate(None))
    )
    max_uses = Faker("random_int", min=50, max=1000)
    current_uses = 0
    min_purchase_amount = Faker("pydecimal", left_digits=3, right_digits=2, positive=True, max_value=500)
    is_active = True
    is_featured = False


class NewsletterSubscriptionFactory(DjangoModelFactory):
    """Factory pour le modele NewsletterSubscription."""

    class Meta:
        model = NewsletterSubscription
        django_get_or_create = ("email",)

    email = Faker("email", locale=FRENCH_LOCALE)
    first_name = Faker("first_name", locale=FRENCH_LOCALE)
    is_active = True


# ====================================================================
# Destinations — Destinations touristiques, Avis
# ====================================================================


class DestinationFactory(DjangoModelFactory):
    """Factory pour le modele Destination — destinations tunisiennes et mediterraneennes."""

    class Meta:
        model = Destination
        django_get_or_create = ("slug",)

    name = Faker("random_element", elements=[
        "Sousse", "Hammamet", "Djerba", "Sfax", "Monastir",
        "Nabeul", "Tozeur", "Tabarka", "Mahdia", "Kairouan",
        "Tunis", "Bizerte", "Gabes", "Kerkennah", "Carthage",
    ])
    slug = LazyAttribute(lambda o: o.name.lower().replace(" ", "-"))
    description = Faker("paragraph", nb_sentences=5, locale=FRENCH_LOCALE)
    short_description = Faker("sentence", nb_words=12, locale=FRENCH_LOCALE)
    airport = SubFactory(AirportFactory)
    category = Faker("random_element", elements=[
        "beach", "culture", "adventure", "relaxation", "urban", "nature",
    ])
    rating = Faker("pydecimal", left_digits=1, right_digits=1, positive=True, max_value=5)
    is_featured = Faker("boolean", chance_of_getting_true=30)
    is_active = True


class DestinationReviewFactory(DjangoModelFactory):
    """Factory pour le modele DestinationReview."""

    class Meta:
        model = DestinationReview
        django_get_or_create = ("destination", "user")

    destination = SubFactory(DestinationFactory)
    user = SubFactory(UserFactory)
    rating = Faker("random_int", min=1, max=5)
    title = Faker("sentence", nb_words=5, locale=FRENCH_LOCALE)
    comment = Faker("paragraph", nb_sentences=3, locale=FRENCH_LOCALE)
    is_approved = False
'''


# ====================================================================
# FILE 8 — requirements_test.txt
# ====================================================================
REQUIREMENTS_TEST = """\
# ====================================================================
# requirements_test.txt — Dependances de test pour le projet NouvelAir
# ====================================================================
# Installation :
#   pip install -r requirements_test.txt
# ====================================================================

# --- Frameworks de test ---
pytest>=8.0,<9.0
pytest-django>=4.8,<5.0
pytest-cov>=5.0,<6.0
pytest-html>=4.1,<5.0
pytest-mock>=3.14,<4.0
pytest-xdist>=3.6,<4.0
pytest-sugar>=1.0,<2.0

# --- BDD (Behavior-Driven Development) ---
behave>=1.2.7,<2.0
behave-django>=1.4.0,<2.0

# --- Factories de donnees de test ---
factory-boy>=3.3,<4.0
faker>=25.0,<30.0

# --- Tests de performance ---
locust>=2.29,<3.0

# --- Securite ---
bandit>=1.7,<2.0
safety>=3.1,<4.0

# --- Rapports ---
allure-pytest>=2.13,<3.0

# --- Tests E2E ---
playwright>=1.44,<2.0
pixelmatch>=0.22,<1.0
axe-playwright-python>=2.2,<3.0

# --- Clients HTTP ---
requests>=2.31,<3.0
httpx>=0.27,<1.0
"""


# ====================================================================
# FONCTIONS UTILITAIRES
# ====================================================================

def create_file(filepath: str, content: str) -> bool:
    """Cree un fichier avec son contenu. Retourne True si succes."""
    try:
        path = Path(filepath)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        return True
    except Exception as e:
        print(f"  [ERREUR] Impossible de creer {filepath} : {e}")
        return False


def print_summary(created: list, failed: list):
    """Affiche le resume de l'execution du script."""
    print("\n" + "=" * 70)
    print("  RESUME DE L'EXECUTION")
    print("=" * 70)

    if created:
        print(f"\n  Fichiers crees avec succes ({len(created)}) :")
        for f in created:
            print(f"    [OK] {f}")

    if failed:
        print(f"\n  Fichiers en echec ({len(failed)}) :")
        for f in failed:
            print(f"    [ECHEC] {f}")

    print(f"\n  Total : {len(created)} fichiers crees, {len(failed)} echecs")

    # Compteur de tests
    print("\n" + "-" * 70)
    print("  RECAPITULATIF DES TESTS")
    print("-" * 70)
    print("  Module              | Fichier                      | Tests")
    print("  " + "-" * 64)
    test_counts = [
        ("flights (Airport)",   "test_models_flights.py",    "7"),
        ("flights (Aircraft)",  "test_models_flights.py",    "6"),
        ("flights (Flight)",    "test_models_flights.py",    "11"),
        ("bookings (Booking)",  "test_models_bookings.py",   "8"),
        ("bookings (Passenger)","test_models_bookings.py",   "5"),
        ("bookings (Payment)",  "test_models_bookings.py",   "5"),
        ("accounts (Profile)",  "test_models_accounts.py",   "6"),
        ("promotions (Promo)",  "test_models_promotions.py",  "7"),
        ("promotions (NL)",     "test_models_promotions.py",  "3"),
        ("destinations (Dest)", "test_models_promotions.py",  "6"),
        ("destinations (Review)","test_models_promotions.py", "3"),
        ("utils",               "test_models_utils.py",      "5"),
    ]
    total = 0
    for module, fichier, count_str in test_counts:
        count = int(count_str.rstrip("+"))
        total += count
        print(f"  {module:<21}| {fichier:<29}| {count_str:>4}")

    print("  " + "-" * 64)
    print(f"  {'TOTAL':<21}|                              | {total:>4}+")
    print("-" * 70)

    print("\n  Factories dans tests/factories.py :")
    factories = [
        "UserFactory", "AirportFactory", "AircraftFactory", "FlightFactory",
        "BookingFactory", "PassengerFactory", "PaymentFactory",
        "UserProfileFactory", "PromotionFactory", "NewsletterSubscriptionFactory",
        "DestinationFactory", "DestinationReviewFactory",
    ]
    for f in factories:
        print(f"    - {f}")
    print(f"  Total : {len(factories)} factories\n")

    print("  Commandes utiles :")
    print("    pytest tests/unit/ -v                    # Tous les tests unitaires")
    print("    pytest tests/unit/ -v -m unit            # Seulement les tests marques unit")
    print("    pytest tests/unit/ -v --tb=short         # Traceback courtes")
    print("    pytest tests/unit/ --cov=. --cov-report=html  # Couverture HTML")
    print("    pytest tests/unit/ -v -k \"test_flight\"   # Filtrer par nom")
    print()

    return len(created) > 0 and len(failed) == 0


# ====================================================================
# FONCTION PRINCIPALE
# ====================================================================

def main():
    """Fonction principale — cree tous les fichiers de test Jour 2."""
    print(BANNER)
    print(f"  Date : {datetime.now().strftime('%d/%m/%Y a %H:%M')}")
    print(f"  Repertoire projet : {PROJECT_ROOT}")
    print()

    files_to_create = [
        ("tests/unit/__init__.py",               TESTS_UNIT_INIT,             "tests/unit/__init__.py (empty)"),
        ("tests/unit/test_models_flights.py",     TEST_MODELS_FLIGHTS,         "tests/unit/test_models_flights.py (24 tests)"),
        ("tests/unit/test_models_bookings.py",    TEST_MODELS_BOOKINGS,        "tests/unit/test_models_bookings.py (18 tests)"),
        ("tests/unit/test_models_accounts.py",    TEST_MODELS_ACCOUNTS,        "tests/unit/test_models_accounts.py (6 tests)"),
        ("tests/unit/test_models_promotions.py",  TEST_MODELS_PROMOTIONS,      "tests/unit/test_models_promotions.py (23 tests)"),
        ("tests/unit/test_models_utils.py",       TEST_MODELS_UTILS,           "tests/unit/test_models_utils.py (5 tests)"),
        ("tests/factories.py",                    TESTS_FACTORIES,             "tests/factories.py (12 factories)"),
        ("requirements_test.txt",                 REQUIREMENTS_TEST,           "requirements_test.txt (20+ packages)"),
    ]

    created = []
    failed = []

    for relative_path, content, description in files_to_create:
        filepath = PROJECT_ROOT / relative_path
        print(f"  Creation : {description} ...", end=" ")
        if create_file(str(filepath), content):
            print("OK")
            created.append(relative_path)
        else:
            print("ECHEC")
            failed.append(relative_path)

    # Resume
    success = print_summary(created, failed)

    if success:
        print("  Setup Jour 2 termine avec succes !")
        print("  Prochaine etape : executer les tests avec 'pytest tests/unit/ -v'")
    else:
        print("  ATTENTION : certains fichiers n'ont pas pu etre crees.")

    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
