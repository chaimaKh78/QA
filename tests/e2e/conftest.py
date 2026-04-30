"""
Fixtures Playwright pour les tests E2E - Jour 6.

Fournit les fixtures partagées pour tous les tests E2E :
- page : fixture page Playwright (API synchrone)
- browser_context : contexte avec viewport 1280x720
- base_url : URL de base de l'application
- screenshot_on_failure : capture automatique d'écran en cas d'échec
- traced_page : page avec trace activée pour le débogage
"""

import os
import pytest
from playwright.sync_api import Page, BrowserContext, Browser


# ── Configuration ────────────────────────────────────────────────────────────

BASE_URL = os.environ.get("NOUVELAIR_BASE_URL", "http://127.0.0.1:8000")


# ── Marqueur pytest personnalisé ─────────────────────────────────────────────

def pytest_configure(config):
    """Enregistre le marqueur 'e2e' pour les tests E2E Playwright."""
    config.addinivalue_line(
        "markers", "e2e: marquage des tests End-to-End Playwright (Sprint 1, Jour 6)"
    )


# ── Fixtures de base ─────────────────────────────────────────────────────────

@pytest.fixture(scope="function")
def base_url():
    """
    URL de base de l'application NouvelAir.

    Peut être surchargée via la variable d'environnement NOUVELAIR_BASE_URL.

    Returns:
        str: URL de base (défaut: http://127.0.0.1:8000).
    """
    return BASE_URL


@pytest.fixture(scope="function")
def browser_context(browser, base_url):
    """
    Contexte de navigateur avec viewport 1280x720.

    Crée un nouveau contexte de navigateur avec une taille de fenêtre
    standardisée pour tous les tests E2E.

    Args:
        browser: fixture Playwright browser.
        base_url: URL de base de l'application.

    Yields:
        BrowserContext: contexte de navigateur configuré.
    """
    context = browser.new_context(
        viewport={"width": 1280, "height": 720},
        base_url=base_url,
    )
    yield context
    context.close()


@pytest.fixture(scope="function")
def page(browser_context):
    """
    Page Playwright synchronisée avec contexte configuré.

    C'est la fixture principale utilisée dans chaque test E2E.
    La page hérite automatiquement du viewport et de la base_url
    configurés dans browser_context.

    Args:
        browser_context: contexte de navigateur avec viewport 1280x720.

    Yields:
        Page: instance de page Playwright prête à interagir.
    """
    page = browser_context.new_page()
    yield page
    page.close()


@pytest.fixture(scope="function")
def screenshot_on_failure(page, request):
    """
    Capture automatique d'écran en cas d'échec de test.

    En cas d'échec, une capture d'écran est sauvegardée dans
    test-results/screenshots/<nom_du_test>-failure.png.

    Args:
        page: fixture page Playwright.
        request: objet request de pytest contenant les métadonnées du test.
    """
    yield page
    if request.node.rep_call.failed if hasattr(request.node, "rep_call") else False:
        screenshots_dir = os.path.join("test-results", "screenshots")
        os.makedirs(screenshots_dir, exist_ok=True)
        screenshot_path = os.path.join(
            screenshots_dir,
            f"{request.node.name}-failure.png",
        )
        page.screenshot(path=screenshot_path, full_page=True)


@pytest.fixture(scope="function")
def traced_page(browser_context, request):
    """
    Page avec trace Playwright activée pour le débogage.

    La trace est conservée uniquement en cas d'échec du test,
    dans test-results/traces/<nom_du_test>-trace.zip.

    Args:
        browser_context: contexte de navigateur Playwright.
        request: objet request de pytest.

    Yields:
        Page: page avec tracing activé.
    """
    traces_dir = os.path.join("test-results", "traces")
    os.makedirs(traces_dir, exist_ok=True)
    trace_path = os.path.join(traces_dir, f"{request.node.name}-trace.zip")

    browser_context.tracing.start(
        screenshots=True,
        snapshots=True,
        sources=True,
    )

    page = browser_context.new_page()
    yield page
    page.close()

    failed = request.node.rep_call.failed if hasattr(request.node, "rep_call") else False
    if failed:
        browser_context.tracing.stop(path=trace_path)
    else:
        browser_context.tracing.stop()


# ── Hook pytest_runtest_makereport pour screenshot_on_failure ────────────────

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Hook pytest qui capture le résultat du test (pass/fail) pour permettre
    à la fixture screenshot_on_failure de prendre des captures d'écran
    uniquement en cas d'échec.

    Le résultat est stocké dans item.node.rep_call.
    """
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)
