"""
Vues de l'application Destinations.
"""

from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.utils import timezone
from .models import Destination, DestinationReview
from flights.models import Flight, Airport


class DestinationListView(ListView):
    """Liste de toutes les destinations."""

    model = Destination
    template_name = 'destinations/destination_list.html'
    context_object_name = 'destinations'
    paginate_by = 12

    def get_queryset(self):
        return Destination.objects.filter(
            is_active=True
        ).select_related('airport')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['featured_destinations'] = Destination.objects.filter(
            is_active=True, is_featured=True
        )[:6]
        return context


class DestinationDetailView(DetailView):
    """Détail d'une destination."""

    model = Destination
    template_name = 'destinations/destination_detail.html'
    context_object_name = 'destination'
    slug_url_kwarg = 'slug'

    def get_queryset(self):
        return Destination.objects.filter(is_active=True).prefetch_related('images', 'reviews')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        destination = self.get_object()

        # Vols disponibles vers cette destination
        if destination.airport:
            context['available_flights'] = Flight.objects.filter(
                destination=destination.airport,
                departure_time__gt=timezone.now(),
                is_active=True,
                status='scheduled'
            ).select_related('origin', 'aircraft')[:5]

        context['reviews'] = destination.reviews.filter(is_approved=True)
        context['gallery'] = destination.images.all()
        context['lowest_price'] = destination.get_lowest_price()
        return context
