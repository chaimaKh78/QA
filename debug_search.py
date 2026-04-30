import os, sys, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nouvelair.settings')
django.setup()

from datetime import timedelta
from django.utils import timezone
from tests.factories import AirportFactory, AircraftFactory, FlightFactory
from flights.models import Flight

AirportFactory(code="TUN")
AirportFactory(code="CDG")
aircraft = AircraftFactory()

departure_date = (timezone.now() + timedelta(days=3)).date()
print(f"departure_date: {departure_date}")

flight = FlightFactory(
    flight_number="BJ501",
    origin=AirportFactory(code="TUN"),
    destination=AirportFactory(code="CDG"),
    aircraft=aircraft,
    departure_time=timezone.now() + timedelta(days=3, hours=8),
    arrival_time=timezone.now() + timedelta(days=3, hours=11),
    status="scheduled",
    available_seats_economy=50,
    is_active=True,
)

print(f"Flight created: {flight}")
print(f"Flight origin code: {flight.origin.code}")
print(f"Flight dest code: {flight.destination.code}")
print(f"Flight departure_time: {flight.departure_time}")
print(f"Flight departure_time date: {flight.departure_time.date()}")
print(f"Flight status: {flight.status}")
print(f"Flight is_active: {flight.is_active}")
print(f"Flight seats eco: {flight.available_seats_economy}")

results = Flight.search_flights("TUN", "CDG", departure_date, passengers=1)
print(f"Search results count: {results.count()}")
if results.exists():
    f = results.first()
    print(f"First result: {f}")
else:
    # Debug each filter
    print(f"All flights: {Flight.objects.count()}")
    print(f"Filter origin TUN: {Flight.objects.filter(origin__code='TUN').count()}")
    print(f"Filter dest CDG: {Flight.objects.filter(destination__code='CDG').count()}")
    print(f"Filter date: {Flight.objects.filter(departure_time__date=departure_date).count()}")
    print(f"Filter active: {Flight.objects.filter(is_active=True).count()}")
    print(f"Filter scheduled: {Flight.objects.filter(status='scheduled').count()}")
