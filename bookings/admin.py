"""
Administration de l'application Bookings.
"""

from django.contrib import admin
from .models import Booking, Passenger, Payment


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = (
        'short_reference', 'user', 'contact_email', 'status',
        'total_amount', 'created_at'
    )
    list_filter = ('status', 'created_at')
    search_fields = ('reference', 'contact_email', 'contact_phone')
    ordering = ('-created_at',)
    readonly_fields = ('reference',)

    fieldsets = (
        ('Réservation', {
            'fields': ('reference', 'user', 'status', 'total_amount')
        }),
        ('Contact', {
            'fields': ('contact_email', 'contact_phone', 'special_requests')
        }),
    )


class PassengerInline(admin.TabularInline):
    model = Passenger
    extra = 0
    readonly_fields = ('booking', 'flight', 'price')
    fields = ('booking', 'flight', 'title', 'first_name', 'last_name',
              'travel_class', 'seat_number', 'price')


@admin.register(Passenger)
class PassengerAdmin(admin.ModelAdmin):
    list_display = (
        'last_name', 'first_name', 'booking', 'flight',
        'travel_class', 'seat_number', 'price'
    )
    list_filter = ('travel_class',)
    search_fields = ('last_name', 'first_name', 'passport_number')


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('booking', 'amount', 'method', 'status', 'transaction_id', 'created_at')
    list_filter = ('method', 'status')
    search_fields = ('transaction_id', 'booking__reference')
