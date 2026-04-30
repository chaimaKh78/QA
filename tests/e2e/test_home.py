"""
Tests E2E – Page d'accueil (Jour 6).

Teste les fonctionnalités principales de la page d'accueil de NouvelAir :
- Chargement et titre
- Formulaire de recherche
- Liens de navigation
- Destinations populaires
- Vols à venir

Tests: 5
"""

import pytest
from playwright.sync_api import Page
from pages.home_page import HomePage


# ── Tests ─────────────────────────────────────────────────────────────────────

@pytest.mark.e2e
class TestHomePage:
    """Suite de tests E2E pour la page d'accueil de NouvelAir."""

    def test_homepage_loads(self, page: Page, base_url: str):
        """
        Vérifie que la page d'accueil se charge correctement.

        Actions:
            1. Naviguer vers /
            2. Vérifier que le titre contient "NouvelAir"
            3. Vérifier que la réponse HTTP est 200

        Assertions:
            - Le statut HTTP est 200
            - Le titre de la page contient "NouvelAir"
        """
        home = HomePage(page, base_url)
        home.navigate(home.url)

        response = page.goto(f"{base_url}{home.url}", wait_until="domcontentloaded")
        assert response is not None, "La réponse est None, la page n'a pas chargé"
        assert response.status == 200, f"Status attendu 200, obtenu {response.status}"

        title = home.get_title()
        assert "NouvelAir" in title or "nouvelair" in title.lower(), (
            f"Le titre ne contient pas 'NouvelAir'. Titre obtenu: '{title}'"
        )

    def test_homepage_search_form_present(self, page: Page, base_url: str):
        """
        Vérifie que le formulaire de recherche de vols est présent.

        Actions:
            1. Naviguer vers /
            2. Vérifier la présence des champs du formulaire

        Assertions:
            - Le formulaire de recherche existe
            - Les champs origin, destination, date et passengers sont présents
        """
        home = HomePage(page, base_url)
        home.navigate(home.url)

        assert home.has_search_form(), (
            "Le formulaire de recherche de vols n'est pas présent sur la page d'accueil"
        )

        # Vérifier la présence des champs principaux du formulaire
        origin_select = page.locator("select[name='origin'], select#id_origin, #origin")
        destination_select = page.locator("select[name='destination'], select#id_destination, #destination")
        date_input = page.locator("input[name='departure_date'], input[type='date']")
        passengers_input = page.locator("input[name='passengers'], select[name='passengers']")

        assert origin_select.count() > 0, "Le champ 'origine' (origin) est manquant"
        assert destination_select.count() > 0, "Le champ 'destination' est manquant"
        assert date_input.count() > 0, "Le champ 'date de départ' est manquant"
        assert passengers_input.count() > 0, "Le champ 'passagers' est manquant"

    def test_navigation_links(self, page: Page, base_url: str):
        """
        Vérifie que les liens principaux de navigation sont présents.

        Actions:
            1. Naviguer vers /
            2. Vérifier la présence des liens de navigation

        Assertions:
            - Les liens Recherche, Destinations, Promotions, Compte existent
        """
        home = HomePage(page, base_url)
        home.navigate(home.url)

        # Vérifier la présence des liens de navigation principaux
        nav_links = [
            ("Recherche", "a:has-text('Recherche'), a:has-text('Vols'), a[href*='search'], a[href*='recherche']"),
            ("Destinations", "a:has-text('Destinations'), a[href*='destinations']"),
            ("Promotions", "a:has-text('Promotions'), a[href*='promotions']"),
            ("Compte", "a:has-text('Compte'), a:has-text('Mon Compte'), a:has-text('Profil'), a[href*='accounts']"),
        ]

        for link_name, selector in nav_links:
            locator = page.locator(selector)
            assert locator.count() > 0, (
                f"Le lien de navigation '{link_name}' est manquant"
            )

    def test_popular_destinations_displayed(self, page: Page, base_url: str):
        """
        Vérifie que la section des destinations populaires est visible.

        Actions:
            1. Naviguer vers /
            2. Vérifier la section destinations populaires

        Assertions:
            - La section destinations populaires existe sur la page
            - Au moins une carte de destination est affichée
        """
        home = HomePage(page, base_url)
        home.navigate(home.url)

        # Vérifier la section destinations populaires
        section = page.locator(
            "section:has-text('Populaire'), section:has-text('Destination'), "
            ".popular-destinations, .destinations-section, "
            "[class*='popular'], [class*='destinations']"
        )
        assert section.count() > 0, (
            "La section 'Destinations populaires' n'est pas présente sur la page"
        )

        destinations = home.get_popular_destinations()
        assert len(destinations) > 0, (
            "Aucune carte de destination populaire n'est affichée"
        )

    def test_upcoming_flights_displayed(self, page: Page, base_url: str):
        """
        Vérifie que la section des vols à venir est visible.

        Actions:
            1. Naviguer vers /
            2. Vérifier la section vols à venir

        Assertions:
            - La section vols à venir existe sur la page
            - Au moins une carte de vol est affichée
        """
        home = HomePage(page, base_url)
        home.navigate(home.url)

        # Vérifier la section vols à venir
        section = page.locator(
            "section:has-text('Prochain'), section:has-text('Vol'), "
            ".upcoming-flights, .flights-section, "
            "[class*='upcoming'], [class*='flights']"
        )
        assert section.count() > 0, (
            "La section 'Vols à venir' n'est pas présente sur la page"
        )

        flights = home.get_upcoming_flights()
        assert len(flights) > 0, (
            "Aucune carte de vol à venir n'est affichée"
        )
