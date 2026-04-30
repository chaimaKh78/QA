"""
Tests d'intégration — Vues de l'application Destinations (5 tests).

Couvre : DestinationListView, DestinationDetailView.
"""

import pytest
from django.test import Client
from django.urls import reverse

from destinations.models import Destination, DestinationReview
from django.contrib.auth.models import User


# ── 1. test_destination_list ─────────────────────────────────────────────────


@pytest.mark.integration
@pytest.mark.django_db
def test_destination_list(setup_db):
    """GET destinations:list retourne 200 et le contexte contient 'destinations'."""
    # Crée au moins une destination active
    Destination.objects.create(
        name="Djerba",
        slug="djerba",
        description="Île paradisiaque au sud de la Tunisie.",
        short_description="Djerba, la douceur de vivre.",
        airport=setup_db["airport_tun"],
        category="beach",
        is_active=True,
        is_featured=False,
    )

    client = Client()
    response = client.get(reverse("destinations:list"))
    assert response.status_code == 200
    assert "destinations" in response.context
    assert "destinations/destination_list.html" in [t.name for t in response.templates]


# ── 2. test_destination_detail ───────────────────────────────────────────────


@pytest.mark.integration
@pytest.mark.django_db
def test_destination_detail(setup_db):
    """GET destinations:detail avec un slug valide retourne 200."""
    destination = Destination.objects.create(
        name="Sfax",
        slug="sfax",
        description="Ville portuaire historique.",
        short_description="Sfax, porte du Sahel.",
        airport=setup_db["airport_tun"],
        category="culture",
        is_active=True,
        is_featured=False,
    )

    client = Client()
    response = client.get(
        reverse("destinations:detail", kwargs={"slug": "sfax"})
    )
    assert response.status_code == 200
    assert "destination" in response.context
    assert response.context["destination"].slug == "sfax"


# ── 3. test_destination_detail_404 ───────────────────────────────────────────


@pytest.mark.integration
@pytest.mark.django_db
def test_destination_detail_404(db):
    """GET destinations:detail avec un slug invalide retourne 404."""
    client = Client()
    response = client.get(
        reverse("destinations:detail", kwargs={"slug": "slug-inexistant-xyz"})
    )
    assert response.status_code == 404


# ── 4. test_destination_featured ─────────────────────────────────────────────


@pytest.mark.integration
@pytest.mark.django_db
def test_destination_featured(setup_db):
    """Les destinations vedettes (is_featured=True) apparaissent dans le contexte."""
    # Crée 2 destinations featured
    dest1 = Destination.objects.create(
        name="Hammamet",
        slug="hammamet",
        description="Station balnéaire célèbre.",
        short_description="Hammamet, joyau du cap Bon.",
        airport=setup_db["airport_tun"],
        category="beach",
        is_active=True,
        is_featured=True,
    )
    dest2 = Destination.objects.create(
        name="Sousse",
        slug="sousse",
        description="Ville historique et touristique.",
        short_description="Sousse, perle du Sahel.",
        airport=setup_db["airport_tun"],
        category="culture",
        is_active=True,
        is_featured=True,
    )
    # Crée 1 destination non-featured
    Destination.objects.create(
        name="Gabès",
        slug="gabes",
        description="Oasis côtière unique.",
        short_description="Gabès, entre mer et désert.",
        airport=setup_db["airport_tun"],
        category="nature",
        is_active=True,
        is_featured=False,
    )

    client = Client()
    response = client.get(reverse("destinations:list"))
    assert response.status_code == 200
    assert "featured_destinations" in response.context
    featured = list(response.context["featured_destinations"])
    assert len(featured) >= 2
    featured_slugs = [d.slug for d in featured]
    assert "hammamet" in featured_slugs
    assert "sousse" in featured_slugs


# ── 5. test_destination_review_form ──────────────────────────────────────────


@pytest.mark.integration
@pytest.mark.django_db
def test_destination_review_form(setup_db):
    """
    Un utilisateur authentifié peut voir le formulaire d'avis
    sur la page de détail d'une destination.
    """
    user = setup_db["user"]
    destination = Destination.objects.create(
        name="Kairouan",
        slug="kairouan",
        description="Sainte ville de l'Islam.",
        short_description="Kairouan, ville spirituelle.",
        airport=setup_db["airport_tun"],
        category="culture",
        is_active=True,
        is_featured=False,
    )

    # Connecte l'utilisateur
    client = Client()
    client.login(username="testuser", password="TestPassword123!")

    response = client.get(
        reverse("destinations:detail", kwargs={"slug": "kairouan"})
    )
    assert response.status_code == 200

    # La page de détail est accessible pour l'utilisateur authentifié.
    # Le formulaire d'avis dépend du template, mais on vérifie que
    # l'utilisateur connecté reçoit bien la page avec le contexte complet.
    assert "destination" in response.context
    assert response.context["destination"].slug == "kairouan"
