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
        assert destination.category == category
        assert destination.get_category_display()

    def test_destination_str(self):
        """Test que __str__ retourne le nom de la destination."""
        assert str(destination) == "Djerba"

    def test_get_lowest_price(self):
        """Test de la methode get_lowest_price."""
        airport = AirportFactory(code="TUN")
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
        user = User.objects.create_user(username="reviewer1", email="rev1@test.com")
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
        user = User.objects.create_user(username="reviewer2", email="rev2@test.com")
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
        assert review.rating >= 1
        assert review.rating <= 5

        assert review5.rating == 5
