"""
Tests unitaires pour l'application Destinations.
"""

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from destinations.models import Destination, DestinationReview
from flights.models import Airport


class DestinationModelTest(TestCase):
    """Tests du modèle Destination."""

    def setUp(self):
        self.airport = Airport.objects.create(
            code="DJE", name="Aéroport Djerba", city="Djerba",
            country="Tunisie", latitude=33.88, longitude=10.78
        )
        self.destination = Destination.objects.create(
            name="Djerba - L'île des rêves",
            slug="djerba-ile-des-reves",
            description="Djerba est une magnifique île tunisienne...",
            short_description="L'île aux mille couleurs",
            airport=self.airport,
            category="beach",
            rating=4.5,
            is_featured=True
        )

    def test_destination_creation(self):
        """Vérifie la création correcte d'une destination."""
        self.assertEqual(self.destination.name, "Djerba - L'île des rêves")
        self.assertTrue(self.destination.is_featured)

    def test_destination_str(self):
        """Vérifie la représentation string."""
        self.assertEqual(str(self.destination), "Djerba - L'île des rêves")

    def test_get_lowest_price(self):
        """Vérifie la méthode de prix le plus bas."""
        price = self.destination.get_lowest_price()
        # Pas de vol, donc None
        self.assertIsNone(price)

    def test_unique_slug(self):
        """Vérifie l'unicité du slug."""
        with self.assertRaises(Exception):
            Destination.objects.create(
                name="Djerba 2",
                slug="djerba-ile-des-reves",
                description="Test",
                short_description="Test",
                category="beach",
            )


class DestinationReviewTest(TestCase):
    """Tests du modèle DestinationReview."""

    def setUp(self):
        self.user = User.objects.create_user(username='reviewer', password='pass')
        self.airport = Airport.objects.create(
            code="DJE", name="Aéroport Djerba", city="Djerba",
            country="Tunisie", latitude=33.88, longitude=10.78
        )
        self.destination = Destination.objects.create(
            name="Djerba", slug="djerba",
            description="Description", short_description="Courte",
            airport=self.airport, category="beach"
        )

    def test_review_creation(self):
        """Vérifie la création d'un avis."""
        review = DestinationReview.objects.create(
            destination=self.destination,
            user=self.user,
            rating=5,
            title="Magnifique !",
            comment="Un endroit paradisiaque."
        )
        self.assertEqual(review.rating, 5)
        self.assertFalse(review.is_approved)

    def test_unique_review_per_user(self):
        """Vérifie qu'un utilisateur ne peut laisser qu'un avis par destination."""
        DestinationReview.objects.create(
            destination=self.destination, user=self.user,
            rating=4, title="Bien", comment="Bon séjour"
        )
        with self.assertRaises(Exception):
            DestinationReview.objects.create(
                destination=self.destination, user=self.user,
                rating=5, title="Super", comment="Superbe"
            )


class DestinationViewTest(TestCase):
    """Tests des vues de l'application Destinations."""

    def setUp(self):
        self.airport = Airport.objects.create(
            code="DJE", name="Aéroport Djerba", city="Djerba",
            country="Tunisie", latitude=33.88, longitude=10.78
        )
        self.destination = Destination.objects.create(
            name="Djerba", slug="djerba",
            description="Une île magnifique en Tunisie",
            short_description="L'île aux palmiers",
            airport=self.airport, category="beach", rating=4.5
        )

    def test_destination_list(self):
        """Vérifie l'accès à la liste des destinations."""
        response = self.client.get(reverse('destinations:list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Djerba")

    def test_destination_detail(self):
        """Vérifie l'accès au détail d'une destination."""
        response = self.client.get(
            reverse('destinations:detail', kwargs={'slug': 'djerba'})
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Djerba")

    def test_destination_detail_404(self):
        """Vérifie le 404 pour un slug invalide."""
        response = self.client.get(
            reverse('destinations:detail', kwargs={'slug': 'inexistant'})
        )
        self.assertEqual(response.status_code, 404)
