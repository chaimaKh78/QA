"""
Vues de l'application Bookings.
"""

from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import DetailView, ListView, View, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse
from django.db import transaction
from .models import Booking, Passenger, Payment
from .forms import PassengerForm, ContactInfoForm, PaymentForm


class BookingCreateView(View):
    """
    Vue de création de réservation - processus en plusieurs étapes:
    1. Informations des passagers
    2. Coordonnées de contact
    3. Paiement
    4. Confirmation
    """

    def get(self, request):
        if 'search_params' not in request.session and 'booking_flight_id' not in request.session:
            messages.warning(request, "Veuillez d'abord rechercher un vol.")
            return redirect('flights:home')

        flight_id = request.session.get('booking_flight_id')
        if not flight_id:
            messages.warning(request, "Veuillez sélectionner un vol.")
            return redirect('flights:search_results')

        params = request.session.get('search_params', {})
        passengers_count = int(params.get('passengers', 1))
        travel_class = params.get('travel_class', 'economy')

        passenger_forms = [PassengerForm(prefix=str(i)) for i in range(passengers_count)]
        contact_form = ContactInfoForm()

        # Pré-remplir l'email si l'utilisateur est connecté
        if request.user.is_authenticated:
            contact_form = ContactInfoForm(initial={
                'contact_email': request.user.email
            })

        context = {
            'passenger_forms': passenger_forms,
            'contact_form': contact_form,
            'passengers_count': passengers_count,
            'travel_class': travel_class,
        }
        return render(request, 'bookings/booking_form.html', context)

    @transaction.atomic
    def post(self, request):
        params = request.session.get('search_params', {})
        passengers_count = int(params.get('passengers', 1))
        travel_class = params.get('travel_class', 'economy')

        # Étape 1: Validation des formulaires passagers + contact
        passenger_forms = [PassengerForm(request.POST, prefix=str(i)) for i in range(passengers_count)]
        contact_form = ContactInfoForm(request.POST)

        all_passengers_valid = all(f.is_valid() for f in passenger_forms)
        if not all_passengers_valid or not contact_form.is_valid():
            context = {
                'passenger_forms': passenger_forms,
                'contact_form': contact_form,
                'passengers_count': passengers_count,
                'travel_class': travel_class,
            }
            messages.error(request, "Veuillez corriger les erreurs dans les formulaires.")
            return render(request, 'bookings/booking_form.html', context)

        # Étape 2: Récupérer le vol et calculer le prix
        from flights.models import Flight
        flight = get_object_or_404(Flight, pk=request.session.get('booking_flight_id'))

        if travel_class == 'business':
            price_per_passenger = flight.get_current_price_business()
        else:
            price_per_passenger = flight.get_current_price_economy()

        total_amount = price_per_passenger * passengers_count

        # Étape 3: Créer la réservation
        booking = contact_form.save(commit=False)
        booking.user = request.user if request.user.is_authenticated else None
        booking.total_amount = total_amount
        booking.status = 'confirmed'
        booking.save()

        # Créer les passagers
        for i, form in enumerate(passenger_forms):
            passenger = form.save(commit=False)
            passenger.booking = booking
            passenger.flight = flight
            passenger.travel_class = travel_class
            passenger.price = price_per_passenger
            passenger.save()

        # Créer le paiement (simulé)
        Payment.objects.create(
            booking=booking,
            amount=total_amount,
            method='credit_card',
            status='completed',
            transaction_id=f'SIM-{booking.short_reference}'
        )

        # Mettre à jour les sièges disponibles
        if travel_class == 'business':
            flight.available_seats_business = max(0, flight.available_seats_business - passengers_count)
        else:
            flight.available_seats_economy = max(0, flight.available_seats_economy - passengers_count)
        flight.save()

        # Nettoyer la session
        for key in ['booking_flight_id', 'search_params']:
            if key in request.session:
                del request.session[key]

        messages.success(
            request,
            f"Réservation confirmée ! Référence : {booking.short_reference}"
        )
        return redirect('bookings:confirmation', reference=booking.reference)


class BookingConfirmationView(DetailView):
    """Page de confirmation de réservation."""

    model = Booking
    template_name = 'bookings/booking_confirmation.html'
    context_object_name = 'booking'

    def get_object(self):
        return get_object_or_404(Booking, reference=self.kwargs['reference'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['passengers'] = self.object.passengers.select_related('flight').all()
        context['payment'] = self.object.payments.first()
        return context


class BookingLookupView(View):
    """Recherche de réservation par référence et email."""

    def get(self, request):
        return render(request, 'bookings/booking_lookup.html')

    def post(self, request):
        reference = request.POST.get('reference', '').strip().upper()
        email = request.POST.get('email', '').strip()

        if not reference or not email:
            messages.error(request, "Veuillez fournir la référence et l'email.")
            return render(request, 'bookings/booking_lookup.html')

        try:
            booking = Booking.objects.filter(
                reference__startswith=reference,
                contact_email=email
            ).first()

            if booking:
                return redirect('bookings:detail', reference=booking.reference)
            else:
                messages.error(request, "Aucune réservation trouvée avec ces informations.")
        except Exception:
            messages.error(request, "Une erreur est survenue lors de la recherche.")

        return render(request, 'bookings/booking_lookup.html')


class BookingDetailView(DetailView):
    """Détail d'une réservation."""

    model = Booking
    template_name = 'bookings/booking_detail.html'
    context_object_name = 'booking'

    def get_object(self):
        return get_object_or_404(Booking, reference=self.kwargs['reference'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['passengers'] = self.object.passengers.select_related('flight').all()
        context['payment'] = self.object.payments.first()
        return context


class BookingCancelView(View):
    """Annulation d'une réservation."""

    def post(self, request, reference):
        booking = get_object_or_404(Booking, reference=reference)

        if booking.status in ['cancelled', 'completed', 'refunded']:
            messages.error(request, "Cette réservation ne peut plus être annulée.")
            return redirect('bookings:detail', reference=reference)

        booking.status = 'cancelled'
        booking.save()

        # Rembourser les sièges
        passengers = booking.passengers.all()
        for passenger in passengers:
            flight = passenger.flight
            if passenger.travel_class == 'business':
                flight.available_seats_business += 1
            else:
                flight.available_seats_economy += 1
            flight.save()

        # Mettre à jour le paiement
        payment = booking.payments.filter(status='completed').first()
        if payment:
            payment.status = 'refunded'
            payment.save()

        messages.success(request, "Votre réservation a été annulée avec succès.")
        return redirect('bookings:detail', reference=reference)


class MyBookingsView(LoginRequiredMixin, ListView):
    """Liste des réservations de l'utilisateur connecté."""

    model = Booking
    template_name = 'bookings/my_bookings.html'
    context_object_name = 'bookings'

    def get_queryset(self):
        return Booking.objects.filter(
            user=self.request.user
        ).prefetch_related('passengers', 'payments').order_by('-created_at')


def select_flight(request, flight_id):
    """Sélectionne un vol pour la réservation et redirige vers le formulaire."""
    request.session['booking_flight_id'] = flight_id
    return redirect('bookings:create')
