"""
Modèles Account - Profils utilisateurs.
"""

from django.db import models
from django.conf import settings
from django.contrib.auth.models import User


class UserProfile(models.Model):
    """Profil étendu de l'utilisateur."""

    GENDER_CHOICES = [
        ('M', 'Masculin'),
        ('F', 'Féminin'),
    ]

    user = models.OneToOneField(
        User, on_delete=models.CASCADE,
        related_name='profile', verbose_name="Utilisateur"
    )
    phone = models.CharField(max_length=20, blank=True, verbose_name="Téléphone")
    address = models.TextField(blank=True, verbose_name="Adresse")
    city = models.CharField(max_length=100, blank=True, verbose_name="Ville")
    country = models.CharField(max_length=100, blank=True, verbose_name="Pays")
    date_of_birth = models.DateField(null=True, blank=True, verbose_name="Date de naissance")
    nationality = models.CharField(max_length=100, blank=True, verbose_name="Nationalité")
    passport_number = models.CharField(max_length=50, blank=True, verbose_name="Passeport")
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, verbose_name="Genre")
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True, verbose_name="Avatar")
    newsletter = models.BooleanField(default=False, verbose_name="Newsletter")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Profil utilisateur"
        verbose_name_plural = "Profils utilisateurs"

    def __str__(self):
        return f"Profil de {self.user.get_full_name() or self.user.username}"

    @property
    def full_name(self):
        return self.user.get_full_name() or self.user.username

    @property
    def booking_count(self):
        return self.user.bookings.count()


class SavedDestination(models.Model):
    """Destinations favorites d'un utilisateur."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='saved_destinations'
    )
    airport = models.ForeignKey(
        'flights.Airport', on_delete=models.CASCADE,
        related_name='saved_by'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Destination favorite"
        verbose_name_plural = "Destinations favorites"
        unique_together = ('user', 'airport')

    def __str__(self):
        return f"{self.user.username} → {self.airport.city}"
