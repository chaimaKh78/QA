"""
Tests d'intégration — Vues de l'application Promotions (5 tests).

Couvre : PromotionListView, PromotionDetailView, NewsletterSubscribeView.
"""

import pytest
from datetime import timedelta
from django.test import Client
from django.urls import reverse
from django.utils import timezone

from promotions.models import Promotion, NewsletterSubscription


# ── 1. test_promotion_list ───────────────────────────────────────────────────


@pytest.mark.integration
@pytest.mark.django_db
def test_promotion_list(db):
    """GET promotions:list retourne 200 et le contexte contient 'promotions'."""
    # Crée une promotion active
    now = timezone.now()
    Promotion.objects.create(
        code="PROMO20",
        name="Réduction 20%",
        description="20% de réduction sur tous les vols.",
        promo_type="percentage",
        discount_percentage=20.00,
        discount_amount=0,
        start_date=now - timedelta(hours=1),
        end_date=now + timedelta(days=30),
        max_uses=100,
        current_uses=0,
        is_active=True,
        is_featured=True,
    )

    client = Client()
    response = client.get(reverse("promotions:list"))
    assert response.status_code == 200
    assert "promotions" in response.context
    assert "promotions/promotion_list.html" in [t.name for t in response.templates]
    # Au moins la promotion créée doit apparaître
    promotions = list(response.context["promotions"])
    assert len(promotions) >= 1


# ── 2. test_promotion_detail ─────────────────────────────────────────────────


@pytest.mark.integration
@pytest.mark.django_db
def test_promotion_detail(db):
    """GET promotions:detail avec un code valide retourne 200."""
    now = timezone.now()
    promo = Promotion.objects.create(
        code="SUMMER2025",
        name="Offre Été 2025",
        description="Offres spéciales pour l'été 2025.",
        promo_type="percentage",
        discount_percentage=15.00,
        discount_amount=0,
        start_date=now - timedelta(hours=1),
        end_date=now + timedelta(days=60),
        max_uses=200,
        current_uses=5,
        is_active=True,
        is_featured=False,
    )

    client = Client()
    response = client.get(
        reverse("promotions:detail", kwargs={"code": "SUMMER2025"})
    )
    assert response.status_code == 200
    assert "promotion" in response.context
    assert response.context["promotion"].code == "SUMMER2025"


# ── 3. test_promotion_detail_404 ─────────────────────────────────────────────


@pytest.mark.integration
@pytest.mark.django_db
def test_promotion_detail_404(db):
    """GET promotions:detail avec un code invalide retourne 404."""
    client = Client()
    response = client.get(
        reverse("promotions:detail", kwargs={"code": "INEXISTANT"})
    )
    assert response.status_code == 404


# ── 4. test_newsletter_subscribe_success ─────────────────────────────────────


@pytest.mark.integration
@pytest.mark.django_db
def test_newsletter_subscribe_success(db):
    """POST avec un email valide vers la newsletter retourne un succès JSON."""
    client = Client()
    response = client.post(
        reverse("promotions:newsletter_subscribe"),
        data={"email": "subscriber@example.com", "first_name": "Ahmed"},
    )
    assert response.status_code == 200
    assert response["Content-Type"] == "application/json"

    data = response.json()
    assert data["success"] is True
    assert "Merci" in data.get("message", "")

    # Vérifie que l'abonnement a été créé en base
    assert NewsletterSubscription.objects.filter(
        email="subscriber@example.com"
    ).exists()


# ── 5. test_newsletter_subscribe_duplicate ───────────────────────────────────


@pytest.mark.integration
@pytest.mark.django_db
def test_newsletter_subscribe_duplicate(db):
    """POST avec un email déjà inscrit retourne une erreur JSON."""
    # Crée un abonnement existant
    NewsletterSubscription.objects.create(
        email="existing@example.com",
        first_name="Fatma",
    )

    client = Client()
    response = client.post(
        reverse("promotions:newsletter_subscribe"),
        data={"email": "existing@example.com"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is False
    assert "déjà" in data.get("error", "").lower() or "inscrit" in data.get("error", "").lower()
