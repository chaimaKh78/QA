"""
Modèles Destinations - Gestion des destinations touristiques.
"""

from django.db import models
from django.utils import timezone


class Destination(models.Model):
    """Modèle représentant une destination touristique."""

    CATEGORY_CHOICES = [
        ('beach', 'Plage'),
        ('culture', 'Culture'),
        ('adventure', 'Aventure'),
        ('relaxation', 'Détente'),
        ('urban', 'Urbain'),
        ('nature', 'Nature'),
    ]

    name = models.CharField(max_length=200, verbose_name="Nom")
    slug = models.SlugField(unique=True, verbose_name="Slug")
    description = models.TextField(verbose_name="Description")
    short_description = models.CharField(max_length=300, verbose_name="Description courte")
    airport = models.ForeignKey(
        'flights.Airport', on_delete=models.SET_NULL,
        null=True, blank=True, related_name='destinations',
        verbose_name="Aéroport associé"
    )
    category = models.CharField(
        max_length=20, choices=CATEGORY_CHOICES,
        verbose_name="Catégorie"
    )
    image = models.ImageField(
        upload_to='destinations/', blank=True, null=True,
        verbose_name="Image principale"
    )
    rating = models.DecimalField(
        max_digits=3, decimal_places=1,
        default=4.0, verbose_name="Note moyenne"
    )
    is_featured = models.BooleanField(
        default=False, verbose_name="Destination vedette"
    )
    is_active = models.BooleanField(default=True, verbose_name="Active")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Destination"
        verbose_name_plural = "Destinations"
        ordering = ['-is_featured', 'name']

    def __str__(self):
        return self.name

    def get_lowest_price(self):
        """Retourne le prix le plus bas pour un vol vers cette destination."""
        if self.airport:
            from flights.models import Flight
            flight = Flight.objects.filter(
                destination=self.airport,
                departure_time__gt=timezone.now(),
                is_active=True
            ).order_by('base_price_economy').first()
            if flight:
                return flight.get_current_price_economy()
        return None


class DestinationImage(models.Model):
    """Images supplémentaires pour une destination."""

    destination = models.ForeignKey(
        Destination, on_delete=models.CASCADE,
        related_name='images', verbose_name="Destination"
    )
    image = models.ImageField(upload_to='destinations/gallery/', verbose_name="Image")
    alt_text = models.CharField(max_length=200, blank=True, verbose_name="Texte alternatif")
    is_primary = models.BooleanField(default=False, verbose_name="Image principale")

    class Meta:
        verbose_name = "Image de destination"
        verbose_name_plural = "Images de destination"

    def __str__(self):
        return f"Image - {self.destination.name}"


class DestinationReview(models.Model):
    """Avis des voyageurs sur une destination."""

    destination = models.ForeignKey(
        Destination, on_delete=models.CASCADE,
        related_name='reviews', verbose_name="Destination"
    )
    user = models.ForeignKey(
        'auth.User', on_delete=models.CASCADE,
        related_name='destination_reviews', verbose_name="Utilisateur"
    )
    rating = models.PositiveSmallIntegerField(
        verbose_name="Note (1-5)",
        help_text="Note de 1 à 5 étoiles"
    )
    title = models.CharField(max_length=200, verbose_name="Titre de l'avis")
    comment = models.TextField(verbose_name="Commentaire")
    is_approved = models.BooleanField(default=False, verbose_name="Approuvé")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Avis"
        verbose_name_plural = "Avis"
        unique_together = ('destination', 'user')
        ordering = ['-created_at']

    def __str__(self):
        return f"Avis de {self.user.username} sur {self.destination.name}"
