"""
Formulaires Booking - Formulaires de réservation et passagers.
"""

from django import forms
from django.core.exceptions import ValidationError
from .models import Booking, Passenger, Payment


class PassengerForm(forms.ModelForm):
    """Formulaire pour ajouter les informations d'un passager."""

    class Meta:
        model = Passenger
        fields = [
            'title', 'first_name', 'last_name', 'date_of_birth',
            'nationality', 'passport_number', 'passport_expiry',
            'special_assistance', 'meal_preference',
        ]
        widgets = {
            'title': forms.Select(attrs={'class': 'form-select'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'date_of_birth': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'nationality': forms.TextInput(attrs={'class': 'form-control'}),
            'passport_number': forms.TextInput(attrs={'class': 'form-control'}),
            'passport_expiry': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'special_assistance': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'meal_preference': forms.Select(attrs={'class': 'form-select'}),
        }

    def clean_passport_number(self):
        passport = self.cleaned_data.get('passport_number', '')
        if passport and len(passport) < 5:
            raise ValidationError("Le numéro de passeport doit contenir au moins 5 caractères.")
        return passport


class ContactInfoForm(forms.ModelForm):
    """Formulaire pour les informations de contact de la réservation."""

    class Meta:
        model = Booking
        fields = ['contact_email', 'contact_phone', 'special_requests']
        widgets = {
            'contact_email': forms.EmailInput(attrs={'class': 'form-control'}),
            'contact_phone': forms.TextInput(attrs={'class': 'form-control'}),
            'special_requests': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class PaymentForm(forms.ModelForm):
    """Formulaire pour le paiement de la réservation."""

    card_number = forms.CharField(
        max_length=19,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'XXXX XXXX XXXX XXXX',
            'pattern': '[0-9 ]{13,19}',
        }),
        label="Numéro de carte"
    )
    card_holder = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label="Titulaire de la carte"
    )
    expiry_date = forms.CharField(
        max_length=5,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'MM/AA',
            'pattern': '(0[1-9]|1[0-2])/[0-9]{2}',
        }),
        label="Date d'expiration"
    )
    cvv = forms.CharField(
        max_length=4,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'CVV',
            'pattern': '[0-9]{3,4}',
        }),
        label="CVV"
    )

    class Meta:
        model = Payment
        fields = ['method']
        widgets = {
            'method': forms.Select(attrs={'class': 'form-select'}),
        }

    def clean_card_number(self):
        card_number = self.cleaned_data.get('card_number', '').replace(' ', '')
        if not card_number.isdigit() or len(card_number) < 13:
            raise ValidationError("Numéro de carte invalide.")
        return card_number
