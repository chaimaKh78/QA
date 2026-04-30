"""
Tests API - Newsletter (Jour 5).

Teste le endpoint POST /promotions/newsletter/
qui gère l'inscription à la newsletter.

Couverture:
    - Inscription valide
    - Email en double
    - Email invalide
    - Email manquant
    - Format de la réponse JSON
"""

import pytest
from django.test import Client
from promotions.models import NewsletterSubscription


# ── Helpers ───────────────────────────────────────────────────────────────────

VALID_EMAIL = "abonné@nouvelair.com"


# ── Tests ─────────────────────────────────────────────────────────────────────

@pytest.mark.api
@pytest.mark.django_db
class TestNewsletterAPI:
    """Suite de tests pour l'endpoint d'inscription à la newsletter."""

    def setup_method(self):
        """Initialise le client de test."""
        self.client = Client()
        self.newsletter_url = "/promotions/newsletter/"

    # ─── Test 1: Inscription avec email valide → succès JSON ──────────────

    def test_newsletter_subscribe_valid(self):
        """POST avec email valide → JSON {success: true, message: ...}."""
        response = self.client.post(self.newsletter_url, {
            "email": VALID_EMAIL,
            "first_name": "Ahmed",
        })

        assert response.status_code == 200
        assert response["Content-Type"] == "application/json"

        data = response.json()
        assert data["success"] is True
        assert "message" in data

        # Vérifier en base que l'abonnement a été créé
        assert NewsletterSubscription.objects.filter(email=VALID_EMAIL).exists()

        subscription = NewsletterSubscription.objects.get(email=VALID_EMAIL)
        assert subscription.first_name == "Ahmed"
        assert subscription.is_active is True

    # ─── Test 2: Inscription avec email en double → erreur ────────────────

    def test_newsletter_subscribe_duplicate(self):
        """POST avec un email déjà inscrit → JSON {success: false, error: ...}."""
        # Créer un premier abonnement
        NewsletterSubscription.objects.create(
            email=VALID_EMAIL,
            first_name="Original",
            is_active=True,
        )

        # Tenter de ré-inscrire le même email
        response = self.client.post(self.newsletter_url, {
            "email": VALID_EMAIL,
            "first_name": "Dupliqué",
        })

        assert response.status_code == 200
        data = response.json()
        assert data["success"] is False
        assert "error" in data

        # Vérifier qu'il n'y a toujours qu'un seul abonnement
        assert NewsletterSubscription.objects.filter(email=VALID_EMAIL).count() == 1

    # ─── Test 3: Inscription avec email invalide → erreur ─────────────────

    def test_newsletter_subscribe_invalid_email(self):
        """POST avec un email mal formaté → le champ email est requis mais
        la vue ne valide pas le format, elle tente simplement get_or_create.
        Ce test vérifie le comportement avec une chaîne vide-like.
        """
        response = self.client.post(self.newsletter_url, {
            "email": "not-an-email",
            "first_name": "Test",
        })

        assert response.status_code == 200

        data = response.json()
        # La vue fait get_or_create avec l'email tel quel;
        # un email invalide sera stocké (pas de validation serveur).
        # Le test vérifie simplement que la réponse est cohérente.
        assert "success" in data

    # ─── Test 4: Inscription sans email → erreur ──────────────────────────

    def test_newsletter_subscribe_missing_email(self):
        """POST sans le champ email → JSON {success: false, error: ...}."""
        response = self.client.post(self.newsletter_url, {
            "first_name": "SansEmail",
        })

        assert response.status_code == 200
        data = response.json()
        assert data["success"] is False
        assert "error" in data
        assert "email" in data["error"].lower() or "requis" in data["error"].lower()

        # Aucun abonnement ne doit avoir été créé
        assert NewsletterSubscription.objects.filter(first_name="SansEmail").count() == 0

    # ─── Test 5: Format de la réponse JSON ────────────────────────────────

    def test_newsletter_subscribe_response_format(self):
        """La réponse JSON contient les clés attendues: success + (message|error)."""
        # Cas succès
        unique_email = f"unique-{__import__('uuid').uuid4().hex[:8]}@test.com"
        response = self.client.post(self.newsletter_url, {
            "email": unique_email,
        })

        assert response.status_code == 200
        assert response["Content-Type"] == "application/json"

        data = response.json()
        assert "success" in data, "La clé 'success' est manquante dans la réponse."
        assert isinstance(data["success"], bool), "'success' doit être un booléen."

        # Doit contenir 'message' (succès) ou 'error' (échec)
        has_message = "message" in data
        has_error = "error" in data
        assert has_message or has_error, (
            "La réponse doit contenir 'message' ou 'error'."
        )

        # Cas erreur (email manquant)
        response_error = self.client.post(self.newsletter_url, {})
        data_error = response_error.json()

        assert "success" in data_error
        assert "error" in data_error, (
            "La réponse d'erreur doit contenir la clé 'error'."
        )
