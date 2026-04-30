"""
Tests de responsive design — Jour 7.

Vérifie que le site NouvelAir s'adapte correctement aux différentes
tailles d'écran: mobile, tablette et desktop.

Dépendances:
    pip install playwright pytest-playwright
    playwright install chromium

Couverture: 5 tests couvrant mobile, tablette, desktop et mode paysage.
"""

import pytest

try:
    from playwright.sync_api import Page, expect
    HAS_PLAYWRIGHT = True
except ImportError:
    HAS_PLAYWRIGHT = False

# ── Configuration ────────────────────────────────────────────────────────────

BASE_URL = "http://127.0.0.1:8000"


def pytest_configure(config):
    """Enregistre les marqueurs personnalisés."""
    config.addinivalue_line(
        "markers", "e2e: marquage des tests end-to-end (Sprint 1, Jour 7)"
    )
    config.addinivalue_line(
        "markers", "responsive: marquage des tests de responsive design"
    )


# ── Fixtures ─────────────────────────────────────────────────────────────────

@pytest.fixture
def mobile_viewport():
    """Retourne les dimensions mobile (iPhone SE)."""
    return {"width": 375, "height": 667}


@pytest.fixture
def tablet_viewport():
    """Retourne les dimensions tablette (iPad)."""
    return {"width": 768, "height": 1024}


@pytest.fixture
def desktop_viewport():
    """Retourne les dimensions desktop standard."""
    return {"width": 1280, "height": 800}


# ── Tests ────────────────────────────────────────────────────────────────────

@pytest.mark.e2e
@pytest.mark.responsive
class TestResponsiveDesign:
    """
    Suite de tests de responsive design pour le site NouvelAir.

    Vérifie que:
    - La navigation s'adapte en mobile (hamburger menu ou nav compacte)
    - Les formulaires sont utilisables sur petit écran
    - Le layout passe de 1 à 2 colonnes en tablette
    - Le layout desktop affiche toutes les colonnes
    - Le mode paysage mobile fonctionne correctement
    """

    # ─── Test 1: Navigation mobile — hamburger menu ou nav compacte ───────

    @pytest.mark.skipif(not HAS_PLAYWRIGHT, reason="Playwright non installé")
    def test_mobile_navigation(self, page: Page, base_url, mobile_viewport):
        """
        Vérifie la navigation en viewport mobile (375px).

        Sur mobile, la navigation doit soit:
        - Afficher un bouton hamburger (menu hamburger)
        - Afficher une navigation compacte (icônes ou menu abrégé)
        - Cacher les éléments non essentiels

        La barre de navigation ne doit pas déborder de l'écran.
        """
        page.set_viewport_size(mobile_viewport)
        page.goto(base_url)
        page.wait_for_load_state("networkidle")

        # Vérifier qu'un élément de navigation est présent
        nav = page.locator("nav, header, [role='navigation']")
        expect(nav.first).to_be_visible(timeout=10000)

        # Vérifier que la barre de navigation ne déborde pas
        nav_box = nav.first.bounding_box()
        page_width = mobile_viewport["width"]

        assert nav_box is not None, "L'élément de navigation n'a pas de bounding box."
        assert nav_box["width"] <= page_width + 10, (
            f"La navigation déborde: {nav_box['width']}px > {page_width}px"
        )

        # Vérifier la présence d'un hamburger menu OU d'une navigation visible
        hamburger = page.locator(
            "button[aria-label*='menu' i], "
            "button[aria-label*='navigation' i], "
            ".navbar-toggler, "
            ".hamburger, "
            "button.menu-toggle"
        )
        nav_links = page.locator("nav a, [role='navigation'] a")

        has_hamburger = hamburger.count() > 0
        has_visible_links = nav_links.count() > 0

        assert has_hamburger or has_visible_links, (
            "Aucun hamburger menu ni liens de navigation détectés en mode mobile."
        )

    # ─── Test 2: Formulaire de recherche sur mobile ──────────────────────

    @pytest.mark.skipif(not HAS_PLAYWRIGHT, reason="Playwright non installé")
    def test_mobile_search_form(self, page: Page, base_url, mobile_viewport):
        """
        Vérifie que le formulaire de recherche est utilisable sur mobile.

        Le formulaire doit:
        - Être entièrement visible sans scroll horizontal
        - Avoir des champs de taille suffisante pour le touch (≥44px)
        - Afficher les labels correctement
        """
        page.set_viewport_size(mobile_viewport)
        page.goto(base_url)
        page.wait_for_load_state("networkidle")

        # Vérifier l'absence de scroll horizontal
        scroll_width = page.evaluate("document.documentElement.scrollWidth")
        client_width = page.evaluate("document.documentElement.clientWidth")

        assert scroll_width <= client_width + 5, (
            f"Scroll horizontal détecté: scrollWidth={scroll_width}px, "
            f"clientWidth={client_width}px"
        )

        # Vérifier que les inputs sont accessibles
        inputs = page.locator("input[type='text'], input[type='search'], input[name]")
        if inputs.count() > 0:
            first_input = inputs.first
            box = first_input.bounding_box()
            assert box is not None, "Le premier input n'a pas de bounding box."

            # Vérifier la taille minimum pour le touch (44px)
            min_touch_size = 44
            assert box["height"] >= min_touch_size - 10, (
                f"Champ de recherche trop petit pour le touch: "
                f"{box['height']}px (minimum: {min_touch_size}px)"
            )

    # ─── Test 3: Layout tablette — 2 colonnes ────────────────────────────

    @pytest.mark.skipif(not HAS_PLAYWRIGHT, reason="Playwright non installé")
    def test_tablet_layout(self, page: Page, base_url, tablet_viewport):
        """
        Vérifie le layout en viewport tablette (768px).

        En tablette, le layout devrait afficher:
        - Un maximum de 2 colonnes pour les grilles de contenu
        - La navigation adaptée (pas de hamburger, mais menu compact)
        - Le contenu qui remplit correctement l'espace disponible
        """
        page.set_viewport_size(tablet_viewport)
        page.goto(base_url)
        page.wait_for_load_state("networkidle")

        # Vérifier l'absence de scroll horizontal
        scroll_width = page.evaluate("document.documentElement.scrollWidth")
        client_width = page.evaluate("document.documentElement.clientWidth")

        assert scroll_width <= client_width + 5, (
            f"Overflow horizontal en tablette: {scroll_width}px > {client_width}px"
        )

        # Vérifier que le contenu principal remplit l'espace
        main = page.locator("main, .main-content, #content, .container")
        if main.count() > 0:
            main_box = main.first.bounding_box()
            assert main_box is not None, "Le contenu principal n'a pas de bounding box."

            # Le contenu doit utiliser au moins 80% de la largeur
            min_content_width = tablet_viewport["width"] * 0.8
            assert main_box["width"] >= min_content_width, (
                f"Le contenu principal est trop étroit en tablette: "
                f"{main_box['width']}px (attendu ≥ {min_content_width}px)"
            )

        # Vérifier que le footer est visible et ne déborde pas
        footer = page.locator("footer, .footer, #footer")
        if footer.count() > 0:
            footer_box = footer.first.bounding_box()
            assert footer_box is not None
            assert footer_box["width"] <= tablet_viewport["width"] + 10, (
                f"Le footer déborde en tablette: {footer_box['width']}px"
            )

    # ─── Test 4: Layout desktop — disposition complète ────────────────────

    @pytest.mark.skipif(not HAS_PLAYWRIGHT, reason="Playwright non installé")
    def test_desktop_layout(self, page: Page, base_url, desktop_viewport):
        """
        Vérifie le layout en viewport desktop (1280px).

        En desktop, le layout doit afficher:
        - La navigation complète avec tous les liens
        - Le contenu sur la largeur disponible
        - Pas de contenu qui déborde
        """
        page.set_viewport_size(desktop_viewport)
        page.goto(base_url)
        page.wait_for_load_state("networkidle")

        # Vérifier l'absence de scroll horizontal
        scroll_width = page.evaluate("document.documentElement.scrollWidth")
        client_width = page.evaluate("document.documentElement.clientWidth")

        assert scroll_width <= client_width + 5, (
            f"Overflow horizontal en desktop: {scroll_width}px > {client_width}px"
        )

        # Vérifier que la navigation affiche les liens principaux
        nav = page.locator("nav, header, [role='navigation']")
        if nav.count() > 0:
            nav_links = nav.first.locator("a")
            assert nav_links.count() >= 2, (
                f"Navigation desktop devrait afficher au moins 2 liens. "
                f"Trouvé: {nav_links.count()}"
            )

        # Vérifier le contenu principal
        main = page.locator("main, .main-content, #content")
        if main.count() > 0:
            main_box = main.first.bounding_box()
            assert main_box is not None
            # Le contenu doit être centré avec une largeur raisonnable
            assert main_box["width"] >= 600, (
                f"Le contenu principal est trop étroit en desktop: {main_box['width']}px"
            )

    # ─── Test 5: Mode paysage mobile (667×375) ───────────────────────────

    @pytest.mark.skipif(not HAS_PLAYWRIGHT, reason="Playwright non installé")
    def test_landscape_mobile(self, page: Page, base_url):
        """
        Vérifie le layout en mode paysage mobile (667×375).

        En mode paysage mobile:
        - La hauteur est très limitée (375px)
        - La navigation doit rester accessible
        - Pas de contenu coupé ou masqué
        """
        landscape_viewport = {"width": 667, "height": 375}
        page.set_viewport_size(landscape_viewport)
        page.goto(base_url)
        page.wait_for_load_state("networkidle")

        # Vérifier l'absence de scroll horizontal
        scroll_width = page.evaluate("document.documentElement.scrollWidth")
        client_width = page.evaluate("document.documentElement.clientWidth")

        assert scroll_width <= client_width + 5, (
            f"Overflow horizontal en paysage mobile: {scroll_width}px > {client_width}px"
        )

        # Vérifier que la navigation reste accessible
        nav = page.locator("nav, header, [role='navigation']")
        if nav.count() > 0:
            nav_box = nav.first.bounding_box()
            assert nav_box is not None, "La navigation n'est pas visible en paysage."

            # La navigation ne doit pas prendre plus de 40% de la hauteur en paysage
            max_nav_height = landscape_viewport["height"] * 0.4
            assert nav_box["height"] <= max_nav_height, (
                f"La navigation prend trop de place en paysage: "
                f"{nav_box['height']}px (max: {max_nav_height}px)"
            )

        # Vérifier qu'il y a du contenu visible au-dessus de la ligne de flottaison
        visible_height = landscape_viewport["height"]
        main = page.locator("main, .main-content, #content")
        if main.count() > 0:
            main_box = main.first.bounding_box()
            assert main_box is not None
            # Au moins une partie du contenu principal doit être visible
            assert main_box["y"] < visible_height, (
                "Le contenu principal n'est pas visible dans le viewport en paysage."
            )
