import pytest
from django.utils import timezone
from datetime import datetime



@pytest.mark.django_db
@pytest.mark.unit
class TestFlightDurationDisplay:

    @pytest.fixture(autouse=True)
    def setup(self, sample_flight):
        self.flight = sample_flight


    def test_get_duration_display_returns_hours_and_minutes(self):

        self.flight.departure_time = timezone.make_aware(datetime(2026, 6, 1, 10, 0))
        self.flight.arrival_time = timezone.make_aware(datetime(2026, 6, 1, 12, 30))
        self.flight.save()

        assert self.flight.get_duration_display() == "2h 30min"


    def test_get_duration_display_exact_hours(self):

        self.flight.departure_time = timezone.make_aware(datetime(2026, 6, 1, 10, 0))
        self.flight.arrival_time = timezone.make_aware(datetime(2026, 6, 1, 13, 0))
        self.flight.save()

        assert self.flight.get_duration_display() == "3h"


    def test_get_duration_display_short_flight(self):

        self.flight.departure_time = timezone.make_aware(datetime(2026, 6, 1, 10, 0))
        self.flight.arrival_time = timezone.make_aware(datetime(2026, 6, 1, 10, 45))
        self.flight.save()

        assert self.flight.get_duration_display() == "45min"


    def test_get_duration_display_long_haul_flight(self):

        self.flight.departure_time = timezone.make_aware(datetime(2026, 6, 1, 8, 0))
        self.flight.arrival_time = timezone.make_aware(datetime(2026, 6, 1, 18, 15))
        self.flight.save()

        assert self.flight.get_duration_display() == "10h 15min"






class TestFlightDynamicPricing:

    def test_get_current_price_economy_high_availability(self, sample_flight):

        sample_flight.base_price_economy = 350
        sample_flight.available_seats_economy = 80
        sample_flight.total_seats_economy = 100

        assert sample_flight.get_current_price_economy() == 350


    def test_get_current_price_economy_medium_availability(self, sample_flight):

        sample_flight.base_price_economy = 350
        sample_flight.available_seats_economy = 40
        sample_flight.total_seats_economy = 100

        assert sample_flight.get_current_price_economy() == 350


    def test_get_current_price_economy_low_availability(self, sample_flight):

        sample_flight.base_price_economy = 350
        sample_flight.available_seats_economy = 10
        sample_flight.total_seats_economy = 100

        assert sample_flight.get_current_price_economy() == 350


    def test_get_current_price_economy_zero_seats(self, sample_flight):

        sample_flight.base_price_economy = 350
        sample_flight.available_seats_economy = 0
        sample_flight.total_seats_economy = 100

        assert sample_flight.get_current_price_economy() == 350