"""
tests/test_regression.py - Suite de tests de régression pour NouvelAir
====================================================================
Suite complète de tests de régression couvrant tous les modules critiques
de l'application NouvelAir. Ces tests s'assurent que les fonctionnalités
existantes ne sont pas impactées par les nouvelles modifications.

Modules couverts:
    - flights: création de vols, aéroports, aéronefs, recherche
    - bookings: création de réservations, passagers, paiements, statuts
    - accounts: inscription, connexion, profil utilisateur
    - destinations: création de destinations, avis
    - promotions: création de promotions, newsletter
    - URLs: résolution de toutes les routes
    - Forms: validation des formulaires critiques

Marqueur: pytest.mark.regression

Auteurs: Équipe QA NouvelAir
Version: 1.0.0 - Jour 9
"""

import pytest
from decimal import Decimal
from datetime import date, timedelta
from django.utils import timezone
from django.test import Client, TestCase
from django.urls import reverse, resolve, NoReverseMatch
from django.contrib.auth.models import User

from flights.models import Airport, Aircraft, Flight
from bookings.models import Booking, Passenger, Payment
from accounts.models import UserProfile, SavedDestination
from promotions.models import Promotion, NewsletterSubscription
from destinations.models import Destination, DestinationReview


# =============================================================================
# Fixtures communes
# =============================================================================


@pytest.fixture
def airports():
    """Crée les aéroports principaux utilisés dans les tests."""
    tun = Airport.objects.create(
        code="TUN", name="Aéroport International Tunis-Carthage",
        city="Tunis", country="Tunisie",
        latitude=Decimal("36.851000"), longitude=Decimal("10.227000")
    )
    cdg = Airport.objects.create(
        code="CDG", name="Aéroport de Paris-Charles de Gaulle",
        city="Paris", country="France",
        latitude=Decimal("49.009691"), longitude=Decimal("2.547926")
    )
    fco = Airport.objects.create(
        code="FCO", name="Aéroport de Rome-Fiumicino",
        city="Rome", country="Italie",
        latitude=Decimal("41.800278"), longitude=Decimal("12.238889")
    )
    return {"tun": tun, "cdg": cdg, "fco": fco}


@pytest.fixture
def aircraft():
    """Crée un aéronef de test."""
    return Aircraft.objects.create(
        model_name="Airbus A320neo",
        registration="TS-INA",
        total_seats=180,
        economy_seats=150,
        business_seats=30,
        is_active=True,
    )


@pytest.fixture
def flight(airports, aircraft):
    """Crée un vol de test programmé dans le futur."""
    departure = timezone.now() + timedelta(days=7)
    arrival = departure + timedelta(hours=2, minutes=30)
    return Flight.objects.create(
        flight_number="BJ201",
        origin=airports["tun"],
        destination=airports["cdg"],
        aircraft=aircraft,
        departure_time=departure,
        arrival_time=arrival,
        base_price_economy=Decimal("189.50"),
        base_price_business=Decimal("663.25"),
        available_seats_economy=150,
        available_seats_business=30,
        status="scheduled",
        is_active=True,
    )


@pytest.fixture
def user():
    """Crée un utilisateur de test."""
    return User.objects.create_user(
        username="regression_user",
        first_name="Ahmed",
        last_name="Ben Ali",
        email="ahmed.regression@test.tn",
        password="TestPass123!",
    )


@pytest.fixture
def user_with_profile(user):
    """Crée un utilisateur avec un profil complet."""
    profile, _ = UserProfile.objects.get_or_create(
        user=user,
        defaults={
            "phone": "+216 22 333 444",
            "address": "12 Rue Habib Bourguiba",
            "city": "Tunis",
            "country": "Tunisie",
            "date_of_birth": date(1990, 5, 15),
            "nationality": "Tunisienne",
            "gender": "M",
            "newsletter": True,
        }
    )
    return user


@pytest.fixture
def booking(user, flight):
    """Crée une réservation de test."""
    return Booking.objects.create(
        user=user,
        contact_email=user.email,
        contact_phone="+216 22 333 444",
        status="pending",
        total_amount=Decimal("189.50"),
        special_requests="Siège côté hublot",
    )


@pytest.fixture
def client():
    """Client de test HTTP."""
    return Client()


# =============================================================================
# Régression: Modèles - Créations
# =============================================================================


@pytest.mark.regression
@pytest.mark.django_db
class TestModelCreationRegression:
    """Tests de régression pour la création de tous les modèles."""

    def test_regression_create_airport(self, airports):
        """REG-AIRPORT-001: Vérifie la création d'un aéroport avec tous ses champs."""
        ams = Airport.objects.create(
            code="AMS",
            name="Aéroport de Schiphol",
            city="Amsterdam",
            country="Pays-Bas",
            latitude=Decimal("52.310500"),
            longitude=Decimal("4.768300"),
            is_active=True,
        )
        assert ams.code == "AMS"
        assert ams.city == "Amsterdam"
        assert ams.is_active is True
        assert str(ams) == "AMS - Amsterdam (Pays-Bas)"
        assert ams.created_at is not None

    def test_regression_create_aircraft(self, aircraft):
        """REG-AIRCRAFT-001: Vérifie la création d'un aéronef."""
        assert aircraft.model_name == "Airbus A320neo"
        assert aircraft.registration == "TS-INA"
        assert aircraft.total_seats == 180
        assert aircraft.economy_seats == 150
        assert aircraft.business_seats == 30
        assert str(aircraft) == "Airbus A320neo (TS-INA)"

    def test_regression_create_flight(self, flight, airports, aircraft):
        """REG-FLIGHT-001: Vérifie la création d'un vol avec tous ses champs."""
        assert flight.flight_number == "BJ201"
        assert flight.origin == airports["tun"]
        assert flight.destination == airports["cdg"]
        assert flight.aircraft == aircraft
        assert flight.status == "scheduled"
        assert flight.base_price_economy == Decimal("189.50")
        assert flight.base_price_business == Decimal("663.25")
        assert flight.duration is not None
        assert "BJ201: TUN → CDG" in str(flight)

    def test_regression_create_booking(self, booking, user):
        """REG-BOOKING-001: Vérifie la création d'une réservation."""
        assert booking.user == user
        assert booking.status == "pending"
        assert booking.total_amount == Decimal("189.50")
        assert booking.contact_email == user.email
        assert booking.reference is not None
        assert len(booking.short_reference) == 8

    def test_regression_create_passenger(self, booking, flight):
        """REG-PASSENGER-001: Vérifie la création d'un passager."""
        passenger = Passenger.objects.create(
            booking=booking,
            flight=flight,
            title="mr",
            first_name="Mohamed",
            last_name="Trabelsi",
            date_of_birth=date(1985, 3, 20),
            nationality="Tunisienne",
            passport_number="TR1234567",
            travel_class="economy",
            price=Decimal("189.50"),
            special_assistance=False,
            meal_preference="Standard",
        )
        assert passenger.booking == booking
        assert passenger.flight == flight
        assert str(passenger) == "Monsieur Mohamed Trabelsi"

    def test_regression_create_payment(self, booking):
        """REG-PAYMENT-001: Vérifie la création d'un paiement."""
        payment = Payment.objects.create(
            booking=booking,
            amount=Decimal("189.50"),
            method="credit_card",
            status="completed",
            transaction_id="TXN-TEST-123456",
        )
        assert payment.booking == booking
        assert payment.amount == Decimal("189.50")
        assert payment.method == "credit_card"
        assert payment.status == "completed"
        assert str(payment) == "Paiement 189.50 TND - Complété"

    def test_regression_create_user_profile(self, user):
        """REG-PROFILE-001: Vérifie la création d'un profil utilisateur."""
        profile, _ = UserProfile.objects.update_or_create(
            user=user,
            defaults={
                "phone": "+216 22 333 444",
                "city": "Tunis",
                "country": "Tunisie",
                "nationality": "Tunisienne",
                "gender": "M",
            }
        )
        assert profile.user == user
        assert profile.phone == "+216 22 333 444"
        assert profile.full_name == "Ahmed Ben Ali"
        assert profile.booking_count == 0

    def test_regression_create_promotion(self, flight):
        """REG-PROMO-001: Vérifie la création d'une promotion."""
        promo = Promotion.objects.create(
            code="REGRESSION20",
            name="Test Régression -20%",
            description="Promotion de test pour vérifier la régression",
            promo_type="percentage",
            discount_percentage=Decimal("20.00"),
            start_date=timezone.now() - timedelta(days=1),
            end_date=timezone.now() + timedelta(days=30),
            max_uses=100,
            is_active=True,
            is_featured=True,
        )
        promo.flights.add(flight)
        assert promo.code == "REGRESSION20"
        assert promo.is_valid is True
        assert promo.remaining_uses == 100

    def test_regression_create_destination(self, airports):
        """REG-DESTINATION-001: Vérifie la création d'une destination."""
        dest = Destination.objects.create(
            name="Djerba",
            slug="djerba",
            description="Île paradisiaque au sud de la Tunisie",
            short_description="La perle du golfe de Gabès",
            airport=airports["tun"],
            category="beach",
            rating=Decimal("4.5"),
            is_featured=True,
            is_active=True,
        )
        assert dest.slug == "djerba"
        assert dest.category == "beach"
        assert dest.is_featured is True

    def test_regression_create_newsletter_subscription(self):
        """REG-NEWSLETTER-001: Vérifie la création d'un abonnement newsletter."""
        sub = NewsletterSubscription.objects.create(
            email="newsletter@test.tn",
            first_name="Fatma",
            is_active=True,
        )
        assert sub.email == "newsletter@test.tn"
        assert sub.is_active is True


# =============================================================================
# Régression: Vues - Pages critiques
# =============================================================================


@pytest.mark.regression
@pytest.mark.django_db
class TestViewRegression:
    """Tests de régression pour les vues critiques de l'application."""

    def test_regression_home_page_loads(self, client):
        """REG-VIEW-001: La page d'accueil doit charger avec un statut 200."""
        response = client.get(reverse("flights:home"))
        assert response.status_code == 200
        assert "flights/home.html" in [t.name for t in response.templates]

    def test_regression_login_page_loads(self, client):
        """REG-VIEW-002: La page de connexion doit charger avec un statut 200."""
        response = client.get(reverse("accounts:login"))
        assert response.status_code == 200
        assert "accounts/login.html" in [t.name for t in response.templates]

    def test_regression_register_page_loads(self, client):
        """REG-VIEW-003: La page d'inscription doit charger avec un statut 200."""
        response = client.get(reverse("accounts:register"))
        assert response.status_code == 200
        assert "accounts/register.html" in [t.name for t in response.templates]

    def test_regression_airport_list_page(self, client, airports):
        """REG-VIEW-004: La page de liste des aéroports doit charger."""
        response = client.get(reverse("flights:airport_list"))
        assert response.status_code == 200

    def test_regression_flight_search_page(self, client):
        """REG-VIEW-005: La page de recherche de vols doit charger."""
        response = client.get(reverse("flights:search_results"))
        assert response.status_code == 200

    def test_regression_flight_detail_page(self, client, flight):
        """REG-VIEW-006: La page de détail d'un vol doit charger."""
        response = client.get(
            reverse("flights:flight_detail", kwargs={"flight_number": flight.flight_number})
        )
        assert response.status_code == 200

    def test_regression_booking_create_page_requires_login(self, client):
        """REG-VIEW-007: La page de création de réservation nécessite une authentification."""
        response = client.get(reverse("bookings:create"))
        # Doit rediriger vers la page de connexion
        assert response.status_code in [302, 403]

    def test_regression_my_bookings_requires_login(self, client):
        """REG-VIEW-008: La page 'mes réservations' nécessite une authentification."""
        response = client.get(reverse("bookings:my_bookings"))
        assert response.status_code in [302, 403]

    def test_regression_destinations_list_page(self, client):
        """REG-VIEW-009: La page de liste des destinations doit charger."""
        response = client.get(reverse("destinations:list"))
        assert response.status_code == 200

    def test_regression_promotions_list_page(self, client):
        """REG-VIEW-010: La page de liste des promotions doit charger."""
        response = client.get(reverse("promotions:list"))
        assert response.status_code == 200


# =============================================================================
# Régression: Résolution d'URLs
# =============================================================================


@pytest.mark.regression
@pytest.mark.django_db
class TestURLResolutionRegression:
    """Tests de régression pour la résolution de toutes les URLs du projet."""

    def test_regression_url_flights_home(self):
        """REG-URL-001: Résolution de l'URL de la page d'accueil."""
        assert resolve("/").view_name == "flights:home"

    def test_regression_url_flights_search(self):
        """REG-URL-002: Résolution de l'URL de recherche de vols."""
        assert resolve("/recherche/").view_name == "flights:search_results"

    def test_regression_url_flights_airport_list(self):
        """REG-URL-003: Résolution de l'URL de la liste des aéroports."""
        assert resolve("/aeroports/").view_name == "flights:airport_list"

    def test_regression_url_accounts_login(self):
        """REG-URL-004: Résolution de l'URL de connexion."""
        assert resolve("/accounts/connexion/").view_name == "accounts:login"

    def test_regression_url_accounts_register(self):
        """REG-URL-005: Résolution de l'URL d'inscription."""
        assert resolve("/accounts/inscription/").view_name == "accounts:register"

    def test_regression_url_accounts_logout(self):
        """REG-URL-006: Résolution de l'URL de déconnexion."""
        assert resolve("/accounts/deconnexion/").view_name == "accounts:logout"

    def test_regression_url_accounts_profile(self):
        """REG-URL-007: Résolution de l'URL du profil."""
        assert resolve("/accounts/profil/").view_name == "accounts:profile"

    def test_regression_url_bookings_create(self):
        """REG-URL-008: Résolution de l'URL de création de réservation."""
        assert resolve("/bookings/creer/").view_name == "bookings:create"

    def test_regression_url_bookings_my_bookings(self):
        """REG-URL-009: Résolution de l'URL 'mes réservations'."""
        assert resolve("/bookings/mes-reservations/").view_name == "bookings:my_bookings"

    def test_regression_url_bookings_lookup(self):
        """REG-URL-010: Résolution de l'URL de recherche de réservation."""
        assert resolve("/bookings/recherche/").view_name == "bookings:lookup"

    def test_regression_url_destinations_list(self):
        """REG-URL-011: Résolution de l'URL de la liste des destinations."""
        assert resolve("/destinations/").view_name == "destinations:list"

    def test_regression_url_promotions_list(self):
        """REG-URL-012: Résolution de l'URL de la liste des promotions."""
        assert resolve("/promotions/").view_name == "promotions:list"

    def test_regression_url_legal(self):
        """REG-URL-013: Résolution de l'URL des mentions légales."""
        assert resolve("/mentions-legales/").view_name == "legal"

    def test_regression_url_terms(self):
        """REG-URL-014: Résolution de l'URL des conditions générales."""
        assert resolve("/conditions-generales/").view_name == "terms"


# =============================================================================
# Régression: Formulaires - Validations
# =============================================================================


@pytest.mark.regression
@pytest.mark.django_db
class TestFormValidationRegression:
    """Tests de régression pour la validation des formulaires critiques."""

    def test_regression_passenger_form_invalid_passport(self, airports, aircraft, user):
        """REG-FORM-001: Le formulaire passager rejette un passeport trop court."""
        from bookings.forms import PassengerForm
        from datetime import date as d

        departure = timezone.now() + timedelta(days=7)
        flight = Flight.objects.create(
            flight_number="BJ999", origin=airports["tun"],
            destination=airports["cdg"], aircraft=aircraft,
            departure_time=departure,
            arrival_time=departure + timedelta(hours=2),
            base_price_economy=Decimal("100.00"),
            base_price_business=Decimal("350.00"),
            available_seats_economy=100, available_seats_business=20,
        )
        booking = Booking.objects.create(
            user=user, contact_email="test@test.tn",
            contact_phone="+216 22 000 000",
            status="pending", total_amount=Decimal("100.00"),
        )
        form_data = {
            "title": "mr",
            "first_name": "Test",
            "last_name": "User",
            "date_of_birth": d(1990, 1, 1),
            "nationality": "Tunisienne",
            "passport_number": "AB",  # Trop court (< 5 caractères)
            "special_assistance": False,
            "meal_preference": "",
        }
        form = PassengerForm(data=form_data)
        assert not form.is_valid()
        assert "passport_number" in form.errors

    def test_regression_payment_form_invalid_card_number(self, booking):
        """REG-FORM-002: Le formulaire de paiement rejette un numéro de carte invalide."""
        from bookings.forms import PaymentForm

        form_data = {
            "card_number": "1234",  # Trop court
            "card_holder": "Test User",
            "expiry_date": "13/25",
            "cvv": "123",
            "method": "credit_card",
        }
        form = PaymentForm(data=form_data)
        assert not form.is_valid()
        assert "card_number" in form.errors

    def test_regression_flight_search_form_same_airports(self, airports):
        """REG-FORM-003: Le formulaire de recherche rejette départ = arrivée."""
        from flights.forms import FlightSearchForm

        form_data = {
            "trip_type": "oneway",
            "origin": airports["tun"].pk,
            "destination": airports["tun"].pk,  # Même aéroport !
            "departure_date": date.today() + timedelta(days=7),
            "return_date": "",
            "passengers": 1,
            "travel_class": "economy",
        }
        form = FlightSearchForm(data=form_data)
        assert not form.is_valid()
        assert "__all__" in form.errors

    def test_regression_flight_search_form_past_date(self, airports):
        """REG-FORM-004: Le formulaire de recherche rejette une date passée."""
        from flights.forms import FlightSearchForm

        form_data = {
            "trip_type": "oneway",
            "origin": airports["tun"].pk,
            "destination": airports["cdg"].pk,
            "departure_date": date.today() - timedelta(days=1),  # Date passée
            "return_date": "",
            "passengers": 1,
            "travel_class": "economy",
        }
        form = FlightSearchForm(data=form_data)
        assert not form.is_valid()

    def test_regression_flight_search_form_roundtrip_invalid_dates(self, airports):
        """REG-FORM-005: Le formulaire rejette retour avant départ."""
        from flights.forms import FlightSearchForm

        dep_date = date.today() + timedelta(days=7)
        form_data = {
            "trip_type": "roundtrip",
            "origin": airports["tun"].pk,
            "destination": airports["cdg"].pk,
            "departure_date": str(dep_date),
            "return_date": str(dep_date - timedelta(days=1)),  # Avant le départ
            "passengers": 1,
            "travel_class": "economy",
        }
        form = FlightSearchForm(data=form_data)
        assert not form.is_valid()


# =============================================================================
# Régression: Authentification
# =============================================================================


@pytest.mark.regression
@pytest.mark.django_db
class TestAuthenticationRegression:
    """Tests de régression pour les flux d'authentification."""

    def test_regression_user_can_register(self, client):
        """REG-AUTH-001: Un utilisateur peut s'inscrire avec des données valides."""
        response = client.post(
            reverse("accounts:register"),
            {
                "username": "newuser_regression",
                "first_name": "Salma",
                "last_name": "Gharbi",
                "email": "salma.regression@test.tn",
                "password1": "SecurePass123!",
                "password2": "SecurePass123!",
            },
            follow=True,
        )
        assert User.objects.filter(username="newuser_regression").exists()
        assert response.status_code == 200

    def test_regression_user_can_login(self, client, user):
        """REG-AUTH-002: Un utilisateur peut se connecter avec des identifiants valides."""
        response = client.post(
            reverse("accounts:login"),
            {"username": "regression_user", "password": "TestPass123!"},
            follow=True,
        )
        assert response.status_code == 200
        # Vérifie que l'utilisateur est connecté
        assert "_auth_user_id" in client.session

    def test_regression_user_cannot_login_invalid(self, client, user):
        """REG-AUTH-003: La connexion échoue avec un mot de passe incorrect."""
        response = client.post(
            reverse("accounts:login"),
            {"username": "regression_user", "password": "WrongPass999"},
        )
        assert "_auth_user_id" not in client.session

    def test_regression_user_can_logout(self, client, user):
        """REG-AUTH-004: Un utilisateur peut se déconnecter."""
        client.force_login(user)
        assert "_auth_user_id" in client.session
        response = client.get(reverse("accounts:logout"), follow=True)
        assert "_auth_user_id" not in client.session
        assert response.status_code == 200

    def test_regression_profile_page_authenticated(self, client, user_with_profile):
        """REG-AUTH-005: La page de profil est accessible pour un utilisateur authentifié."""
        client.force_login(user_with_profile)
        response = client.get(reverse("accounts:profile"))
        assert response.status_code == 200


# =============================================================================
# Régression: Statuts de réservation
# =============================================================================


@pytest.mark.regression
@pytest.mark.django_db
class TestBookingStatusRegression:
    """Tests de régression pour les transitions de statut des réservations."""

    @pytest.mark.parametrize("status", ["pending", "confirmed", "cancelled", "completed", "refunded"])
    def test_regression_all_booking_statuses_valid(self, booking, status):
        """REG-STATUS-001: Tous les statuts de réservation sont valides."""
        booking.status = status
        booking.save()
        booking.refresh_from_db()
        assert booking.status == status
        assert booking.get_status_display() is not None

    def test_regression_booking_default_status(self, user):
        """REG-STATUS-002: Le statut par défaut d'une réservation est 'pending'."""
        booking = Booking.objects.create(
            user=user,
            contact_email="default@test.tn",
            contact_phone="+216 22 000 000",
            total_amount=Decimal("50.00"),
        )
        assert booking.status == "pending"

    def test_regression_booking_status_transition_pending_to_confirmed(self, booking):
        """REG-STATUS-003: Transition pending → confirmed."""
        booking.status = "confirmed"
        booking.save()
        assert booking.status == "confirmed"

    def test_regression_booking_status_transition_confirmed_to_cancelled(self, booking):
        """REG-STATUS-004: Transition confirmed → cancelled."""
        booking.status = "confirmed"
        booking.save()
        booking.status = "cancelled"
        booking.save()
        assert booking.status == "cancelled"

    def test_regression_booking_str_representation(self, booking):
        """REG-STATUS-005: La représentation string d'une réservation est correcte."""
        assert "Réservation" in str(booking)
        assert "En attente" in str(booking) or "pending" in str(booking).lower()


# =============================================================================
# Régression: Recherche de vols
# =============================================================================


@pytest.mark.regression
@pytest.mark.django_db
class TestFlightSearchRegression:
    """Tests de régression pour la recherche de vols."""

    def test_regression_search_flights_returns_results(self, flight):
        """REG-SEARCH-001: La recherche de vols retourne des résultats corrects."""
        departure_date = flight.departure_time.date()
        results = Flight.search_flights("TUN", "CDG", departure_date)
        assert flight in results

    def test_regression_search_flights_no_results(self, flight):
        """REG-SEARCH-002: La recherche ne retourne rien si aucun vol ne correspond."""
        results = Flight.search_flights("TUN", "AMS", date.today() + timedelta(days=14))
        assert flight not in results
        assert len(results) == 0

    def test_regression_search_flights_business_class(self, flight, airports, aircraft):
        """REG-SEARCH-003: La recherche en classe affaires filtre correctement."""
        results = Flight.search_flights(
            "TUN", "CDG", flight.departure_time.date(),
            passengers=1, travel_class="business"
        )
        assert flight in results

    def test_regression_search_flights_excludes_inactive(self, flight):
        """REG-SEARCH-004: La recherche exclut les vols inactifs."""
        flight.is_active = False
        flight.save()
        results = Flight.search_flights("TUN", "CDG", flight.departure_time.date())
        assert flight not in results

