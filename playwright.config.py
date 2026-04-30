"""
Configuration Playwright pour les tests E2E - Jour 6 (NouvelAir).

Définit les paramètres globaux pour l'exécution des tests End-to-End :
- URL de base de l'application
- Mode headless
- Capture d'écran et vidéo en cas d'échec
- Trace pour le débogage
- Navigateur par défaut et viewport
"""

# ── Configuration Playwright ──────────────────────────────────────────────────

# URL de base de l'application NouvelAir
# Peut être surchargée via la variable d'environnement NOUVELAIR_BASE_URL
import os

BASE_URL = os.environ.get("NOUVELAIR_BASE_URL", "http://127.0.0.1:8000")

# ── Configuration du serveur de développement ─────────────────────────────────

# Configuration pour pytest-playwright
def pytest_configure(config):
    """
    Configure les paramètres Playwright pour les tests pytest.
    """
    pass


# ── Paramètres Playwright ────────────────────────────────────────────────────

# Ces paramètres sont utilisés par le fichier playwright.config.py
# et peuvent aussi être passés en ligne de commande :
#   pytest --browser chromium --headed
#   pytest --browser firefox
#   pytest --browser webkit

PLAYWRIGHT_CONFIG = {
    # URL de base de l'application
    "base_url": BASE_URL,

    # Exécuter les tests sans interface graphique
    "headless": True,

    # Capturer une capture d'écran uniquement en cas d'échec de test
    "screenshot": "only-on-failure",

    # Conserver la vidéo d'exécution uniquement en cas d'échec
    "video": "retain-on-failure",

    # Conserver la trace Playwright uniquement en cas d'échec
    "trace": "retain-on-failure",

    # Navigateur par défaut pour l'exécution des tests
    "browser": "chromium",

    # Temps d'attente maximal pour les opérations (en millisecondes)
    "timeout": 30000,

    # Taille de la fenêtre du navigateur
    "viewport": {
        "width": 1280,
        "height": 720,
    },
}


# ── Configuration pytest-playwright ───────────────────────────────────────────

# Marqueurs pytest personnalisés
pytest_markers = [
    "e2e: marquage des tests End-to-End Playwright (Sprint 1, Jour 6)",
]

# Dossiers de sortie pour les artefacts de test
OUTPUT_DIR = "test-results"
SCREENSHOTS_DIR = os.path.join(OUTPUT_DIR, "screenshots")
TRACES_DIR = os.path.join(OUTPUT_DIR, "traces")
VIDEOS_DIR = os.path.join(OUTPUT_DIR, "videos")


# ── Section conftest pour pytest ─────────────────────────────────────────────

def get_browser_launch_args():
    """
    Retourne les arguments de lancement du navigateur.

    Returns:
        list: arguments pour le lancement du navigateur.
    """
    return [
        "--no-sandbox",
        "--disable-setuid-sandbox",
        "--disable-dev-shm-usage",
    ]


def get_context_options():
    """
    Retourne les options de création du contexte de navigateur.

    Returns:
        dict: options pour la création du contexte.
    """
    return {
        "viewport": PLAYWRIGHT_CONFIG["viewport"],
        "base_url": PLAYWRIGHT_CONFIG["base_url"],
        "ignore_https_errors": True,
    }
