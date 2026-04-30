"""
Modèles Promotions - Gestion des offres et promotions.
"""

from django.db import models
from django.utils import timezone


class Promotion(models.Model):
    """Modèle représentant une promotion ou offre spéciale."""

    PROMO_TYPE_CHOICES = [
        ('percentage', 'Pourcentage'),
        ('fixed', 'Montant fixe'),
        ('buy_one_get_one', 'Un acheté, un offert'),
        ('free_upgrade', 'Surclassement gratuit'),
    ]

    code = models.CharField(
        max_length=50, unique=True, verbose_name="Code promo"
    )
    name = models.CharField(max_length=200, verbose_name="Nom de la promotion")
    description = models.TextField(verbose_name="Description")
    promo_type = models.CharField(
        max_length=20, choices=PROMO_TYPE_CHOICES,
        verbose_name="Type de promotion"
    )
    discount_percentage = models.DecimalField(
        max_digits=5, decimal_places=2,
        default=0, verbose_name="Remise (%)"
    )
    discount_amount = models.DecimalField(
        max_digits=10, decimal_places=2,
        default=0, verbose_name="Remise (TND)"
    )
    start_date = models.DateTimeField(verbose_name="Date de début")
    end_date = models.DateTimeField(verbose_name="Date de fin")
    max_uses = models.PositiveIntegerField(
        default=100, verbose_name="Nombre max d'utilisations"
    )
    current_uses = models.PositiveIntegerField(
        default=0, verbose_name="Utilisations actuelles"
    )
    min_purchase_amount = models.DecimalField(
        max_digits=10, decimal_places=2,
        default=0, verbose_name="Montant minimum d'achat"
    )
    flights = models.ManyToManyField(
        'flights.Flight', blank=True,
        related_name='promotions',
        verbose_name="Vols applicables"
    )
    is_active = models.BooleanField(default=True, verbose_name="Active")
    is_featured = models.BooleanField(default=False, verbose_name="Mise en avant")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Promotion"
        verbose_name_plural = "Promotions"
        ordering = ['-is_featured', '-start_date']

    def __str__(self):
        return f"{self.code} - {self.name}"

    @property
    def is_valid(self):
        """Vérifie si la promotion est encore valide."""
        now = timezone.now()
        return (
            self.is_active and
            self.start_date <= now <= self.end_date and
            self.current_uses < self.max_uses
        )

    @property
    def remaining_uses(self):
        return max(0, self.max_uses - self.current_uses)


class NewsletterSubscription(models.Model):
    """Abonnements à la newsletter."""

    email = models.EmailField(unique=True, verbose_name="Email")
    first_name = models.CharField(max_length=100, blank=True, verbose_name="Prénom")
    is_active = models.BooleanField(default=True, verbose_name="Actif")
    subscribed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Abonnement newsletter"
        verbose_name_plural = "Abonnements newsletter"
        ordering = ['-subscribed_at']

    def __str__(self):
        return self.email
