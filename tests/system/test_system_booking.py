# tests/system/test_system_booking.py
import re
import pytest
from playwright.sync_api import Page, expect
import time


@pytest.mark.django_db(transaction=True)
@pytest.mark.system
class TestSystemBookingFlow:
    """
    Tests système avec pytest-django live_server fixture.
    Requis : pip install pytest-playwright
    Configurer dans pytest.ini :
        [pytest]
        addopts = --base-url=http://127.0.0.1:8000
    """

    def test_sys_complete_booking_flow(self, live_server, page: Page,
                                         sys_flights, sys_testuser, logged_in_page):
        """
        SYS-010 : Flux de réservation de bout en bout.
        Given  : un vol TUN→CDG disponible + un utilisateur connecté
        When   : l'utilisateur navigue vers le vol
        Then   : les détails du vol sont affichés
        """
        flight = sys_flights["NU201"]
        page = logged_in_page
        page.goto(f"{live_server.url}/vol/{flight.flight_number}/")
        expect(page).not_to_have_url(re.compile(r".*/connexion/.*"))
        # Use a more specific selector to avoid strict mode violation
        expect(page.locator("h4:has-text('NU201')")).to_be_visible()

    def test_sys_404_for_nonexistent_flight(self, live_server, page: Page):
        """SYS-011 : Un vol inexistant retourne une page 404 correcte."""
        response = page.goto(f"{live_server.url}/vol/99999/")
        assert response.status == 404

    def test_sys_anonymous_redirect_to_login(self, live_server, page: Page):
        """SYS-012 : Un visiteur non connecté est redirigé vers login."""
        page.goto(f"{live_server.url}/bookings/mes-reservations/")
        expect(page).to_have_url(re.compile(r".*/accounts/connexion/.*"))

    def test_sys_search_response_time(self, live_server, page: Page,
                                       sys_flights):
        """SYS-013 : La page de résultats répond en moins de 3 secondes."""
        start = time.time()
        page.goto(f"{live_server.url}/search/?origin=TUN&destination=CDG")
        page.wait_for_load_state("networkidle")
        elapsed = time.time() - start

        assert elapsed < 3.0, f"Réponse trop lente : {elapsed:.2f}s > 3s"