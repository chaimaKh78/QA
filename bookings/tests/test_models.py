"""
Tests unitaires pour l'application Bookings.
"""

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import date, timedelta
from flights.models import Airport, Aircraft, Flight
from bookings.models import Booking, Passenger, Payment


class BookingModelTest(TestCase):
    """Tests du modèle Booking."""

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='testpass123'
        )
        self.origin = Airport.objects.create(
            code="TUN", name="Aéroport Tunis", city="Tunis",
            country="Tunisie", latitude=36.85, longitude=10.23
        )
        self.destination = Airport.objects.create(
            code="CDG", name="Aéroport CDG", city="Paris",
            country="France", latitude=49.01, longitude=2.55
        )
        self.aircraft = Aircraft.objects.create(
            model_name="A320", registration="TS-INA",
            total_seats=174, economy_seats=150, business_seats=24
        )
        departure = timezone.now() + timedelta(days=5)
        arrival = departure + timedelta(hours=2.5)
        self.flight = Flight.objects.create(
            flight_number="BJ123",
            origin=self.origin,
            destination=self.destination,
            aircraft=self.aircraft,
            departure_time=departure,
            arrival_time=arrival,
            base_price_economy=350.00,
            base_price_business=850.00,
            available_seats_economy=150,
            available_seats_business=24,
        )

    def test_booking_creation(self):
        """Vérifie la création correcte d'une réservation."""
        booking = Booking.objects.create(
            user=self.user,
            contact_email="test@example.com",
            contact_phone="+21612345678",
            status="confirmed",
            total_amount=350.00
        )
        self.assertIsNotNone(booking.reference)
        self.assertEqual(booking.short_reference, str(booking.reference)[:8].upper())

    def test_booking_str(self):
        """Vérifie la représentation string."""
        booking = Booking.objects.create(
            contact_email="test@example.com",
            contact_phone="+21612345678",
            status="confirmed",
            total_amount=350.00
        )
        self.assertIn("Confirmée", str(booking))

    def test_passenger_creation(self):
        """Vérifie la création d'un passager."""
        booking = Booking.objects.create(
            contact_email="test@example.com",
            contact_phone="+21612345678",
            status="confirmed",
            total_amount=350.00
        )
        passenger = Passenger.objects.create(
            booking=booking,
            flight=self.flight,
            title="mr",
            first_name="Mohamed",
            last_name="Ben Ali",
            date_of_birth=date(1990, 1, 15),
            nationality="Tunisienne",
            travel_class="economy",
            price=350.00
        )
        self.assertEqual(str(passenger), "Monsieur Mohamed Ben Ali")

    def test_payment_creation(self):
        """Vérifie la création d'un paiement."""
        booking = Booking.objects.create(
            contact_email="test@example.com",
            contact_phone="+21612345678",
            status="confirmed",
            total_amount=350.00
        )
        payment = Payment.objects.create(
            booking=booking,
            amount=350.00,
            method="credit_card",
            status="completed",
            transaction_id="SIM-TEST"
        )
        self.assertEqual(payment.amount, 350.00)


class BookingViewTest(TestCase):
    """Tests des vues de l'application Bookings."""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser', password='testpass123'
        )
        self.origin = Airport.objects.create(
            code="TUN", name="Aéroport Tunis", city="Tunis",
            country="Tunisie", latitude=36.85, longitude=10.23
        )
        self.destination = Airport.objects.create(
            code="CDG", name="Aéroport CDG", city="Paris",
            country="France", latitude=49.01, longitude=2.55
        )
        self.aircraft = Aircraft.objects.create(
            model_name="A320", registration="TS-INA",
            total_seats=174, economy_seats=150, business_seats=24
        )
        departure = timezone.now() + timedelta(days=5)
        arrival = departure + timedelta(hours=2.5)
        self.flight = Flight.objects.create(
            flight_number="BJ123",
            origin=self.origin,
            destination=self.destination,
            aircraft=self.aircraft,
            departure_time=departure,
            arrival_time=arrival,
            base_price_economy=350.00,
            base_price_business=850.00,
            available_seats_economy=150,
            available_seats_business=24,
        )

    def test_booking_lookup_page(self):
        """Vérifie l'accès à la page de recherche de réservation."""
        response = self.client.get(reverse('bookings:lookup'))
        self.assertEqual(response.status_code, 200)

    def test_my_bookings_requires_login(self):
        """Vérifie que mes réservations nécessite une connexion."""
        response = self.client.get(reverse('bookings:my_bookings'))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/accounts/login'))

    def test_my_bookings_authenticated(self):
        """Vérifie l'accès aux réservations quand connecté."""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('bookings:my_bookings'))
        self.assertEqual(response.status_code, 200)

    def test_select_flight_redirect(self):
        """Vérifie la sélection de vol."""
        session = self.client.session
        session['search_params'] = {
            'origin': 'TUN', 'destination': 'CDG',
            'departure_date': (date.today() + timedelta(days=5)).isoformat(),
            'passengers': 1, 'travel_class': 'economy', 'trip_type': 'oneway'
        }
        session.save()

        response = self.client.get(
            reverse('bookings:select_flight', kwargs={'flight_id': self.flight.id})
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.client.session.get('booking_flight_id'), self.flight.id)

    def test_booking_cancellation(self):
        """Vérifie l'annulation d'une réservation."""
        booking = Booking.objects.create(
            user=self.user,
            contact_email="test@example.com",
            contact_phone="+21612345678",
            status="confirmed",
            total_amount=350.00
        )
        response = self.client.post(
            reverse('bookings:cancel', kwargs={'reference': booking.reference})
        )
        booking.refresh_from_db()
        self.assertEqual(booking.status, 'cancelled')
