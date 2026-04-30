"""
Tests unitaires pour l'application Promotions.
"""

from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta
from promotions.models import Promotion, NewsletterSubscription
from flights.models import Airport, Aircraft, Flight


class PromotionModelTest(TestCase):
    """Tests du modèle Promotion."""

    def setUp(self):
        self.promotion = Promotion.objects.create(
            code="PROMO50",
            name="Réduction 50%",
            description="50% de réduction sur tous les vols",
            promo_type="percentage",
            discount_percentage=50,
            start_date=timezone.now() - timedelta(days=1),
            end_date=timezone.now() + timedelta(days=30),
            max_uses=100,
            current_uses=10
        )

    def test_promotion_creation(self):
        """Vérifie la création correcte d'une promotion."""
        self.assertEqual(self.promotion.code, "PROMO50")
        self.assertEqual(self.promotion.discount_percentage, 50)

    def test_promotion_is_valid(self):
        """Vérifie la validité d'une promotion active."""
        self.assertTrue(self.promotion.is_valid)

    def test_promotion_expired(self):
        """Vérifie qu'une promotion expirée n'est pas valide."""
        expired_promo = Promotion.objects.create(
            code="EXPIRED",
            name="Expirée",
            description="Promotion expirée",
            promo_type="percentage",
            start_date=timezone.now() - timedelta(days=60),
            end_date=timezone.now() - timedelta(days=30),
        )
        self.assertFalse(expired_promo.is_valid)

    def test_promotion_max_uses_reached(self):
        """Vérifie qu'une promotion épuisée n'est pas valide."""
        full_promo = Promotion.objects.create(
            code="FULL",
            name="Épuisée",
            description="Plus d'utilisations",
            promo_type="percentage",
            start_date=timezone.now() - timedelta(days=1),
            end_date=timezone.now() + timedelta(days=30),
            max_uses=10,
            current_uses=10,
        )
        self.assertFalse(full_promo.is_valid)

    def test_remaining_uses(self):
        """Vérifie le calcul des utilisations restantes."""
        self.assertEqual(self.promotion.remaining_uses, 90)


class PromotionViewTest(TestCase):
    """Tests des vues de l'application Promotions."""

    def test_promotion_list(self):
        """Vérifie l'accès à la liste des promotions."""
        response = self.client.get(reverse('promotions:list'))
        self.assertEqual(response.status_code, 200)

    def test_promotion_detail(self):
        """Vérifie l'accès au détail d'une promotion."""
        Promotion.objects.create(
            code="TEST",
            name="Test Promo",
            description="Description",
            promo_type="percentage",
            start_date=timezone.now() - timedelta(days=1),
            end_date=timezone.now() + timedelta(days=30),
        )
        response = self.client.get(
            reverse('promotions:detail', kwargs={'code': 'TEST'})
        )
        self.assertEqual(response.status_code, 200)

    def test_newsletter_subscribe_success(self):
        """Vérifie l'inscription à la newsletter."""
        response = self.client.post(reverse('promotions:newsletter_subscribe'), {
            'email': 'test@example.com',
            'first_name': 'Test',
        })
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data['success'])

    def test_newsletter_subscribe_duplicate(self):
        """Vérifie qu'on ne peut pas s'inscrire deux fois."""
        NewsletterSubscription.objects.create(email='test@example.com')
        response = self.client.post(reverse('promotions:newsletter_subscribe'), {
            'email': 'test@example.com',
        })
        data = response.json()
        self.assertFalse(data['success'])

    def test_newsletter_subscribe_missing_email(self):
        """Vérifie que l'email est requis."""
        response = self.client.post(reverse('promotions:newsletter_subscribe'), {
            'email': '',
        })
        data = response.json()
        self.assertFalse(data['success'])
