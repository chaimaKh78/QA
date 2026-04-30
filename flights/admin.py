"""
Administration de l'application Flights.
"""

from django.contrib import admin
from .models import Airport, Aircraft, Flight


@admin.register(Airport)
class AirportAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'city', 'country', 'is_active', 'created_at')
    list_filter = ('country', 'is_active')
    search_fields = ('code', 'name', 'city')
    ordering = ('code',)
    list_editable = ('is_active',)


@admin.register(Aircraft)
class AircraftAdmin(admin.ModelAdmin):
    list_display = ('model_name', 'registration', 'total_seats', 'economy_seats', 'business_seats', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('model_name', 'registration')
    list_editable = ('is_active',)


@admin.register(Flight)
class FlightAdmin(admin.ModelAdmin):
    list_display = (
        'flight_number', 'origin', 'destination', 'departure_time',
        'arrival_time', 'status', 'base_price_economy',
        'available_seats_economy', 'available_seats_business', 'is_active'
    )
    list_filter = ('status', 'is_active', 'origin', 'destination', 'departure_time')
    search_fields = ('flight_number', 'origin__code', 'destination__code')
    ordering = ('-departure_time',)
    list_editable = ('status', 'is_active')
    date_hierarchy = 'departure_time'

    fieldsets = (
        ('Informations du vol', {
            'fields': ('flight_number', 'origin', 'destination', 'aircraft', 'status')
        }),
        ('Horaires', {
            'fields': ('departure_time', 'arrival_time')
        }),
        ('Tarification', {
            'fields': ('base_price_economy', 'base_price_business',
                       'available_seats_economy', 'available_seats_business')
        }),
        ('Métadonnées', {
            'fields': ('is_active',),
            'classes': ('collapse',)
        }),
    )
