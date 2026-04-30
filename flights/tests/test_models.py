"""
Tests unitaires pour l'application Flights.
"""

from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from datetime import date, timedelta
from flights.models import Airport, Aircraft, Flight


class AirportModelTest(TestCase):
    """Tests du modèle Airport."""

    def setUp(self):
        self.airport = Airport.objects.create(
            code="TUN",
            name="Aéroport International Tunis-Carthage",
            city="Tunis",
            country="Tunisie",
            latitude=36.8510,
            longitude=10.2272
        )

    def test_airport_creation(self):
        """Vérifie la création correcte d'un aéroport."""
        self.assertEqual(self.airport.code, "TUN")
        self.assertEqual(self.airport.city, "Tunis")
        self.assertTrue(self.airport.is_active)

    def test_airport_str_representation(self):
        """Vérifie la représentation string de l'aéroport."""
        expected = "TUN - Tunis (Tunisie)"
        self.assertEqual(str(self.airport), expected)

    def test_airport_ordering(self):
        """Vérifie l'ordre de tri des aéroports par code."""
        Airport.objects.create(
            code="CDG", name="Aéroport CDG", city="Paris",
            country="France", latitude=49.0, longitude=2.5
        )
        airports = list(Airport.objects.all())
        self.assertEqual(airports[0].code, "CDG")
        self.assertEqual(airports[1].code, "TUN")

    def test_airport_unique_code(self):
        """Vérifie que le code IATA est unique."""
        with self.assertRaises(Exception):
            Airport.objects.create(
                code="TUN", name="Autre aéroport", city="Test",
                country="Test", latitude=0, longitude=0
            )


class AircraftModelTest(TestCase):
    """Tests du modèle Aircraft."""

    def setUp(self):
        self.aircraft = Aircraft.objects.create(
            model_name="Airbus A320-200",
            registration="TS-INA",
            total_seats=174,
            economy_seats=150,
            business_seats=24
        )

    def test_aircraft_creation(self):
        """Vérifie la création correcte d'un aéronef."""
        self.assertEqual(self.aircraft.model_name, "Airbus A320-200")
        self.assertEqual(self.aircraft.total_seats, 174)

    def test_aircraft_str(self):
        """Vérifie la représentation string."""
        self.assertIn("Airbus A320-200", str(self.aircraft))
        self.assertIn("TS-INA", str(self.aircraft))

    def test_seats_sum(self):
        """Vérifie que économie + affaires = total."""
        self.assertEqual(
            self.aircraft.economy_seats + self.aircraft.business_seats,
            self.aircraft.total_seats
        )


class FlightModelTest(TestCase):
    """Tests du modèle Flight."""

    def setUp(self):
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

    def test_flight_creation(self):
        """Vérifie la création correcte d'un vol."""
        self.assertEqual(self.flight.flight_number, "BJ123")
        self.assertEqual(self.flight.status, "scheduled")
        self.assertAlmostEqual(float(self.flight.base_price_economy), 350.00)

    def test_flight_duration_auto_calculated(self):
        """Vérifie que la durée est calculée automatiquement."""
        self.assertIsNotNone(self.flight.duration)
        self.assertEqual(self.flight.duration, timedelta(hours=2, minutes=30))

    def test_flight_str(self):
        """Vérifie la représentation string du vol."""
        self.assertIn("BJ123", str(self.flight))
        self.assertIn("TUN", str(self.flight))
        self.assertIn("CDG", str(self.flight))

    def test_flight_search(self):
        """Vérifie la méthode de recherche de vols."""
        results = Flight.search_flights(
            origin_code="TUN",
            destination_code="CDG",
            departure_date=date.today() + timedelta(days=5),
            passengers=1
        )
        self.assertEqual(results.count(), 1)

    def test_flight_search_no_results(self):
        """Vérifie que la recherche renvoie vide si pas de résultats."""
        results = Flight.search_flights(
            origin_code="TUN",
            destination_code="DJE",
            departure_date=date.today() + timedelta(days=5),
            passengers=1
        )
        self.assertEqual(results.count(), 0)

    def test_price_methods(self):
        """Vérifie les méthodes de prix."""
        price_eco = self.flight.get_current_price_economy()
        price_bus = self.flight.get_current_price_business()
        self.assertGreater(price_eco, 0)
        self.assertGreater(price_bus, price_eco)


class FlightViewTest(TestCase):
    """Tests des vues de l'application Flights."""

    def setUp(self):
        self.client = Client()
        self.airport1 = Airport.objects.create(
            code="TUN", name="Aéroport Tunis", city="Tunis",
            country="Tunisie", latitude=36.85, longitude=10.23
        )
        self.airport2 = Airport.objects.create(
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
            origin=self.airport1,
            destination=self.airport2,
            aircraft=self.aircraft,
            departure_time=departure,
            arrival_time=arrival,
            base_price_economy=350.00,
            base_price_business=850.00,
            available_seats_economy=150,
            available_seats_business=24,
        )

    def test_home_view_status(self):
        """Vérifie que la page d'accueil est accessible."""
        response = self.client.get(reverse('flights:home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'NouvelAir')
        self.assertTemplateUsed(response, 'flights/home.html')

    def test_home_view_contains_form(self):
        """Vérifie que la page d'accueil contient le formulaire de recherche."""
        response = self.client.get(reverse('flights:home'))
        self.assertContains(response, 'Rechercher un vol')

    def test_flight_detail_view(self):
        """Vérifie la page de détail d'un vol."""
        response = self.client.get(
            reverse('flights:flight_detail', kwargs={'flight_number': 'BJ123'})
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'BJ123')

    def test_airport_list_view(self):
        """Vérifie la page de liste des aéroports."""
        response = self.client.get(reverse('flights:airport_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'TUN')

    def test_airport_autocomplete(self):
        """Vérifie l'API d'autocomplétion des aéroports."""
        response = self.client.get(
            reverse('flights:airport_autocomplete'), {'q': 'TUN'}
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(len(data) > 0)

    def test_search_flight_post(self):
        """Vérifie la soumission du formulaire de recherche."""
        response = self.client.post(reverse('flights:home'), {
            'trip_type': 'oneway',
            'origin': self.airport1.pk,
            'destination': self.airport2.pk,
            'departure_date': (date.today() + timedelta(days=5)).strftime('%Y-%m-%d'),
            'passengers': 1,
            'travel_class': 'economy',
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('flights:search_results'))

    def test_search_same_airport_error(self):
        """Vérifie qu'on ne peut pas chercher avec le même aéroport."""
        response = self.client.post(reverse('flights:home'), {
            'trip_type': 'oneway',
            'origin': self.airport1.pk,
            'destination': self.airport1.pk,
            'departure_date': (date.today() + timedelta(days=5)).strftime('%Y-%m-%d'),
            'passengers': 1,
            'travel_class': 'economy',
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'différents')
