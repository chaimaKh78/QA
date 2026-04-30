"""
Configuration des URLs pour l'application Bookings.
"""

from django.urls import path
from . import views

app_name = 'bookings'

urlpatterns = [
    path('creer/', views.BookingCreateView.as_view(), name='create'),
    path('confirmation/<uuid:reference>/', views.BookingConfirmationView.as_view(), name='confirmation'),
    path('recherche/', views.BookingLookupView.as_view(), name='lookup'),
    path('detail/<uuid:reference>/', views.BookingDetailView.as_view(), name='detail'),
    path('annuler/<uuid:reference>/', views.BookingCancelView.as_view(), name='cancel'),
    path('mes-reservations/', views.MyBookingsView.as_view(), name='my_bookings'),
    path('selectionner-vol/<int:flight_id>/', views.select_flight, name='select_flight'),
]
