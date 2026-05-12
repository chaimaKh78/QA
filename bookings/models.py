"""
Modèles Booking - Gestion des réservations.
"""

import uuid
from django.db import models
from django.conf import settings

from django.core.validators import MinValueValidator


class Booking(models.Model):
    """Modèle principal de réservation."""

    BOOKING_STATUS_CHOICES = [
        ('pending', 'En attente'),
        ('confirmed', 'Confirmée'),
        ('cancelled', 'Annulée'),
        ('completed', 'Terminée'),
        ('refunded', 'Remboursée'),
    ]

    reference = models.UUIDField(
        default=uuid.uuid4, unique=True, editable=False,
        verbose_name="Référence de réservation"
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='bookings', verbose_name="Utilisateur",
        null=True, blank=True
    )
    contact_email = models.EmailField(verbose_name="Email de contact")
    contact_phone = models.CharField(max_length=20, verbose_name="Téléphone de contact")
    status = models.CharField(
        max_length=20, choices=BOOKING_STATUS_CHOICES,
        default='pending', verbose_name="Statut"
    )
    total_amount = models.DecimalField(
        max_digits=10, decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name="Montant total (TND)"
    )
    special_requests = models.TextField(
        blank=True, verbose_name="Demandes spéciales"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Réservation"
        verbose_name_plural = "Réservations"
        ordering = ['-created_at']

    def __str__(self):
        return f"Réservation {str(self.reference)[:8].upper()} - {self.get_status_display()}"

    @property
    def short_reference(self):
        return str(self.reference)[:8].upper()


class Passenger(models.Model):
    """Modèle représentant un passager d'une réservation."""

    TITLE_CHOICES = [
        ('mr', 'Monsieur'),
        ('mme', 'Madame'),
        ('mll', 'Mademoiselle'),
        ('enf', 'Enfant'),
    ]

    TRAVEL_CLASS_CHOICES = [
        ('economy', 'Économie'),
        ('business', 'Affaires'),
    ]

    booking = models.ForeignKey(
        Booking, on_delete=models.CASCADE,
        related_name='passengers', verbose_name="Réservation"
    )
    flight = models.ForeignKey(
        'flights.Flight', on_delete=models.PROTECT,
        related_name='passengers', verbose_name="Vol"
    )
    title = models.CharField(
        max_length=4, choices=TITLE_CHOICES, verbose_name="Titre"
    )
    first_name = models.CharField(max_length=100, verbose_name="Prénom")
    last_name = models.CharField(max_length=100, verbose_name="Nom")
    date_of_birth = models.DateField(verbose_name="Date de naissance")
    nationality = models.CharField(max_length=100, verbose_name="Nationalité")
    passport_number = models.CharField(
        max_length=50, blank=True, verbose_name="Numéro de passeport"
    )
    passport_expiry = models.DateField(
        null=True, blank=True, verbose_name="Expiration du passeport"
    )
    travel_class = models.CharField(
        max_length=10, choices=TRAVEL_CLASS_CHOICES,
        default='economy', verbose_name="Classe de voyage"
    )
    seat_number = models.CharField(
        max_length=5, blank=True, verbose_name="Numéro de siège"
    )
    price = models.DecimalField(
        max_digits=10, decimal_places=2,
        verbose_name="Prix payé (TND)"
    )
    special_assistance = models.BooleanField(
        default=False, verbose_name="Assistance spéciale requise"
    )
    meal_preference = models.CharField(
        max_length=50, blank=True, verbose_name="Préférence alimentaire"
    )

    class Meta:
        verbose_name = "Passager"
        verbose_name_plural = "Passagers"

    def __str__(self):
        return f"{self.get_title_display()} {self.first_name} {self.last_name}"


class Payment(models.Model):
    """Modèle de paiement associé à une réservation."""

    PAYMENT_METHOD_CHOICES = [
        ('credit_card', 'Carte de crédit'),
        ('debit_card', 'Carte de débit'),
        ('bank_transfer', 'Virement bancaire'),
        ('cash', 'Espèces'),
    ]

    PAYMENT_STATUS_CHOICES = [
        ('pending', 'En attente'),
        ('completed', 'Complété'),
        ('failed', 'Échoué'),
        ('refunded', 'Remboursé'),
    ]

    booking = models.ForeignKey(
        Booking, on_delete=models.CASCADE,
        related_name='payments', verbose_name="Réservation"
    )
    amount = models.DecimalField(
        max_digits=10, decimal_places=2,
        verbose_name="Montant (TND)"
    )
    method = models.CharField(
        max_length=20, choices=PAYMENT_METHOD_CHOICES,
        verbose_name="Méthode de paiement"
    )
    status = models.CharField(
        max_length=20, choices=PAYMENT_STATUS_CHOICES,
        default='pending', verbose_name="Statut"
    )
    transaction_id = models.CharField(
        max_length=200, blank=True, verbose_name="ID de transaction"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Paiement"
        verbose_name_plural = "Paiements"
        ordering = ['-created_at']

    def __str__(self):
        return f"Paiement {self.amount} TND - {self.get_status_display()}"
