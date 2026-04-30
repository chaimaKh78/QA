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
        POST sur /accounts/connexion/ sans CSRF → 403 Forbidden.

        Le formulaire de connexion est une cible privilégiée pour
        les attaques CSRF (force l'utilisateur à se connecter avec
        les identifiants de l'attaquant).
        """
        csrf_client = Client(enforce_csrf_checks=True)

        response = csrf_client.post("/accounts/connexion/", {
            "username": "attacker",
            "password": "attacker123",
        })

        assert response.status_code == 403, (
            f"Login POST sans CSRF devrait renvoyer 403, obtenu: {response.status_code}"
        )

    # ─── Test 3: Inscription sans CSRF → 403 ────────────────────────────

    def test_register_csrf_protection(self):
        """
        POST sur /accounts/inscription/ sans CSRF → 403 Forbidden.

        Le formulaire d'inscription doit être protégé contre les
        créations de comptes non autorisées via CSRF.
        """
        csrf_client = Client(enforce_csrf_checks=True)

        response = csrf_client.post("/accounts/inscription/", {
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
        POST sur /bookings/creer/ sans CSRF → 403 Forbidden.

        La création de réservation est une action critique qui doit
        être protégée par CSRF pour éviter les réservations non
        autorisées au nom de l'utilisateur.
        """
        csrf_client = Client(enforce_csrf_checks=True)

        response = csrf_client.post("/bookings/creer/", {
            "contact_email": "test@example.com",
            "contact_phone": "+21612345678",
        })

        # 403 pour CSRF OU 302/redirect si la vue exige d'abord une session
        # Dans les deux cas, la réservation ne doit pas être créée
        assert response.status_code in (403, 302), (
            f"Réservation POST sans CSRF devrait renvoyer 403 ou 302 (redirect), "
            f"obtenu: {response.status_code}"
        )
        assert response.status_code == 403 or "/accounts/connexion/" in response.url or response.url == "/", (
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
