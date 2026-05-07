# tests/system/conftest_system.py
"""
Configuration des tests système NouvelAir.
==========================================

Ce fichier configure l'environnement complet pour les tests système :
  - Serveur Django réel (LiveServer) sur un port aléatoire
  - Navigateurs Playwright (Chromium, Firefox, WebKit)
  - Fixtures de données (utilisateurs, aéroports, vols, réservations)
  - Authentification automatique
  - Capture de screenshots et vidéos en cas d'échec
  - Intégration Allure Reports

Utilisation :
    pytest tests/system/ -m system -v
    pytest tests/system/ -m system --browser firefox -v
    pytest tests/system/ -m system --headed   # Mode visible (débogage)
    pytest tests/system/ -m system --slowmo=500  # Ralentir pour observer
"""
import os
import re
# Allow Django database operations in async contexts (Playwright tests)
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"

import pytest
import allure

from datetime import timedelta
from decimal import Decimal
from pathlib import Path
from typing import Generator

from django.contrib.auth.models import User
from django.test import LiveServerTestCase, override_settings
from playwright.sync_api import (
    sync_playwright, Browser, BrowserContext,
    Page, Playwright, expect,
)


# ─────────────────────────────────────────────────────────────────────────────
# CONSTANTES
# ─────────────────────────────────────────────────────────────────────────────

SCREENSHOTS_DIR = Path("reports/system/screenshots")
VIDEOS_DIR      = Path("reports/system/videos")
TRACES_DIR      = Path("reports/system/traces")

# Créer les dossiers de rapports si absents
for _dir in (SCREENSHOTS_DIR, VIDEOS_DIR, TRACES_DIR):
    _dir.mkdir(parents=True, exist_ok=True)

# Comptes de test (cohérents avec le cahier des charges NouvelAir)
TEST_USER = {
    "username": "testuser",
    "password": "NouvelAir2025!",
    "email":    "testuser@nouvelair.test",
    "first_name": "Ali",
    "last_name":  "Ben Salah",
}

ADMIN_USER = {
    "username": "admin",
    "password": "NouvelAir2025!",
    "email":    "admin@nouvelair.test",
}


# ─────────────────────────────────────────────────────────────────────────────
# FIXTURES PLAYWRIGHT — Scope function (isolées par test)
# ─────────────────────────────────────────────────────────────────────────────

@pytest.fixture
def browser_context_args(browser_context_args):
    """Configurer les paramètres du contexte Playwright."""
    return {
        **browser_context_args,
        "base_url": "http://127.0.0.1:8000",
        "ignore_https_errors": True,
    }


# ─────────────────────────────────────────────────────────────────────────────
# FIXTURES DE DONNÉES — Scope function (recréées à chaque test)
# ─────────────────────────────────────────────────────────────────────────────

@pytest.fixture
def sys_airports(db):
    """
    Crée les 10 aéroports du cahier des charges NouvelAir (section 4.2).
    Disponibles sur context.airports['TUN'], etc.
    """
    from flights.models import Airport

    data = [
        ("TUN", "Tunis-Carthage",        "Tunis",      "TN",  36.851,  10.227),
        ("MIR", "Habib Bourguiba",        "Monastir",   "TN",  35.758,  10.755),
        ("DJE", "Zarzis",                 "Djerba",     "TN",  33.875,  10.775),
        ("SFA", "Sfax-Thyna",             "Sfax",       "TN",  34.718,  10.691),
        ("TOE", "Nefta",                  "Tozeur",     "TN",  33.939,   8.110),
        ("CDG", "Charles de Gaulle",      "Paris",      "FR",  49.013,   2.550),
        ("FCO", "Leonardo da Vinci",      "Rome",       "IT",  41.804,  12.251),
        ("IST", "Istanbul Airport",       "Istanbul",   "TR",  41.275,  28.752),
        ("CMN", "Mohammed V",             "Casablanca", "MA",  33.367,  -7.590),
        ("ALG", "Houari Boumediene",      "Alger",      "DZ",  36.691,   3.215),
    ]
    airports = {}
    for code, name, city, country, lat, lon in data:
        airports[code], _ = Airport.objects.get_or_create(
            code=code,
            defaults=dict(name=name, city=city, country=country,
                          latitude=lat, longitude=lon),
        )
    return airports


@pytest.fixture
def sys_aircraft(db):
    """Crée un appareil de test réaliste."""
    from flights.models import Aircraft

    aircraft, _ = Aircraft.objects.get_or_create(
        registration="TS-INA",
        defaults=dict(
            model_name="Airbus A320",
            total_seats=180,
            economy_seats=156,
            business_seats=24,
            is_active=True,
        ),
    )
    return aircraft


@pytest.fixture
def sys_flights(db, sys_airports, sys_aircraft):
    """
    Crée une flotte complète de vols de test.
    Retourne un dict indexé par numéro de vol.

    Vols créés :
        NU201  TUN → CDG  (250 TND éco / 750 TND biz)
        NU202  TUN → FCO  (210 TND éco / 600 TND biz)
        NU203  TUN → IST  (190 TND éco / 550 TND biz)
        NU204  CDG → TUN  (260 TND éco / 780 TND biz)
        NU205  TUN → CMN  (160 TND éco / 480 TND biz)
    """
    from django.utils import timezone
    from flights.models import Flight

    now = timezone.now()
    flight_specs = [
        ("NU201", "TUN", "CDG",  7, 2, 30, Decimal("250.00"), Decimal("750.00")),
        ("NU202", "TUN", "FCO",  8, 2,  0, Decimal("210.00"), Decimal("600.00")),
        ("NU203", "TUN", "IST",  9, 3, 15, Decimal("190.00"), Decimal("550.00")),
        ("NU204", "CDG", "TUN", 10, 2, 45, Decimal("260.00"), Decimal("780.00")),
        ("NU205", "TUN", "CMN", 12, 1, 30, Decimal("160.00"), Decimal("480.00")),
    ]

    flights = {}
    for fn, orig, dest, days, dur_h, dur_m, eco, biz in flight_specs:
        dep = now + timedelta(days=days, hours=8)
        arr = dep + timedelta(hours=dur_h, minutes=dur_m)
        flights[fn], _ = Flight.objects.get_or_create(
            flight_number=fn,
            defaults=dict(
                origin=sys_airports[orig],
                destination=sys_airports[dest],
                aircraft=sys_aircraft,
                departure_time=dep,
                arrival_time=arr,
                base_price_economy=eco,
                base_price_business=biz,
                available_seats_economy=120,
                available_seats_business=20,
                status="scheduled",
            ),
        )
    return flights


@pytest.fixture
def sys_testuser(db):
    """
    Crée l'utilisateur standard de test avec profil complet.
    Identifiants : testuser / NouvelAir2025!
    """
    from accounts.models import UserProfile

    user, created = User.objects.get_or_create(
        username=TEST_USER["username"],
        defaults=dict(
            email=TEST_USER["email"],
            first_name=TEST_USER["first_name"],
            last_name=TEST_USER["last_name"],
            is_active=True,
        ),
    )
    if created:
        user.set_password(TEST_USER["password"])
        user.save()

    UserProfile.objects.get_or_create(
        user=user,
        defaults=dict(phone="+21620000001"),
    )
    return user


@pytest.fixture
def sys_admin(db):
    """
    Crée le superutilisateur admin.
    Identifiants : admin / NouvelAir2025!
    """
    admin, created = User.objects.get_or_create(
        username=ADMIN_USER["username"],
        defaults=dict(
            email=ADMIN_USER["email"],
            is_staff=True,
            is_superuser=True,
            is_active=True,
        ),
    )
    if created:
        admin.set_password(ADMIN_USER["password"])
        admin.save()
    return admin


@pytest.fixture
def sys_booking(db, sys_testuser, sys_flights):
    """
    Crée une réservation de test en statut 'pending'.
    Liée à sys_testuser sur le vol NU201.
    """
    from bookings.models import Booking

    booking, _ = Booking.objects.get_or_create(
        booking_reference="SYS-TEST-001",
        defaults=dict(
            user=sys_testuser,
            flight=sys_flights["NU201"],
            passenger_first_name=sys_testuser.first_name,
            passenger_last_name=sys_testuser.last_name,
            passenger_email=sys_testuser.email,
            travel_class="economy",
            number_of_passengers=1,
            status="pending",
            total_price=Decimal("250.00"),
        ),
    )
    return booking


@pytest.fixture
def sys_confirmed_booking(db, sys_testuser, sys_flights):
    """Réservation confirmée pour tester l'annulation."""
    from bookings.models import Booking

    booking, _ = Booking.objects.get_or_create(
        booking_reference="SYS-TEST-002",
        defaults=dict(
            user=sys_testuser,
            flight=sys_flights["NU202"],
            passenger_first_name=sys_testuser.first_name,
            passenger_last_name=sys_testuser.last_name,
            passenger_email=sys_testuser.email,
            travel_class="business",
            number_of_passengers=1,
            status="confirmed",
            total_price=Decimal("600.00"),
        ),
    )
    return booking


# ─────────────────────────────────────────────────────────────────────────────
# FIXTURES D'AUTHENTIFICATION
# ─────────────────────────────────────────────────────────────────────────────

@pytest.fixture
def logged_in_page(page: Page, live_server, sys_testuser) -> Page:
    """
    Retourne une page avec testuser déjà connecté.
    Évite de répéter le flux de login dans chaque test.

    Usage :
        def test_booking_list(self, logged_in_page, live_server):
            logged_in_page.goto(live_server.url + "/bookings/")
            expect(logged_in_page.locator("h1")).to_be_visible()
    """
    _login(page, live_server.url, TEST_USER["username"], TEST_USER["password"])
    return page


@pytest.fixture
def admin_page(page: Page, live_server, sys_admin) -> Page:
    """
    Retourne une page avec l'admin Django connecté.
    Utile pour tester l'interface d'administration.
    """
    _login(page, live_server.url, ADMIN_USER["username"], ADMIN_USER["password"])
    return page


def _login(page: Page, base_url: str, username: str, password: str) -> None:
    """
    Effectue le login Django via le formulaire.
    Méthode privée partagée par les fixtures d'authentification.

    Lève une AssertionError si le login échoue
    (mauvais identifiants ou formulaire introuvable).
    """
    # Essayer l'URL French en premier, puis fallback à l'anglaise
    login_paths = ["/accounts/connexion/", "/accounts/login/"]
    page_loaded = False
    
    for path in login_paths:
        try:
            page.goto(base_url + path)
            page.wait_for_load_state("networkidle", timeout=5000)
            page_loaded = True
            break
        except:
            continue
    
    if not page_loaded:
        raise AssertionError(f"Impossible de charger la page de connexion depuis {login_paths}")

    # Remplir username (essayer plusieurs sélecteurs possibles)
    username_field = (
        page.locator('[name="username"]')
        .or_(page.locator('[id="id_username"]'))
        .or_(page.get_by_label("Nom d'utilisateur", exact=False))
    )
    username_field.first.fill(username)

    # Remplir password
    password_field = (
        page.locator('[name="password"]')
        .or_(page.locator('[id="id_password"]'))
        .or_(page.get_by_label("Mot de passe", exact=False))
    )
    password_field.first.fill(password)

    # Soumettre
    page.locator('[type="submit"]').first.click()
    page.wait_for_load_state("networkidle")

    # Vérifier que le login a réussi (on n'est plus sur /accounts/connexion/ ou /accounts/login/)
    current_url = page.url
    for path in login_paths:
        if path in current_url:
            raise AssertionError(
                f"Login échoué pour '{username}' — toujours sur {current_url}\n"
                "Vérifier les identifiants dans TEST_USER / ADMIN_USER."
            )


# ─────────────────────────────────────────────────────────────────────────────
# HELPERS — Utilitaires partagés entre les tests
# ─────────────────────────────────────────────────────────────────────────────

class SystemTestHelpers:
    """
    Classe utilitaire avec des méthodes de haut niveau pour les tests système.
    Peut être utilisée directement ou via la fixture 'helpers'.

    Exemple d'utilisation :
        def test_quelquechose(self, page, live_server, helpers):
            helpers.go_to_home(page, live_server.url)
            helpers.fill_search_form(page, "TUN", "CDG")
    """

    @staticmethod
    def go_to_home(page: Page, base_url: str) -> None:
        """Navigue vers la page d'accueil et attend le chargement."""
        page.goto(base_url + "/")
        page.wait_for_load_state("networkidle")

    @staticmethod
    def fill_search_form(
        page: Page,
        origin: str,
        destination: str,
        passengers: int = 1,
        trip_type: str = "one_way",
    ) -> None:
        """
        Remplit le formulaire de recherche de vols.
        Compatible avec plusieurs variantes de template Bootstrap.
        """
        # Champ Départ
        origin_sel = (
            page.locator('[name="origin"]')
            .or_(page.get_by_placeholder("Départ", exact=False))
            .or_(page.locator('#id_origin'))
        )
        if origin_sel.count() > 0:
            origin_sel.first.fill(origin)

        # Champ Destination
        dest_sel = (
            page.locator('[name="destination"]')
            .or_(page.get_by_placeholder("Destination", exact=False))
            .or_(page.locator('#id_destination'))
        )
        if dest_sel.count() > 0:
            dest_sel.first.fill(destination)

        # Champ Passagers
        pax_sel = (
            page.locator('[name="passengers"]')
            .or_(page.locator('#id_passengers'))
        )
        if pax_sel.count() > 0:
            pax_sel.first.fill(str(passengers))

    @staticmethod
    def submit_search(page: Page) -> None:
        """Clique sur le bouton Rechercher et attend les résultats."""
        page.locator('[type="submit"]').first.click()
        page.wait_for_load_state("networkidle")

    @staticmethod
    def take_screenshot(page: Page, name: str) -> str:
        """
        Capture un screenshot et l'attache au rapport Allure.
        Retourne le chemin du fichier.
        """
        clean_name = re.sub(r"[^\w\-]", "_", name)
        path = str(SCREENSHOTS_DIR / f"{clean_name}.png")
        page.screenshot(path=path, full_page=True)
        allure.attach.file(
            path,
            name=name,
            attachment_type=allure.attachment_type.PNG,
        )
        return path

    @staticmethod
    def assert_no_django_error(page: Page) -> None:
        """
        Vérifie que la page n'affiche pas d'erreur Django (500, Traceback).
        À appeler après chaque navigation importante.
        """
        content = page.content()
        assert "Traceback" not in content, \
            "Erreur Django (Traceback) détectée dans la page"
        assert page.url.split("//")[1].split("/")[0] not in ["500", "error"], \
            "Page d'erreur 500 détectée"

    @staticmethod
    def wait_for_url_contains(page: Page, fragment: str, timeout: int = 5000) -> None:
        """Attend que l'URL contienne un fragment donné."""
        page.wait_for_url(f"**{fragment}**", timeout=timeout)

    @staticmethod
    def get_page_title(page: Page) -> str:
        """Retourne le titre de la page actuelle."""
        return page.title()

    @staticmethod
    def is_logged_in(page: Page) -> bool:
        """
        Détecte si un utilisateur est connecté en cherchant
        des indicateurs courants dans la navbar NouvelAir.
        """
        content = page.content().lower()
        logged_in_indicators = [
            "déconnexion", "logout", "profil", "profile",
            "ma réservation", "mon compte",
        ]
        return any(ind in content for ind in logged_in_indicators)


@pytest.fixture
def helpers() -> SystemTestHelpers:
    """Retourne une instance des helpers de test système."""
    return SystemTestHelpers()


# ─────────────────────────────────────────────────────────────────────────────
# PAGE OBJECT MODEL — Basique pour NouvelAir
# ─────────────────────────────────────────────────────────────────────────────

class HomePage:
    """Page Object Model pour la page d'accueil NouvelAir."""

    def __init__(self, page: Page, base_url: str):
        self.page     = page
        self.base_url = base_url

    def navigate(self) -> "HomePage":
        self.page.goto(self.base_url + "/")
        self.page.wait_for_load_state("networkidle")
        return self

    @property
    def title(self) -> str:
        return self.page.title()

    @property
    def search_form(self):
        return self.page.locator("form").first

    def fill_origin(self, code: str) -> "HomePage":
        f = (self.page.locator('[name="origin"]')
             .or_(self.page.get_by_placeholder("Départ", exact=False)))
        if f.count() > 0:
            f.first.fill(code)
        return self

    def fill_destination(self, code: str) -> "HomePage":
        f = (self.page.locator('[name="destination"]')
             .or_(self.page.get_by_placeholder("Destination", exact=False)))
        if f.count() > 0:
            f.first.fill(code)
        return self

    def submit(self) -> "SearchResultsPage":
        self.page.locator('[type="submit"]').first.click()
        self.page.wait_for_load_state("networkidle")
        return SearchResultsPage(self.page, self.base_url)


class SearchResultsPage:
    """Page Object Model pour la page de résultats de recherche."""

    def __init__(self, page: Page, base_url: str):
        self.page     = page
        self.base_url = base_url

    @property
    def flight_cards(self):
        """Retourne tous les éléments de vol affichés."""
        return self.page.locator(".flight-result, .card, .list-group-item")

    @property
    def flight_count(self) -> int:
        return self.flight_cards.count()

    def has_flight(self, flight_number: str) -> bool:
        return self.page.get_by_text(flight_number).count() > 0

    def click_first_flight(self) -> "FlightDetailPage":
        self.flight_cards.first.click()
        self.page.wait_for_load_state("networkidle")
        return FlightDetailPage(self.page, self.base_url)


class FlightDetailPage:
    """Page Object Model pour la page de détail d'un vol."""

    def __init__(self, page: Page, base_url: str):
        self.page     = page
        self.base_url = base_url

    def navigate(self, pk: int) -> "FlightDetailPage":
        self.page.goto(f"{self.base_url}/flight/{pk}/")
        self.page.wait_for_load_state("networkidle")
        return self

    def click_book(self) -> "BookingPage":
        book_btn = (
            self.page.get_by_role("link", name=re.compile(r"réserv", re.I))
            .or_(self.page.get_by_role("button", name=re.compile(r"réserv", re.I)))
        )
        if book_btn.count() > 0:
            book_btn.first.click()
            self.page.wait_for_load_state("networkidle")
        return BookingPage(self.page, self.base_url)


class LoginPage:
    """Page Object Model pour la page de connexion."""

    def __init__(self, page: Page, base_url: str):
        self.page     = page
        self.base_url = base_url

    def navigate(self) -> "LoginPage":
        self.page.goto(f"{self.base_url}/accounts/login/")
        self.page.wait_for_load_state("networkidle")
        return self

    def login(self, username: str, password: str) -> "HomePage":
        self.page.locator('[name="username"]').fill(username)
        self.page.locator('[name="password"]').fill(password)
        self.page.locator('[type="submit"]').first.click()
        self.page.wait_for_load_state("networkidle")
        return HomePage(self.page, self.base_url)

    @property
    def has_error(self) -> bool:
        content = self.page.content().lower()
        return any(kw in content for kw in
                   ["invalide", "incorrect", "erreur", "error"])


class BookingPage:
    """Page Object Model pour le formulaire de réservation."""

    def __init__(self, page: Page, base_url: str):
        self.page     = page
        self.base_url = base_url

    def fill_passenger_info(
        self,
        first_name: str,
        last_name: str,
        email: str,
    ) -> "BookingPage":
        fields = {
            "passenger_first_name": first_name,
            "passenger_last_name":  last_name,
            "passenger_email":      email,
        }
        for name, value in fields.items():
            sel = self.page.locator(f'[name="{name}"]')
            if sel.count() > 0:
                sel.fill(value)
        return self

    def submit(self) -> Page:
        self.page.locator('[type="submit"]').first.click()
        self.page.wait_for_load_state("networkidle")
        return self.page


# ─── Fixtures pour les Page Objects ──────────────────────────────────────────

@pytest.fixture
def home_page(page: Page, live_server) -> HomePage:
    """Fixture retournant un HomePage prêt à l'emploi."""
    return HomePage(page, live_server.url)


@pytest.fixture
def login_page(page: Page, live_server) -> LoginPage:
    """Fixture retournant un LoginPage prêt à l'emploi."""
    return LoginPage(page, live_server.url)


@pytest.fixture
def flight_detail_page(page: Page, live_server) -> FlightDetailPage:
    """Fixture retournant un FlightDetailPage prêt à l'emploi."""
    return FlightDetailPage(page, live_server.url)


# ─────────────────────────────────────────────────────────────────────────────
# MARQUEURS PYTEST — Décoration automatique des tests système
# ─────────────────────────────────────────────────────────────────────────────

def pytest_collection_modifyitems(items):
    """
    Ajoute automatiquement le marqueur @pytest.mark.system
    à tous les tests dans le dossier tests/system/.
    """
    for item in items:
        if "system" in str(item.fspath):
            item.add_marker(pytest.mark.system)
            item.add_marker(pytest.mark.django_db(transaction=True))