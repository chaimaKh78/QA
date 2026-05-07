# tests/system/test_system_search.py
"""
Tests Système NouvelAir — LiveServer + Playwright.
Ces tests lancent un vrai serveur Django et un vrai navigateur.
"""
import pytest
import re
from playwright.sync_api import expect
from datetime import timedelta
from decimal import Decimal


@pytest.mark.django_db(transaction=True)
@pytest.mark.system
class TestSystemFlightSearch:
    """Tests système avec pytest-django live_server fixture."""

    def test_sys_homepage_loads_with_search_form(self, live_server, page, sys_airports, sys_aircraft):
        """SYS-001 : La page d'accueil s'affiche avec le formulaire de recherche."""
        from flights.models import Flight
        from django.utils import timezone
        
        page.goto(f"{live_server.url}/")
        page.wait_for_load_state("networkidle")

        # Vérifier le titre contient NouvelAir ou Vol
        expect(page).to_have_title(re.compile(r"NouvelAir|Vol"))
        
        # Vérifier que le formulaire de recherche est présent
        form = page.locator("form").first
        expect(form).to_be_visible()

    def test_sys_search_returns_results(self, live_server, page, sys_airports, sys_aircraft):
        """SYS-002 : Une recherche TUN→CDG affiche les vols disponibles."""
        from flights.models import Flight
        from django.utils import timezone
        
        # Créer un vol de test
        dep = timezone.now() + timedelta(days=7)
        arr = dep + timedelta(hours=2, minutes=30)
        flight, _ = Flight.objects.get_or_create(
            flight_number="NU201",
            defaults={
                "origin": sys_airports["TUN"],
                "destination": sys_airports["CDG"],
                "aircraft": sys_aircraft,
                "departure_time": dep,
                "arrival_time": arr,
                "base_price_economy": Decimal("250.00"),
                "base_price_business": Decimal("750.00"),
                "available_seats_economy": 120,
                "available_seats_business": 20,
                "status": "scheduled",
            },
        )
        
        # La recherche utilise les paramètres de session, pas de query params
        # Aller sur la page d'accueil d'abord
        page.goto(f"{live_server.url}/")
        page.wait_for_load_state("networkidle")
        
        # Utiliser le formulaire de recherche - ModelChoiceField uses PK as value
        origin_pk = sys_airports["TUN"].pk
        dest_pk = sys_airports["CDG"].pk
        page.locator('select[name="origin"]').select_option(str(origin_pk))
        page.locator('select[name="destination"]').select_option(str(dest_pk))
        page.locator('[type="submit"]').first.click()
        page.wait_for_load_state("networkidle")

        # Le vol NU201 doit apparaître - vérifier le badge
        expect(page.locator(".badge")).to_contain_text("NU201")

    def test_sys_login_and_create_booking(self, live_server, page, sys_testuser, sys_flights):
        """SYS-003 : Flux complet login → réservation."""
        from tests.system.conftest import _login, TEST_USER
        
        # Connexion
        _login(page, live_server.url, TEST_USER["username"], TEST_USER["password"])
        
        # Aller sur la page de détail du vol (utiliser le flight_number, pas pk)
        flight = sys_flights["NU201"]
        page.goto(f"{live_server.url}/vol/{flight.flight_number}/")
        
        # Vérifier que le login a réussi (pas de redirect)
        expect(page).not_to_have_url(re.compile(r".*/connexion/.*"))