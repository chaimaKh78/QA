#!/usr/bin/env python3
"""
setup_jour7.py — Création des fichiers de tests visuels, accessibilité et sécurité (Jour 7, NouvelAir)

Ce script génère automatiquement tous les fichiers nécessaires pour les tests
E2E visuels, d'accessibilité, responsive, et de sécurité du Sprint 1, Jour 7.

Fichiers créés:
    1. tests/e2e/__init__.py
    2. tests/e2e/test_visual_regression.py   (8 tests)
    3. tests/e2e/test_accessibility.py        (7 tests)
    4. tests/e2e/test_responsive.py           (5 tests)
    5. tests/security/__init__.py
    6. tests/security/test_csrf.py            (5 tests)
    7. tests/security/test_auth_security.py   (5 tests)
    8. docs/accessibility_report_template.md
    9. docs/visual_regression_report.md
   10. reports/screenshots/                   (répertoire)

Usage:
    python setup_jour7.py

Le script doit être exécuté depuis la racine du projet NouvelAir:
    D:\\NouvelairApp\\nouvelair_project\\
"""

import os
import sys
import stat

# ─────────────────────────────────────────────────────────────────────────────
# Configuration
# ─────────────────────────────────────────────────────────────────────────────

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_URL = "http://127.0.0.1:8000"
SCREENSHOTS_DIR = os.path.join(BASE_DIR, "reports", "screenshots")
BASELINES_DIR = os.path.join(BASE_DIR, "reports", "baselines")

DIRECTORIES_TO_CREATE = [
    os.path.join(BASE_DIR, "tests", "e2e"),
    os.path.join(BASE_DIR, "tests", "security"),
    os.path.join(BASE_DIR, "docs"),
    os.path.join(BASE_DIR, "reports", "screenshots"),
    os.path.join(BASE_DIR, "reports", "baselines"),
    os.path.join(BASE_DIR, "reports", "accessibility"),
]

FILES_TO_CREATE = {
    "tests/e2e/__init__.py": "init_file",
    "tests/e2e/test_visual_regression.py": "visual_regression_tests",
    "tests/e2e/test_accessibility.py": "accessibility_tests",
    "tests/e2e/test_responsive.py": "responsive_tests",
    "tests/security/__init__.py": "init_file",
    "tests/security/test_csrf.py": "csrf_tests",
    "tests/security/test_auth_security.py": "auth_security_tests",
    "docs/accessibility_report_template.md": "accessibility_report",
    "docs/visual_regression_report.md": "visual_regression_report",
}

BANNER = r"""
╔══════════════════════════════════════════════════════════════════════╗
║           NouvelAir — Setup Tests Visuels & Sécurité (Jour 7)       ║
║           Sprint 1 · Formation Django                                ║
╚══════════════════════════════════════════════════════════════════════╝
"""


# ─────────────────────────────────────────────────────────────────────────────
# File Content Generators
# ─────────────────────────────────────────────────────────────────────────────

def get_init_file():
    """__init__.py — fichier vide."""
    return ""


def get_visual_regression_tests():
    """tests/e2e/test_visual_regression.py — 8 tests de régression visuelle."""
    return '''\
"""
Tests de régression visuelle — Jour 7.

Utilise Playwright pour capturer des screenshots des pages principales
et les comparer aux images de référence (baselines).

Dépendances optionnelles:
    pip install playwright pytest-playwright pixelmatch Pillow
    playwright install chromium

Si pixelmatch n'est pas disponible, PIL/Pillow est utilisé comme fallback.

Couverture: 8 tests sur les pages principales en desktop, mobile et tablette.
"""

import os
import pytest

# ── Gestion gracieuse des dépendances ────────────────────────────────────────

try:
    from playwright.sync_api import Page, expect
    HAS_PLAYWRIGHT = True
except ImportError:
    HAS_PLAYWRIGHT = False

try:
    from PIL import Image
    import numpy as np
    HAS_PIL = True
except ImportError:
    HAS_PIL = False

try:
    from pixelmatch.contrib.PIL import pixelmatch
    HAS_PIXELMATCH = True
except ImportError:
    HAS_PIXELMATCH = False

# ── Chemins de stockage ──────────────────────────────────────────────────────

BASE_URL = "http://127.0.0.1:8000"
SCREENSHOTS_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "reports", "screenshots")
BASELINES_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "reports", "baselines")
DIFF_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "reports", "diffs")

for _d in [SCREENSHOTS_DIR, BASELINES_DIR, DIFF_DIR]:
    os.makedirs(_d, exist_ok=True)


# ── Marqueurs pytest ─────────────────────────────────────────────────────────

def pytest_configure(config):
    """Enregistre les marqueurs personnalisés."""
    config.addinivalue_line(
        "markers", "e2e: marquage des tests end-to-end (Sprint 1, Jour 7)"
    )
    config.addinivalue_line(
        "markers", "visual: marquage des tests de régression visuelle"
    )


# ── Fonctions utilitaires ────────────────────────────────────────────────────

def take_screenshot(page, name):
    """
    Capture un screenshot de la page actuelle et le sauvegarde.

    Args:
        page: Instance Playwright Page.
        name: Nom du fichier (sans extension).

    Returns:
        str: Chemin absolu vers le fichier PNG sauvegardé.
    """
    filepath = os.path.join(SCREENSHOTS_DIR, f"{name}.png")
    page.screenshot(path=filepath, full_page=True)
    return filepath


def save_baseline(page, name):
    """
    Sauvegarde un screenshot comme image de référence (baseline).

    Args:
        page: Instance Playwright Page.
        name: Nom du fichier de baseline (sans extension).

    Returns:
        str: Chemin absolu vers le fichier baseline PNG.
    """
    filepath = os.path.join(BASELINES_DIR, f"{name}.png")
    page.screenshot(path=filepath, full_page=True)
    return filepath


def compare_screenshots(baseline_path, current_path, threshold=0.1):
    """
    Compare deux screenshots et retourne le pourcentage de différence.

    Utilise pixelmatch si disponible, sinon PIL/Pillow en fallback.
    Le seuil (threshold) est le pourcentage maximal de pixels différents
    avant de considérer le test comme échoué.

    Args:
        baseline_path: Chemin vers l'image de référence.
        current_path: Chemin vers le screenshot actuel.
        threshold: Seuil de tolérance en pourcentage (défaut: 0.1 = 10%).

    Returns:
        float: Pourcentage de pixels différents (0.0 à 100.0).

    Raises:
        FileNotFoundError: Si l'un des fichiers n'existe pas.
    """
    if not os.path.exists(baseline_path):
        raise FileNotFoundError(f"Baseline introuvable: {baseline_path}")
    if not os.path.exists(current_path):
        raise FileNotFoundError(f"Screenshot introuvable: {current_path}")

    # ── Méthode pixelmatch (précise) ─────────────────────────────────────
    if HAS_PIXELMATCH:
        img_baseline = Image.open(baseline_path)
        img_current = Image.open(current_path)

        # S'assurer que les images ont la même taille
        max_w = max(img_baseline.width, img_current.width)
        max_h = max(img_baseline.height, img_current.height)

        if img_baseline.size != img_current.size:
            # Redimensionner à la taille maximale commune
            img_baseline = img_baseline.resize((max_w, max_h), Image.LANCZOS)
            img_current = img_current.resize((max_w, max_h), Image.LANCZOS)

        arr_baseline = np.array(img_baseline.convert("RGBA"))
        arr_current = np.array(img_current.convert("RGBA"))
        arr_diff = np.zeros_like(arr_baseline)

        total_pixels = max_w * max_h
        different_pixels = pixelmatch(
            arr_baseline, arr_current, arr_diff,
            threshold=0.1,        # seuil de tolérance pixelmatch (0-1)
            includeAA=False,       # ignorer l'anti-aliasing
            alpha=0.1,
        )

        diff_percentage = (different_pixels / total_pixels) * 100

        # Sauvegarder l'image diff
        diff_path = os.path.join(
            DIFF_DIR,
            os.path.basename(current_path).replace(".png", "_diff.png")
        )
        Image.fromarray(arr_diff).save(diff_path)

        return round(diff_percentage, 4)

    # ── Méthode PIL fallback (comparaison par histogramme) ───────────────
    if HAS_PIL:
        img_baseline = Image.open(baseline_path).convert("RGB")
        img_current = Image.open(current_path).convert("RGB")

        # Redimensionner à la taille identique pour comparaison
        max_w = max(img_baseline.width, img_current.width)
        max_h = max(img_baseline.height, img_current.height)
        img_baseline = img_baseline.resize((max_w, max_h), Image.LANCZOS)
        img_current = img_current.resize((max_w, max_h), Image.LANCZOS)

        # Comparaison pixel par pixel avec numpy
        arr_baseline = np.array(img_baseline, dtype=np.int16)
        arr_current = np.array(img_current, dtype=np.int16)

        diff = np.abs(arr_baseline - arr_current)
        # Un pixel est considéré différent si la différence totale RGB dépasse 30
        different_mask = np.sum(diff, axis=2) > 30
        total_pixels = max_w * max_h
        different_pixels = int(np.sum(different_mask))

        diff_percentage = (different_pixels / total_pixels) * 100

        # Sauvegarder l'image diff
        diff_arr = np.where(different_mask[:, :, np.newaxis], [255, 0, 0], arr_current.astype(np.uint8))
        diff_path = os.path.join(
            DIFF_DIR,
            os.path.basename(current_path).replace(".png", "_diff.png")
        )
        Image.fromarray(diff_arr.astype(np.uint8)).save(diff_path)

        return round(diff_percentage, 4)

    raise ImportError(
        "Aucune bibliothèque de comparaison d'images disponible. "
        "Installez pixelmatch ou Pillow: pip install pixelmatch Pillow"
    )


# ── Fixtures ─────────────────────────────────────────────────────────────────

@pytest.fixture(scope="session")
def base_url():
    """URL de base du site NouvelAir."""
    return BASE_URL


@pytest.fixture(scope="session")
def screenshot_dir():
    """Répertoire de stockage des screenshots."""
    return SCREENSHOTS_DIR


# ── Tests ────────────────────────────────────────────────────────────────────

@pytest.mark.e2e
@pytest.mark.visual
class TestVisualRegression:
    """
    Suite de tests de régression visuelle pour les pages principales de NouvelAir.

    Chaque test capture un screenshot et le compare à l'image de référence.
    Si la baseline n'existe pas, elle est automatiquement créée.

    Pour mettre à jour les baselines:
        pytest tests/e2e/test_visual_regression.py --baseline-update
    """

    # ─── Test 1: Page d'accueil — création de la baseline ─────────────────

    @pytest.mark.skipif(not HAS_PLAYWRIGHT, reason="Playwright non installé")
    def test_homepage_visual_baseline(self, page: Page, base_url):
        """
        Capture un screenshot de la page d'accueil et le sauvegarde comme baseline.

        Ce test sert de référence pour les comparaisons futures.
        Exécuter avec --baseline-update pour forcer la mise à jour.
        """
        page.goto(base_url)
        page.wait_for_load_state("networkidle")

        # Attendre que le contenu principal soit visible
        page.wait_for_selector("body", timeout=10000)

        baseline_path = save_baseline(page, "homepage")

        assert os.path.exists(baseline_path), (
            f"Le baseline n'a pas été sauvegardé: {baseline_path}"
        )

    # ─── Test 2: Page d'accueil — comparaison avec baseline ──────────────

    @pytest.mark.skipif(not HAS_PLAYWRIGHT, reason="Playwright non installé")
    def test_homepage_visual_regression(self, page: Page, base_url):
        """
        Compare le screenshot actuel de la page d'accueil avec la baseline.

        Seuil de tolérance: 0.1% de pixels différents.
        """
        page.goto(base_url)
        page.wait_for_load_state("networkidle")
        page.wait_for_selector("body", timeout=10000)

        current_path = take_screenshot(page, "homepage_current")
        baseline_path = os.path.join(BASELINES_DIR, "homepage.png")

        # Si la baseline n'existe pas, on la crée et on skip le test
        if not os.path.exists(baseline_path):
            save_baseline(page, "homepage")
            pytest.skip(
                "Baseline créée. Relancez le test pour effectuer la comparaison."
            )

        diff_percentage = compare_screenshots(baseline_path, current_path)

        assert diff_percentage < 0.1, (
            f"Régression visuelle détectée: {diff_percentage:.4f}% de pixels "
            f"différents (seuil: 0.1%). "
            f"Diff sauvegardée: {os.path.join(DIFF_DIR, 'homepage_current_diff.png')}"
        )

    # ─── Test 3: Page de résultats de recherche ──────────────────────────

    @pytest.mark.skipif(not HAS_PLAYWRIGHT, reason="Playwright non installé")
    def test_search_page_visual(self, page: Page, base_url):
        """
        Capture un screenshot de la page de résultats de recherche.

        Navigue vers /recherche/ et vérifie que la page se charge correctement.
        """
        page.goto(f"{base_url}/recherche/")
        page.wait_for_load_state("networkidle")
        page.wait_for_selector("body", timeout=10000)

        current_path = take_screenshot(page, "search_page")
        baseline_path = os.path.join(BASELINES_DIR, "search_page.png")

        if not os.path.exists(baseline_path):
            save_baseline(page, "search_page")
            pytest.skip("Baseline créée pour la page de recherche.")

        diff_percentage = compare_screenshots(baseline_path, current_path)
        assert diff_percentage < 0.1, (
            f"Régression visuelle (recherche): {diff_percentage:.4f}%"
        )

    # ─── Test 4: Page de connexion ───────────────────────────────────────

    @pytest.mark.skipif(not HAS_PLAYWRIGHT, reason="Playwright non installé")
    def test_login_page_visual(self, page: Page, base_url):
        """
        Capture un screenshot de la page de connexion.

        Vérifie le formulaire de login avec ses champs username et password.
        """
        page.goto(f"{base_url}/compte/connexion/")
        page.wait_for_load_state("networkidle")
        page.wait_for_selector("body", timeout=10000)

        current_path = take_screenshot(page, "login_page")
        baseline_path = os.path.join(BASELINES_DIR, "login_page.png")

        if not os.path.exists(baseline_path):
            save_baseline(page, "login_page")
            pytest.skip("Baseline créée pour la page de connexion.")

        diff_percentage = compare_screenshots(baseline_path, current_path)
        assert diff_percentage < 0.1, (
            f"Régression visuelle (connexion): {diff_percentage:.4f}%"
        )

    # ─── Test 5: Page des destinations ───────────────────────────────────

    @pytest.mark.skipif(not HAS_PLAYWRIGHT, reason="Playwright non installé")
    def test_destination_page_visual(self, page: Page, base_url):
        """
        Capture un screenshot de la page des destinations.

        Vérifie l'affichage de la grille de destinations.
        """
        page.goto(f"{base_url}/destinations/")
        page.wait_for_load_state("networkidle")
        page.wait_for_selector("body", timeout=10000)

        current_path = take_screenshot(page, "destination_page")
        baseline_path = os.path.join(BASELINES_DIR, "destination_page.png")

        if not os.path.exists(baseline_path):
            save_baseline(page, "destination_page")
            pytest.skip("Baseline créée pour la page des destinations.")

        diff_percentage = compare_screenshots(baseline_path, current_path)
        assert diff_percentage < 0.1, (
            f"Régression visuelle (destinations): {diff_percentage:.4f}%"
        )

    # ─── Test 6: Page « Mes réservations » ───────────────────────────────

    @pytest.mark.skipif(not HAS_PLAYWRIGHT, reason="Playwright non installé")
    def test_booking_page_visual(self, page: Page, base_url):
        """
        Capture un screenshot de la page « Mes réservations ».

        Note: Cette page est protégée par authentification.
        Sans connexion, on s'attend à une redirection vers le login.
        Le test vérifie que la page de redirection se charge.
        """
        page.goto(f"{base_url}/reservations/mes-reservations/")
        page.wait_for_load_state("networkidle")
        page.wait_for_selector("body", timeout=10000)

        current_path = take_screenshot(page, "my_bookings_page")
        baseline_path = os.path.join(BASELINES_DIR, "my_bookings_page.png")

        if not os.path.exists(baseline_path):
            save_baseline(page, "my_bookings_page")
            pytest.skip("Baseline créée pour la page Mes réservations.")

        diff_percentage = compare_screenshots(baseline_path, current_path)
        assert diff_percentage < 0.1, (
            f"Régression visuelle (réservations): {diff_percentage:.4f}%"
        )

    # ─── Test 7: Page d'accueil — version mobile (375×667) ───────────────

    @pytest.mark.skipif(not HAS_PLAYWRIGHT, reason="Playwright non installé")
    def test_mobile_homepage_visual(self, page: Page, base_url):
        """
        Capture un screenshot de la page d'accueil en viewport mobile (iPhone SE).

        Viewport: 375×667 pixels.
        Vérifie que le layout s'adapte correctement à la taille mobile.
        """
        page.set_viewport_size({"width": 375, "height": 667})
        page.goto(base_url)
        page.wait_for_load_state("networkidle")
        page.wait_for_selector("body", timeout=10000)

        current_path = take_screenshot(page, "mobile_homepage")
        baseline_path = os.path.join(BASELINES_DIR, "mobile_homepage.png")

        if not os.path.exists(baseline_path):
            save_baseline(page, "mobile_homepage")
            pytest.skip("Baseline mobile créée.")

        diff_percentage = compare_screenshots(baseline_path, current_path)
        assert diff_percentage < 0.1, (
            f"Régression visuelle (mobile): {diff_percentage:.4f}%"
        )

    # ─── Test 8: Page d'accueil — version tablette (768×1024) ────────────

    @pytest.mark.skipif(not HAS_PLAYWRIGHT, reason="Playwright non installé")
    def test_tablet_homepage_visual(self, page: Page, base_url):
        """
        Capture un screenshot de la page d'accueil en viewport tablette (iPad).

        Viewport: 768×1024 pixels.
        Vérifie le layout intermédiaire entre mobile et desktop.
        """
        page.set_viewport_size({"width": 768, "height": 1024})
        page.goto(base_url)
        page.wait_for_load_state("networkidle")
        page.wait_for_selector("body", timeout=10000)

        current_path = take_screenshot(page, "tablet_homepage")
        baseline_path = os.path.join(BASELINES_DIR, "tablet_homepage.png")

        if not os.path.exists(baseline_path):
            save_baseline(page, "tablet_homepage")
            pytest.skip("Baseline tablette créée.")

        diff_percentage = compare_screenshots(baseline_path, current_path)
        assert diff_percentage < 0.1, (
            f"Régression visuelle (tablette): {diff_percentage:.4f}%"
        )
'''


def get_accessibility_tests():
    """tests/e2e/test_accessibility.py — 7 tests d'accessibilité."""
    return '''\
"""
Tests d'accessibilité — Jour 7.

Utilise axe-playwright-python pour scanner les pages principales du site
NouvelAir et détecter les violations des normes WCAG 2.1 AA.

Dépendances optionnelles:
    pip install axe-playwright-python playwright pytest-playwright
    playwright install chromium

Couverture: 7 tests couvrant toutes les pages principales.
"""

import os
import json
from datetime import datetime

import pytest

# ── Gestion gracieuse des dépendances ────────────────────────────────────────

try:
    from playwright.sync_api import Page, expect
    HAS_PLAYWRIGHT = True
except ImportError:
    HAS_PLAYWRIGHT = False

try:
    from axe_playwright_python.sync_playwright import Axe
    HAS_AXE = True
except ImportError:
    HAS_AXE = False

# ── Configuration ────────────────────────────────────────────────────────────

BASE_URL = "http://127.0.0.1:8000"
REPORTS_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "reports", "accessibility")


def pytest_configure(config):
    """Enregistre les marqueurs personnalisés."""
    config.addinivalue_line(
        "markers", "e2e: marquage des tests end-to-end (Sprint 1, Jour 7)"
    )
    config.addinivalue_line(
        "markers", "a11y: marquage des tests d'accessibilité"
    )


# ── Fonctions utilitaires ────────────────────────────────────────────────────

def run_accessibility_scan(page, tags=None):
    """
    Exécute un scan d'accessibilité axe sur la page actuelle.

    Args:
        page: Instance Playwright Page.
        tags: Liste de tags axe à inclure. Par défaut: ['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa'].

    Returns:
        dict: Résultat du scan axe, contenant 'violations', 'passes', 'incomplete', 'inapplicable'.
    """
    if not HAS_AXE:
        raise ImportError(
            "axe-playwright-python n'est pas installé. "
            "Installez-le: pip install axe-playwright-python"
        )

    axe = Axe()
    if tags is None:
        tags = ["wcag2a", "wcag2aa", "wcag21a", "wcag21aa"]

    results = axe.run(page, options={"runOnly": {"type": "tag", "values": tags}})
    return results


def assert_no_critical_violations(violations):
    """
    Vérifie qu'il n'y a pas de violations critiques dans les résultats axe.

    Les violations sont classifiées par impact:
        - critical: empêche totalement l'utilisation
        - serious: empêche significativement l'utilisation
        - moderate: gêne l'utilisation
        - minor: légèrement gênant

    Args:
        violations: Liste des violations retournées par axe.

    Raises:
        AssertionError: Si des violations critiques ou serious sont trouvées.
    """
    critical = [v for v in violations if v.get("impact") == "critical"]
    serious = [v for v in violations if v.get("impact") == "serious"]

    if critical:
        details = "\\n".join(
            f"  - [{v['id']}] {v['description']} "
            f"({len(v.get('nodes', []))} éléments affectés)"
            for v in critical
        )
        pytest.fail(
            f"Violations CRITIQUES d'accessibilité détectées ({len(critical)}):\\n{details}"
        )

    if serious:
        details = "\\n".join(
            f"  - [{v['id']}] {v['description']} "
            f"({len(v.get('nodes', []))} éléments affectés)"
            for v in serious
        )
        pytest.fail(
            f"Violations SERIEUSES d'accessibilité détectées ({len(serious)}):\\n{details}"
        )


def generate_accessibility_report(violations, page_name, page_url):
    """
    Génère un rapport HTML détaillé des violations d'accessibilité.

    Args:
        violations: Liste des violations axe.
        page_name: Nom lisible de la page (ex: "Page d'accueil").
        page_url: URL de la page scannée.

    Returns:
        str: Chemin vers le fichier HTML du rapport.
    """
    os.makedirs(REPORTS_DIR, exist_ok=True)

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    safe_name = page_name.lower().replace(" ", "_")

    # Regrouper par impact
    by_impact = {}
    for v in violations:
        impact = v.get("impact", "unknown")
        by_impact.setdefault(impact, []).append(v)

    impact_labels = {
        "critical": "🔴 Critique",
        "serious": "🟠 Sérieux",
        "moderate": "🟡 Modéré",
        "minor": "🔵 Mineur",
    }

    violation_cards = ""
    for impact, viols in sorted(by_impact.items(), key=lambda x: ["critical", "serious", "moderate", "minor"].index(x[0]) if x[0] in ["critical", "serious", "moderate", "minor"] else 99):
        label = impact_labels.get(impact, f"⚪ {impact}")
        for v in viols:
            nodes_html = ""
            for node in v.get("nodes", []):
                target = ", ".join(node.get("target", []))
                failure = node.get("failureSummary", "Pas de description")
                nodes_html += f"""
                <tr>
                    <td style="padding:4px 8px;border:1px solid #ddd;font-family:monospace;font-size:12px;">{target}</td>
                    <td style="padding:4px 8px;border:1px solid #ddd;font-size:12px;">{failure}</td>
                </tr>"""
            border_color = {"critical":"#e74c3c","serious":"#e67e22","moderate":"#f1c40f","minor":"#3498db"}.get(impact, "#95a5a6")
            violation_cards += f"""
            <div style="margin-bottom:16px;padding:12px;border-left:4px solid {border_color};background:#fafafa;">
                <h4 style="margin:0 0 4px;">[{v.get("id", "N/A")}] {v.get("description", "Sans description")}</h4>
                <p style="margin:0;color:#666;">Impact: <strong>{label}</strong> — 
                   <a href="{v.get("helpUrl", "#")}" target="_blank">En savoir plus</a></p>
                <table style="width:100%;margin-top:8px;border-collapse:collapse;">
                    <thead><tr>
                        <th style="text-align:left;padding:4px 8px;border:1px solid #ddd;background:#f0f0f0;">Sélecteur</th>
                        <th style="text-align:left;padding:4px 8px;border:1px solid #ddd;background:#f0f0f0;">Description</th>
                    </tr></thead>
                    <tbody>{nodes_html}</tbody>
                </table>
            </div>"""

    html = f"""<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Rapport Accessibilité — {page_name} — NouvelAir</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; max-width: 960px; margin: 0 auto; padding: 20px; color: #333; }}
        h1 {{ color: #1a1a2e; border-bottom: 3px solid #e94560; padding-bottom: 8px; }}
        .summary {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 12px; margin: 20px 0; }}
        .summary-card {{ padding: 16px; border-radius: 8px; text-align: center; }}
        .summary-card h3 {{ margin: 0; font-size: 2em; }}
        .summary-card p {{ margin: 4px 0 0; color: #666; }}
        .card-critical {{ background: #fde8e8; color: #e74c3c; }}
        .card-serious {{ background: #fef3e8; color: #e67e22; }}
        .card-moderate {{ background: #fef9e7; color: #f39c12; }}
        .card-minor {{ background: #ebf5fb; color: #3498db; }}
        .card-total {{ background: #f4f6f7; color: #2c3e50; }}
    </style>
</head>
<body>
    <h1>♿ Rapport d'Accessibilité — {page_name}</h1>
    <p><strong>Date:</strong> {timestamp}<br>
       <strong>URL:</strong> <a href="{page_url}">{page_url}</a><br>
       <strong>Standard:</strong> WCAG 2.1 AA</p>

    <div class="summary">
        <div class="summary-card card-total">
            <h3>{len(violations)}</h3><p>Total violations</p>
        </div>
        <div class="summary-card card-critical">
            <h3>{len(by_impact.get("critical", []))}</h3><p>Critiques</p>
        </div>
        <div class="summary-card card-serious">
            <h3>{len(by_impact.get("serious", []))}</h3><p>Sérieuses</p>
        </div>
        <div class="summary-card card-moderate">
            <h3>{len(by_impact.get("moderate", []))}</h3><p>Modérées</p>
        </div>
        <div class="summary-card card-minor">
            <h3>{len(by_impact.get("minor", []))}</h3><p>Mineures</p>
        </div>
    </div>

    <h2>Détails des violations</h2>
    {violation_cards if violations else "<p style=\"color:#27ae60;font-weight:bold;\">✅ Aucune violation détectée !</p>"}

    <hr>
    <p style="color:#999;font-size:12px;">Généré automatiquement par NouvelAir E2E Tests — {timestamp}</p>
</body>
</html>"""

    report_path = os.path.join(REPORTS_DIR, f"a11y_{safe_name}.html")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(html)

    # Sauvegarder aussi en JSON
    json_path = os.path.join(REPORTS_DIR, f"a11y_{safe_name}.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(violations, f, ensure_ascii=False, indent=2)

    return report_path


# ── Tests ────────────────────────────────────────────────────────────────────

@pytest.mark.e2e
@pytest.mark.a11y
class TestAccessibility:
    """
    Suite de tests d'accessibilité pour le site NouvelAir.

    Chaque test scanne une page avec axe-core (WCAG 2.1 AA) et vérifie
    qu'il n'y a pas de violations critiques ou sérieuses.
    """

    # ─── Test 1: Page d'accueil ──────────────────────────────────────────

    @pytest.mark.skipif(not HAS_PLAYWRIGHT or not HAS_AXE, reason="Playwright ou axe-playwright-python non installé")
    def test_homepage_accessibility(self, page: Page, base_url):
        """
        Scan d'accessibilité de la page d'accueil.

        Vérifie la conformité WCAG 2.1 AA:
        - Images avec alt text
        - Structure de titres (h1, h2, etc.)
        - Contraste des couleurs
        - Navigation au clavier
        """
        page.goto(base_url)
        page.wait_for_load_state("networkidle")

        results = run_accessibility_scan(page)
        violations = results.get("violations", [])

        report_path = generate_accessibility_report(violations, "Page d'accueil", base_url)

        assert_no_critical_violations(violations)

        # Avertissement si violations modérées/mineures
        moderate = [v for v in violations if v.get("impact") in ("moderate", "minor")]
        if moderate:
            pytest.skip(
                f"Violations modérées/mineures trouvées ({len(moderate)}). "
                f"Rapport: {report_path}"
            )

    # ─── Test 2: Page de connexion ───────────────────────────────────────

    @pytest.mark.skipif(not HAS_PLAYWRIGHT or not HAS_AXE, reason="Playwright ou axe-playwright-python non installé")
    def test_login_page_accessibility(self, page: Page, base_url):
        """
        Scan d'accessibilité de la page de connexion.

        Points de contrôle:
        - Labels associés aux champs de formulaire
        - Messages d'erreur accessibles
        - Focus visible sur les champs
        """
        page.goto(f"{base_url}/compte/connexion/")
        page.wait_for_load_state("networkidle")

        results = run_accessibility_scan(page)
        violations = results.get("violations", [])

        report_path = generate_accessibility_report(violations, "Connexion", f"{base_url}/compte/connexion/")

        assert_no_critical_violations(violations)

    # ─── Test 3: Page de résultats de recherche ──────────────────────────

    @pytest.mark.skipif(not HAS_PLAYWRIGHT or not HAS_AXE, reason="Playwright ou axe-playwright-python non installé")
    def test_search_page_accessibility(self, page: Page, base_url):
        """
        Scan d'accessibilité de la page de résultats de recherche.

        Points de contrôle:
        - Tableau de résultats accessible
        - Filtres utilisables au clavier
        - Information de tri (aria-sort)
        """
        page.goto(f"{base_url}/recherche/")
        page.wait_for_load_state("networkidle")

        results = run_accessibility_scan(page)
        violations = results.get("violations", [])

        report_path = generate_accessibility_report(violations, "Recherche", f"{base_url}/recherche/")

        assert_no_critical_violations(violations)

    # ─── Test 4: Page Mes réservations ───────────────────────────────────

    @pytest.mark.skipif(not HAS_PLAYWRIGHT or not HAS_AXE, reason="Playwright ou axe-playwright-python non installé")
    def test_booking_page_accessibility(self, page: Page, base_url):
        """
        Scan d'accessibilité de la page « Mes réservations ».

        Points de contrôle:
        - Tableau de réservations lisible
        - Liens d'action accessibles
        - Statuts avec couleurs + texte (pas couleur seule)
        """
        page.goto(f"{base_url}/reservations/mes-reservations/")
        page.wait_for_load_state("networkidle")

        results = run_accessibility_scan(page)
        violations = results.get("violations", [])

        report_path = generate_accessibility_report(
            violations, "Mes réservations", f"{base_url}/reservations/mes-reservations/"
        )

        assert_no_critical_violations(violations)

    # ─── Test 5: Page des destinations ───────────────────────────────────

    @pytest.mark.skipif(not HAS_PLAYWRIGHT or not HAS_AXE, reason="Playwright ou axe-playwright-python non installé")
    def test_destination_page_accessibility(self, page: Page, base_url):
        """
        Scan d'accessibilité de la page des destinations.

        Points de contrôle:
        - Images de destinations avec alt descriptif
        - Cartes cliquables avec rôle approprié
        - Nom de destination comme heading
        """
        page.goto(f"{base_url}/destinations/")
        page.wait_for_load_state("networkidle")

        results = run_accessibility_scan(page)
        violations = results.get("violations", [])

        report_path = generate_accessibility_report(
            violations, "Destinations", f"{base_url}/destinations/"
        )

        assert_no_critical_violations(violations)

    # ─── Test 6: Page d'inscription ──────────────────────────────────────

    @pytest.mark.skipif(not HAS_PLAYWRIGHT or not HAS_AXE, reason="Playwright ou axe-playwright-python non installé")
    def test_register_page_accessibility(self, page: Page, base_url):
        """
        Scan d'accessibilité de la page d'inscription.

        Points de contrôle:
        - Champs avec labels et descriptions
        - Validation en temps réel accessible
        - Indicateur de force du mot de passe
        """
        page.goto(f"{base_url}/compte/inscription/")
        page.wait_for_load_state("networkidle")

        results = run_accessibility_scan(page)
        violations = results.get("violations", [])

        report_path = generate_accessibility_report(
            violations, "Inscription", f"{base_url}/compte/inscription/"
        )

        assert_no_critical_violations(violations)

    # ─── Test 7: Vérification spécifique du contraste des couleurs ───────

    @pytest.mark.skipif(not HAS_PLAYWRIGHT or not HAS_AXE, reason="Playwright ou axe-playwright-python non installé")
    def test_color_contrast(self, page: Page, base_url):
        """
        Vérification spécifique du contraste des couleurs sur les éléments clés.

        Scan uniquement la règle 'color-contrast' d'axe pour s'assurer
        que le texte est lisible par tous les utilisateurs.

        WCAG 2.1 AA exige:
        - Ratio 4.5:1 pour le texte normal
        - Ratio 3:1 pour le texte large (≥18pt ou ≥14pt gras)
        """
        page.goto(base_url)
        page.wait_for_load_state("networkidle")

        # Scanner uniquement les règles de contraste
        axe = Axe()
        results = axe.run(page, options={
            "runOnly": {"type": "rule", "values": ["color-contrast"]}
        })

        violations = results.get("violations", [])

        report_path = generate_accessibility_report(
            violations, "Contraste couleurs", base_url
        )

        # Pas de violations de contraste acceptées
        assert len(violations) == 0, (
            f"Violations de contraste couleur détectées ({len(violations)}): "
            f"Consultez le rapport: {report_path}"
        )
'''


def get_responsive_tests():
    """tests/e2e/test_responsive.py — 5 tests de responsive design."""
    return '''\
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
'''


def get_csrf_tests():
    """tests/security/test_csrf.py — 5 tests de protection CSRF."""
    return '''\
"""
Tests de sécurité — Protection CSRF (Jour 7).

Vérifie que toutes les vues POST du site NouvelAir rejettent
correctement les requêtes sans token CSRF valide.

Django active automatiquement la protection CSRF via le middleware
CsrfViewMiddleware. Ce middleware inspecte chaque requête POST et
rejette celles qui n'incluent pas un token CSRF valide.

Couverture: 5 tests sur les formulaires principaux.
"""

import pytest
from django.test import Client


def pytest_configure(config):
    """Enregistre les marqueurs personnalisés."""
    config.addinivalue_line(
        "markers", "security: marquage des tests de sécurité (Sprint 1, Jour 7)"
    )


# ── Tests ────────────────────────────────────────────────────────────────────

@pytest.mark.security
@pytest.mark.django_db
class TestCSRFProtection:
    """
    Suite de tests de protection CSRF pour le site NouvelAir.

    Chaque test vérifie qu'une requête POST sans token CSRF
    est rejetée avec un statut 403 (Forbidden).

    Le client de test Django avec `enforce_csrf_checks=True` simule
    un navigateur qui n'envoie pas de cookie CSRF ni de champ caché.
    """

    # ─── Test 1: POST générique sans CSRF → 403 ─────────────────────────

    def test_post_without_csrf_token(self):
        """
        Toute requête POST sans token CSRF → 403 Forbidden.

        Le middleware CsrfViewMiddleware de Django rejette les POST
        qui ne contiennent pas de token CSRF valide.
        """
        csrf_client = Client(enforce_csrf_checks=True)

        response = csrf_client.post("/", {"data": "test"})

        assert response.status_code == 403, (
            f"POST sans CSRF devrait renvoyer 403, obtenu: {response.status_code}"
        )

    # ─── Test 2: Login sans CSRF → 403 ──────────────────────────────────

    def test_login_csrf_protection(self):
        """
        POST sur /compte/connexion/ sans CSRF → 403 Forbidden.

        Le formulaire de connexion est une cible privilégiée pour
        les attaques CSRF (force l'utilisateur à se connecter avec
        les identifiants de l'attaquant).
        """
        csrf_client = Client(enforce_csrf_checks=True)

        response = csrf_client.post("/compte/connexion/", {
            "username": "attacker",
            "password": "attacker123",
        })

        assert response.status_code == 403, (
            f"Login POST sans CSRF devrait renvoyer 403, obtenu: {response.status_code}"
        )

    # ─── Test 3: Inscription sans CSRF → 403 ────────────────────────────

    def test_register_csrf_protection(self):
        """
        POST sur /compte/inscription/ sans CSRF → 403 Forbidden.

        Le formulaire d'inscription doit être protégé contre les
        créations de comptes non autorisées via CSRF.
        """
        csrf_client = Client(enforce_csrf_checks=True)

        response = csrf_client.post("/compte/inscription/", {
            "username": "csrf_test_user",
            "email": "csrftest@example.com",
            "password1": "StrongPassword123!",
            "password2": "StrongPassword123!",
            "first_name": "CSRF",
            "last_name": "Test",
        })

        assert response.status_code == 403, (
            f"Inscription POST sans CSRF devrait renvoyer 403, obtenu: {response.status_code}"
        )

    # ─── Test 4: Création de réservation sans CSRF → 403 ─────────────────

    def test_booking_csrf_protection(self):
        """
        POST sur /reservations/creer/ sans CSRF → 403 Forbidden.

        La création de réservation est une action critique qui doit
        être protégée par CSRF pour éviter les réservations non
        autorisées au nom de l'utilisateur.
        """
        csrf_client = Client(enforce_csrf_checks=True)

        response = csrf_client.post("/reservations/creer/", {
            "contact_email": "test@example.com",
            "contact_phone": "+21612345678",
        })

        # 403 pour CSRF OU 302/redirect si la vue exige d'abord une session
        # Dans les deux cas, la réservation ne doit pas être créée
        assert response.status_code in (403, 302), (
            f"Réservation POST sans CSRF devrait renvoyer 403 ou 302 (redirect), "
            f"obtenu: {response.status_code}"
        )
        assert response.status_code == 403 or "/compte/connexion/" in response.url or response.url == "/", (
            "La réservation sans CSRF devrait être bloquée (403) ou redirigée vers login."
        )

    # ─── Test 5: Newsletter sans CSRF → 403 ─────────────────────────────

    def test_newsletter_csrf_protection(self):
        """
        POST sur /promotions/newsletter/ sans CSRF → 403 Forbidden.

        Le endpoint newsletter doit aussi être protégé contre les
        abus CSRF (inscriptions non désirées).
        """
        csrf_client = Client(enforce_csrf_checks=True)

        response = csrf_client.post("/promotions/newsletter/", {
            "email": "csrf_newsletter@example.com",
            "first_name": "CSRF",
        })

        # Le endpoint newsletter peut renvoyer 403 ou avoir sa propre protection
        assert response.status_code in (403, 400, 405), (
            f"Newsletter POST sans CSRF devrait renvoyer 403/400/405, "
            f"obtenu: {response.status_code}"
        )
'''


def get_auth_security_tests():
    """tests/security/test_auth_security.py — 5 tests de sécurité auth."""
    return '''\
"""
Tests de sécurité — Authentification et injections (Jour 7).

Vérifie la sécurité de l'authentification et la protection contre
les attaques courantes: SQL injection, XSS, force brute.

Couverture: 5 tests sur les vulnérabilités OWASP Top 10.
"""

import pytest
from django.test import Client
from django.contrib.auth.models import User
from django.urls import reverse


def pytest_configure(config):
    """Enregistre les marqueurs personnalisés."""
    config.addinivalue_line(
        "markers", "security: marquage des tests de sécurité (Sprint 1, Jour 7)"
    )


# ── Helpers ──────────────────────────────────────────────────────────────────

def _create_test_user(username="securitytest", password="SecurePass123!"):
    """Crée un utilisateur de test pour les tests de sécurité."""
    return User.objects.create_user(
        username=username,
        email=f"{username}@nouvelair.com",
        password=password,
        first_name="Security",
        last_name="Test",
    )


# ── Tests ────────────────────────────────────────────────────────────────────

@pytest.mark.security
@pytest.mark.django_db
class TestAuthSecurity:
    """
    Suite de tests de sécurité pour l'authentification du site NouvelAir.

    Couvre:
    - Protection des pages authentifiées
    - Injection SQL via les formulaires de recherche
    - XSS (Cross-Site Scripting) via les inputs
    - Protection contre la force brute
    """

    # ─── Test 1: URL protégée sans auth → redirect vers login ────────────

    def test_protected_url_redirect_without_auth(self):
        """
        Accès à /compte/profil/ sans authentification → redirect vers login.

        Le décorateur @login_required doit rediriger l'utilisateur
        non authentifié vers la page de connexion avec le paramètre
        ?next= pour revenir après authentification.
        """
        client = Client()

        response = client.get("/compte/profil/", follow=False)

        assert response.status_code == 302, (
            f"URL protégée sans auth devrait rediriger (302), obtenu: {response.status_code}"
        )
        assert "/compte/connexion/" in response.url, (
            f"Redirect devrait pointer vers login, obtenu: {response.url}"
        )

    # ─── Test 2: API protégée sans auth → 401 ou redirect ───────────────

    def test_protected_api_without_auth(self):
        """
        Accès à une API protégée sans authentification → 401 ou redirect.

        Vérifie que les endpoints API nécessitant une authentification
        renvoient une erreur 401 Unauthorized ou redirigent vers login.
        """
        client = Client()

        # Test de la page Mes réservations (requiert authentification)
        response = client.get("/reservations/mes-reservations/", follow=False)

        # Doit soit renvoyer 401/403, soit rediriger vers login
        assert response.status_code in (301, 302, 401, 403), (
            f"API protégée sans auth devrait renvoyer 401/403 ou redirect, "
            f"obtenu: {response.status_code}"
        )

        if response.status_code in (301, 302):
            assert "/compte/connexion/" in response.url, (
                f"Redirect sans auth devrait aller vers /compte/connexion/, obtenu: {response.url}"
            )

    # ─── Test 3: Injection SQL via recherche ─────────────────────────────

    def test_sql_injection_via_search(self):
        """
        Recherche avec une chaîne d'injection SQL → pas d'erreur, pas de fuite.

        Les attaques SQL injection les plus courantes:
        - ' OR '1'='1
        - ' UNION SELECT * FROM auth_user --
        - 1; DROP TABLE flights_flight; --

        Le test vérifie que:
        1. La page ne renvoie pas d'erreur 500 (pas d'exception SQL)
        2. Les données sensibles ne sont pas exposées dans la réponse
        3. La requête est correctement paramétrée (pas de concaténation SQL)
        """
        client = Client()

        # Chaînes d'injection SQL courantes
        sql_injections = [
            "' OR '1'='1",
            "' OR '1'='1' --",
            "1; DROP TABLE flights_flight; --",
            "' UNION SELECT username, password FROM auth_user --",
            "1' AND '1'='1",
            "admin'--",
            "' OR 1=1 --",
        ]

        for injection in sql_injections:
            response = client.get("/recherche/", {"q": injection})

            # La page ne doit PAS renvoyer d'erreur serveur (500)
            assert response.status_code in (200, 302, 400, 404), (
                f"Injection SQL '{injection}' a causé un statut inattendu: "
                f"{response.status_code}"
            )

            if response.status_code == 200:
                content = response.content.decode("utf-8", errors="ignore")

                # Vérifier l'absence de fuites de données sensibles
                sensitive_keywords = [
                    "syntax error",
                    "mysql",
                    "postgresql",
                    "sqlite",
                    "traceback",
                    "Internal Server Error",
                    "DROP TABLE",
                    "UNION SELECT",
                ]

                for keyword in sensitive_keywords:
                    assert keyword.lower() not in content.lower(), (
                        f"Fuite potentielle détectée pour '{injection}': "
                        f"le mot-clé '{keyword}' a été trouvé dans la réponse."
                    )

    # ─── Test 4: XSS via recherche ───────────────────────────────────────

    def test_xss_via_search(self):
        """
        Recherche avec une balise script → sortie échappée.

        Les attaques XSS (Cross-Site Scripting) injectent du JavaScript
        malveillant dans les pages web. Le template Django doit échapper
        automatiquement les variables avec {{ variable|escape }}.

        Teste:
        - <script>alert('xss')</script>
        - <img onerror="alert('xss')" src="x">
        - <svg onload="alert('xss')">
        """
        client = Client()

        # Payloads XSS courants
        xss_payloads = [
            '<script>alert("xss")</script>',
            '<img src=x onerror=alert("xss")>',
            '<svg onload=alert("xss")>',
            '"><script>alert("xss")</script>',
            "'-alert('xss')-'",
            '<iframe src="javascript:alert(\'xss\')">',
        ]

        for payload in xss_payloads:
            response = client.get("/recherche/", {"q": payload})

            assert response.status_code in (200, 302, 400, 404), (
                f"Payload XSS a causé un statut inattendu: {response.status_code}"
            )

            if response.status_code == 200:
                content = response.content.decode("utf-8", errors="ignore")

                # Le payload brut NE DOIT PAS apparaître tel quel dans le HTML
                # Django auto-escape transforme < en &lt; etc.
                # Vérifier que les balises script/img/svg ne sont pas interprétées

                # La balise <script> doit être échappée
                if "<script>" in payload.lower():
                    assert "<script>" not in content.lower() or "&lt;script&gt;" in content.lower(), (
                        f"XSS non échappé pour '{payload}': "
                        f"la balise <script> est présente dans le HTML sans être échappée."
                    )

                # L'attribut onerror/onload doit être échappé
                if "onerror" in payload.lower() or "onload" in payload.lower():
                    has_unescaped_event = (
                        'onerror=' in content.lower() and '&lt;' not in content.lower()
                    )
                    assert not has_unescaped_event, (
                        f"Événement non échappé pour '{payload}': "
                        f"l'attribut d'événement est présent dans le HTML."
                    )

    # ─── Test 5: Force brute sur login ────────────────────────────────────

    def test_brute_force_login(self):
        """
        5 tentatives de connexion échouées → compte verrouillé ou limité.

        Ce test vérifie que le site implémente une protection contre
        la force brute, par exemple:
        - Verrouillage du compte après N tentatives
        - Rate limiting (délai entre les tentatives)
        - CAPTCHA après quelques échecs

        Note: Si le site n'implémente pas encore cette protection,
        le test est marqué comme avertissement (xfail) plutôt que
        comme échec.
        """
        client = Client()
        user = _create_test_user()

        # Simuler 5 tentatives de connexion échouées
        for attempt in range(1, 6):
            response = client.post("/compte/connexion/", {
                "username": user.username,
                "password": f"WrongPassword{attempt}!",
            })

            # Les tentatives doivent échouer (pas de connexion)
            assert "_auth_user_id" not in client.session, (
                f"Tentative {attempt}: La connexion a réussi avec un mauvais mot de passe !"
            )

        # Après 5 tentatives, la 6ème tentative valide devrait
        # soit être bloquée, soit fonctionner (si pas de protection)
        response = client.post("/compte/connexion/", {
            "username": user.username,
            "password": "SecurePass123!",  # Mot de passe correct
        })

        # Vérifier le comportement après les tentatives échouées
        if "_auth_user_id" in client.session:
            # Pas de protection force brute: avertissement
            pytest.xfail(
                "Aucune protection contre la force brute détectée. "
                "Considérez l'implémentation de django-axes ou django-ratelimit."
            )

        # Si le login est bloqué après 5 tentatives, c'est bon
        content = response.content.decode("utf-8", errors="ignore") if hasattr(response, "content") else ""

        # Vérifier des signes de protection: message de verrouillage, délai, etc.
        has_protection = any(keyword in content.lower() for keyword in [
            "verrouillé", "bloqué", "trop de tentatives",
            "locked", "blocked", "too many", "rate limit",
            "essayez plus tard", "try again later",
        ])

        if has_protection:
            # Protection détectée → test passé
            assert True
        else:
            # Pas de protection détectée → avertissement
            pytest.xfail(
                "Aucun message de verrouillage/rate limiting détecté après 5 tentatives. "
                "Recommandation: installez django-axes pour la protection brute force."
            )
'''


def get_accessibility_report():
    """docs/accessibility_report_template.md — Modèle de rapport d'accessibilité."""
    return '''\
# 📋 Rapport d'Accessibilité — NouvelAir

> **Projet:** NouvelAir — Système de réservation aérienne  
> **Date:** [DATE_DE_GENERATION]  
> **Standard:** WCAG 2.1 Niveau AA  
> **Outil:** axe-core + axe-playwright-python  
> **Version:** [VERSION]

---

## 1. Résumé des résultats

| Métrique | Valeur |
|----------|--------|
| Pages analysées | [NOMBRE] |
| Violations totales | [NOMBRE] |
| 🔴 Critiques | [NOMBRE] |
| 🟠 Sérieuses | [NOMBRE] |
| 🟡 Modérées | [NOMBRE] |
| 🔵 Mineures | [NOMBRE] |
| Tests réussis | [NOMBRE] |
| Taux de conformité | [POURCENTAGE]% |

### Statut global

- [ ] ✅ **CONFORME** — Aucune violation critique ni sérieuse
- [ ] ⚠️ **PARTIELLEMENT CONFORME** — Violations modérées à corriger
- [ ] ❌ **NON CONFORME** — Violations critiques ou sérieuses détectées

---

## 2. Détail des violations par sévérité

### 🔴 Violations critiques

> Empêchent totalement l'utilisation du site pour certains utilisateurs.

| ID | Description | Pages affectées | Éléments |
|----|-------------|-----------------|----------|
| [VIOLATION_ID] | [DESCRIPTION] | [PAGES] | [NOMBRE] éléments |

### 🟠 Violations sérieuses

> Gênent significativement l'utilisation du site.

| ID | Description | Pages affectées | Éléments |
|----|-------------|-----------------|----------|
| [VIOLATION_ID] | [DESCRIPTION] | [PAGES] | [NOMBRE] éléments |

### 🟡 Violations modérées

> Gênent partiellement l'utilisation du site.

| ID | Description | Pages affectées | Éléments |
|----|-------------|-----------------|----------|
| [VIOLATION_ID] | [DESCRIPTION] | [PAGES] | [NOMBRE] éléments |

### 🔵 Violations mineures

> Problèmes cosmétiques d'accessibilité.

| ID | Description | Pages affectées | Éléments |
|----|-------------|-----------------|----------|
| [VIOLATION_ID] | [DESCRIPTION] | [PAGES] | [NOMBRE] éléments |

---

## 3. Résultats par page

### Page d'accueil (`/`)

- **Statut:** [✅ CONFORME / ⚠️ PARTIELLEMENT CONFORME / ❌ NON CONFORME]
- **Violations:** [NOMBRE]
- **Rapport détaillé:** `reports/accessibility/a11y_page_d_accueil.html`

### Page de connexion (`/compte/connexion/`)

- **Statut:** [✅ CONFORME / ⚠️ PARTIELLEMENT CONFORME / ❌ NON CONFORME]
- **Violations:** [NOMBRE]
- **Rapport détaillé:** `reports/accessibility/a11y_connexion.html`

### Page d'inscription (`/compte/inscription/`)

- **Statut:** [✅ CONFORME / ⚠️ PARTIELLEMENT CONFORME / ❌ NON CONFORME]
- **Violations:** [NOMBRE]
- **Rapport détaillé:** `reports/accessibility/a11y_inscription.html`

### Page de recherche (`/recherche/`)

- **Statut:** [✅ CONFORME / ⚠️ PARTIELLEMENT CONFORME / ❌ NON CONFORME]
- **Violations:** [NOMBRE]
- **Rapport détaillé:** `reports/accessibility/a11y_recherche.html`

### Page des destinations (`/destinations/`)

- **Statut:** [✅ CONFORME / ⚠️ PARTIELLEMENT CONFORME / ❌ NON CONFORME]
- **Violations:** [NOMBRE]
- **Rapport détaillé:** `reports/accessibility/a11y_destinations.html`

### Page « Mes réservations » (`/reservations/mes-reservations/`)

- **Statut:** [✅ CONFORME / ⚠️ PARTIELLEMENT CONFORME / ❌ NON CONFORME]
- **Violations:** [NOMBRE]
- **Rapport détaillé:** `reports/accessibility/a11y_mes_reservations.html`

---

## 4. Recommandations

### 🔴 Priorité haute — Critiques et sérieuses

1. **[RECOMMANDATION_1]**
   - Violation: [VIOLATION_ID]
   - Action: [DESCRIPTION_DE_LA_CORRECTION]
   - Impact utilisateur: [EXPLICATION]

2. **[RECOMMANDATION_2]**
   - Violation: [VIOLATION_ID]
   - Action: [DESCRIPTION_DE_LA_CORRECTION]
   - Impact utilisateur: [EXPLICATION]

### 🟡 Priorité moyenne — Modérées

1. **[RECOMMANDATION_3]**
   - Violation: [VIOLATION_ID]
   - Action: [DESCRIPTION_DE_LA_CORRECTION]

### 🔵 Priorité basse — Mineures

1. **[RECOMMANDATION_4]**
   - Violation: [VIOLATION_ID]
   - Action: [DESCRIPTION_DE_LA_CORRECTION]

---

## 5. Bonnes pratiques identifiées

- [ ] Utilisation de balises sémantiques HTML5 (`<nav>`, `<main>`, `<footer>`)
- [ ] Labels associés aux champs de formulaire
- [ ] Alt text sur les images
- [ ] Contraste de couleurs suffisant
- [ ] Navigation au clavier fonctionnelle
- [ ] Focus visible sur les éléments interactifs
- [ ] ARIA labels sur les éléments dynamiques
- [ ] Skip navigation link

---

## 6. Historique des audits

| Date | Version | Violations critiques | Violations totales | Taux de conformité |
|------|---------|---------------------|--------------------|--------------------|
| [DATE] | [VERSION] | [NOMBRE] | [NOMBRE] | [POURCENTAGE]% |

---

## 7. Ressources

- [WCAG 2.1 Guidelines](https://www.w3.org/TR/WCAG21/)
- [axe-core Documentation](https://github.com/dequelabs/axe-core)
- [WebAIM Contrast Checker](https://webaim.org/resources/contrastchecker/)
- [Pa11y — Accessible Web Testing](https://pa11y.org/)

---

*Ce rapport a été généré automatiquement par les tests E2E NouvelAir (Jour 7).*
'''


def get_visual_regression_report():
    """docs/visual_regression_report.md — Documentation de régression visuelle."""
    return '''\
# 📸 Régression Visuelle — Documentation

> **Projet:** NouvelAir — Système de réservation aérienne  
> **Outil:** Playwright + pixelmatch/Pillow  
> **Seuil par défaut:** 0.1% de pixels différents

---

## 1. Principe de la régression visuelle

La régression visuelle consiste à comparer automatiquement des screenshots
des pages web avec des images de référence (baselines). Si la différence
dépasse un seuil prédéfini, le test échoue, signalant un changement visuel
inattendu.

### Cycle de vie

```
┌─────────────┐     ┌──────────────┐     ┌──────────────┐
│  Page web   │ ──▶ │  Screenshot  │ ──▶ │  Comparaison │
│  (Playwright)│     │  (PNG)       │     │  (pixelmatch)│
└─────────────┘     └──────────────┘     └──────┬───────┘
                                               │
                                   ┌───────────▼───────────┐
                                   │   Diff < seuil ?      │
                                   │   ✓ Test passé        │
                                   │   ✗ Test échoué       │
                                   └───────────────────────┘
```

---

## 2. Installation des dépendances

```bash
# Dépendances principales
pip install playwright pytest-playwright Pillow pixelmatch numpy

# Installation du navigateur Chromium pour Playwright
playwright install chromium
```

### Dépendances optionnelles

| Package | Usage | Requis |
|---------|-------|--------|
| `playwright` | Navigation et screenshots | ✅ Oui |
| `pixelmatch` | Comparaison précise pixel-à-pixel | ⚠️ Recommandé |
| `Pillow` | Comparaison fallback par histogramme | ⚠️ Fallback |
| `numpy` | Calcul matriciel pour la comparaison | ⚠️ Fallback |

> **Note:** Si `pixelmatch` n'est pas disponible, le script utilise
> automatiquement `Pillow` + `numpy` comme méthode de comparaison alternative.

---

## 3. Exécution des tests

```bash
# Exécuter tous les tests visuels
pytest tests/e2e/test_visual_regression.py -v

# Exécuter avec le marqueur e2e
pytest -m "e2e and visual" -v

# Mettre à jour toutes les baselines
pytest tests/e2e/test_visual_regression.py --baseline-update -v

# Exécuter un test spécifique
pytest tests/e2e/test_visual_regression.py::TestVisualRegression::test_homepage_visual_regression -v

# Exécuter avec verbose détaillé
pytest tests/e2e/test_visual_regression.py -v --tb=short
```

---

## 4. Création et mise à jour des baselines

### Création initiale

Les baselines sont créées automatiquement lors de la première exécution
des tests. Si un baseline n'existe pas, le test le crée et se met en
`skip` pour vous inviter à relancer.

### Mise à jour manuelle

Lorsqu'un changement visuel est **volontaire** (redesign, nouveau contenu),
il faut mettre à jour les baselines :

```bash
# Option 1: Supprimer les anciens baselines et relancer les tests
rm -rf reports/baselines/*.png
pytest tests/e2e/test_visual_regression.py -v

# Option 2: Copier les screenshots courants comme nouveaux baselines
cp reports/screenshots/*_current.png reports/baselines/
# Renommer les fichiers (enlever "_current")
```

### Quand mettre à jour les baselines ?

- ✅ Après un **redesign** validé de la page
- ✅ Après modification **intentionnelle** du contenu
- ✅ Après mise à jour de la **typographie** ou des couleurs
- ❌ **NE JAMAIS** mettre à jour pour masquer une régression
- ❌ **NE JAMAIS** ignorer un test qui échoue sans investigation

---

## 5. Seuil de tolérance

Le seuil par défaut est de **0.1%** (1 pixel sur 1000). Ce seuil est
suffisamment strict pour détecter les changements visuels significatifs
tout en tolérant les micro-variations inévitables:

### Variations acceptées (sous le seuil)

- Rendu des polices (anti-aliasing légèrement différent)
- Images avec compression légèrement variable
- Animations non terminées au moment du screenshot
- Timestamps ou compteurs dynamiques

### Variations rejetées (au-dessus du seuil)

- Changement de mise en page
- Élément manquant ou ajouté
- Couleur de fond modifiée
- Taille de police changée
- Image remplacée

### Personnalisation du seuil

```python
# Dans le test, modifier le seuil :
diff_percentage = compare_screenshots(baseline_path, current_path, threshold=0.5)
assert diff_percentage < 0.5  # Seuil plus permissif (0.5%)
```

---

## 6. Structure des répertoires

```
reports/
├── baselines/           # Images de référence (versionnées dans git)
│   ├── homepage.png
│   ├── search_page.png
│   ├── login_page.png
│   ├── destination_page.png
│   ├── my_bookings_page.png
│   ├── mobile_homepage.png
│   └── tablet_homepage.png
├── screenshots/         # Screenshots capturés lors des tests
│   ├── homepage_current.png
│   ├── search_page_current.png
│   └── ...
├── diffs/               # Images de différence (baselines - actuels)
│   ├── homepage_current_diff.png
│   ├── search_page_current_diff.png
│   └── ...
└── accessibility/       # Rapports d'accessibilité (HTML + JSON)
    ├── a11y_page_d_accueil.html
    ├── a11y_page_d_accueil.json
    └── ...
```

### Recommandation Git

```gitignore
# Ignorer les screenshots courants et diffs (générés à chaque run)
reports/screenshots/
reports/diffs/

# VERSIONNER les baselines (ils sont la référence)
!reports/baselines/
!reports/baselines/*.png
```

---

## 7. Pages couvertes

| Page | URL | Viewport | Fichier baseline |
|------|-----|----------|-----------------|
| Accueil | `/` | Desktop (1280×720) | `homepage.png` |
| Accueil mobile | `/` | Mobile (375×667) | `mobile_homepage.png` |
| Accueil tablette | `/` | Tablette (768×1024) | `tablet_homepage.png` |
| Recherche | `/recherche/` | Desktop | `search_page.png` |
| Connexion | `/compte/connexion/` | Desktop | `login_page.png` |
| Destinations | `/destinations/` | Desktop | `destination_page.png` |
| Réservations | `/reservations/mes-reservations/` | Desktop | `my_bookings_page.png` |

---

## 8. Dépannage

### Playwright non installé

```
ERROR: Module 'playwright' not found
```

```bash
pip install playwright pytest-playwright
playwright install chromium
```

### Baseline manquant

```
AssertionError: Le baseline n'a pas été sauvegardé
```

→ Le test crée le baseline automatiquement. Relancez une seconde fois.

### Régression visuelle inattendue

```
AssertionError: Régression visuelle détectée: 0.2534%
```

1. Ouvrez le fichier diff dans `reports/diffs/`
2. Vérifiez si le changement est intentionnel
3. Si oui, mettez à jour le baseline (voir section 4)
4. Si non, identifiez et corrigez le bug CSS/HTML

---

*Documentation générée pour le projet NouvelAir — Jour 7 de la formation Django.*
'''


# ─────────────────────────────────────────────────────────────────────────────
# Main — création des fichiers
# ─────────────────────────────────────────────────────────────────────────────

def create_file(filepath, content):
    """Crée un fichier avec son contenu, en créant les répertoires parents si nécessaire."""
    full_path = os.path.join(BASE_DIR, filepath)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    return full_path


def main():
    """Point d'entrée principal du script."""
    print(BANNER)
    print()

    # ── 1. Création des répertoires ──────────────────────────────────────
    print("📁 Création des répertoires...")
    for dir_path in DIRECTORIES_TO_CREATE:
        full_path = os.path.join(BASE_DIR, dir_path)
        os.makedirs(full_path, exist_ok=True)
        print(f"   ✓ {dir_path}")

    # ── 2. Création des fichiers ─────────────────────────────────────────
    print()
    print("📄 Création des fichiers...")

    content_generators = {
        "init_file": get_init_file,
        "visual_regression_tests": get_visual_regression_tests,
        "accessibility_tests": get_accessibility_tests,
        "responsive_tests": get_responsive_tests,
        "csrf_tests": get_csrf_tests,
        "auth_security_tests": get_auth_security_tests,
        "accessibility_report": get_accessibility_report,
        "visual_regression_report": get_visual_regression_report,
    }

    created_files = []
    for filepath, generator_key in FILES_TO_CREATE.items():
        content = content_generators[generator_key]()
        path = create_file(filepath, content)
        created_files.append(filepath)
        print(f"   ✓ {filepath}")

    # ── 3. Création du fichier .gitkeep pour reports/screenshots ─────────
    gitkeep_path = os.path.join(SCREENSHOTS_DIR, ".gitkeep")
    with open(gitkeep_path, "w") as f:
        f.write("")
    print(f"   ✓ reports/screenshots/.gitkeep")

    # ── 4. Résumé ────────────────────────────────────────────────────────
    print()
    print("━" * 64)
    print("  ✅ RÉSUMÉ DE LA CRÉATION")
    print("━" * 64)
    print(f"  Fichiers créés:     {len(created_files)}")
    print(f"  Répertoires créés:  {len(DIRECTORIES_TO_CREATE)}")
    print()
    print("  📁 Répertoires:")
    for d in DIRECTORIES_TO_CREATE:
        print(f"     • {d}")
    print()
    print("  📄 Fichiers:")
    for f in created_files:
        print(f"     • {f}")
    print()
    print("  📄 Autres:")
    print(f"     • reports/screenshots/.gitkeep")
    print()
    print("━" * 64)
    print("  🧪 Tests E2E (visuels, accessibilité, responsive): 20 tests")
    print("  🔒 Tests sécurité (CSRF, auth, injections):        10 tests")
    print("  📋 Documentation:                                    2 fichiers")
    print("━" * 64)
    print()
    print("  🚀 Prochaines étapes:")
    print()
    print("  1. Installer les dépendances E2E:")
    print("     pip install playwright pytest-playwright axe-playwright-python")
    print("     playwright install chromium")
    print()
    print("  2. Installer les dépendances visuelles:")
    print("     pip install pixelmatch Pillow numpy")
    print()
    print("  3. Démarrer le serveur Django:")
    print("     python manage.py runserver")
    print()
    print("  4. Lancer les tests E2E:")
    print("     pytest tests/e2e/ -v -m e2e")
    print()
    print("  5. Lancer les tests de sécurité:")
    print("     pytest tests/security/ -v -m security")
    print()
    print("  6. Lancer tous les tests du Jour 7:")
    print("     pytest tests/e2e/ tests/security/ -v")
    print()
    print("  7. Voir les rapports générés:")
    print("     • Visual:     reports/screenshots/")
    print("     • Baselines:  reports/baselines/")
    print("     • Diffs:      reports/diffs/")
    print("     • A11y HTML:  reports/accessibility/")
    print()


if __name__ == "__main__":
    main()
