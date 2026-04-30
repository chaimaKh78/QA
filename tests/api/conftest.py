"""
Fixtures partagées pour les tests API - Jour 5.

Fournit des utilitaires pour les requêtes API via Django test client,
incluant la gestion CSRF et la factory pour les utilisateurs de test.
"""

import pytest
from django.test import Client
from django.contrib.auth.models import User


# ── Marqueur pytest personnalisé ──────────────────────────────────────────────

def pytest_configure(config):
    """Enregistre le marqueur 'api' pour les tests API."""
    config.addinivalue_line(
        "markers", "api: marquage des tests d'API (Sprint 1, Jour 5)"
    )


# ── Fixtures de base ─────────────────────────────────────────────────────────

@pytest.fixture
def api_client():
    """
    Client de test Django standard pour les requêtes API.

    Contrairement au navigateur, le test client Django contourne
    automatiquement la vérification CSRF dans les requêtes POST
    lorsqu'on utilise enforce_csrf_checks=False (par défaut).

    Usage:
        response = api_client.get('/api/endpoint/')
        response = api_client.post('/api/endpoint/', data={...})
    """
    return Client()


@pytest.fixture
def csrf_client():
    """
    Client de test qui active explicitement la vérification CSRF.

    Ce client doit être utilisé pour tester que les vues rejettent
    correctement les requêtes sans token CSRF.

    Usage:
        response = csrf_client.post('/api/endpoint/', data={...})
        assert response.status_code == 403
    """
    return Client(enforce_csrf_checks=True)


@pytest.fixture
def api_client_factory():
    """
    Factory retournant un callable pour créer des clients configurables.

    Permet de créer des clients avec des options spécifiques (auth,
    headers, etc.) pour différents scénarios de test.

    Usage:
        factory = api_client_factory()
        client = client()
        authenticated_client = factory(user=user)

    Returns:
        callable: fonction acceptant des kwargs pour configurer le client.
    """
    def _factory(**kwargs):
        client = Client(**kwargs)
        return client
    return _factory


@pytest.fixture
def authenticated_client(api_client):
    """
    Client pré-authentifié avec un utilisateur de test standard.

    Crée un utilisateur avec les informations par défaut et le connecte
    automatiquement au client de test.

    Returns:
        tuple: (client, user) où user est l'utilisateur Django créé.
    """
    user = User.objects.create_user(
        username="testuser",
        email="testuser@nouvelair.com",
        password="SecurePass123!",
        first_name="Test",
        last_name="User",
    )
    api_client.force_login(user)
    return api_client, user


@pytest.fixture
def staff_client(api_client):
    """
    Client authentifié en tant que membre du staff (admin).

    Returns:
        tuple: (client, user) où user est un administrateur.
    """
    user = User.objects.create_superuser(
        username="admin",
        email="admin@nouvelair.com",
        password="AdminPass123!",
        first_name="Admin",
        last_name="NouvelAir",
    )
    api_client.force_login(user)
    return api_client, user


@pytest.fixture
def sample_airport_data():
    """
    Dictionnaire de données pour créer un aéroport de test.

    Returns:
        dict: données valides pour Airport.objects.create().
    """
    return {
        "code": "TST",
        "name": "Test Airport",
        "city": "Test City",
        "country": "Tunisia",
        "latitude": "36.806500",
        "longitude": "10.181500",
        "is_active": True,
    }


@pytest.fixture
def sample_user_data():
    """
    Dictionnaire de données pour créer un utilisateur de test.

    Returns:
        dict: données valides pour l'inscription.
    """
    return {
        "username": "newuser",
        "email": "newuser@example.com",
        "password1": "StrongPassword123!",
        "password2": "StrongPassword123!",
        "first_name": "Nouveau",
        "last_name": "Utilisateur",
    }


@pytest.fixture
def sample_booking_data():
    """
    Dictionnaire de données pour la recherche de réservation.

    Returns:
        dict: données pour le formulaire de lookup.
    """
    return {
        "reference": "ABCDEF12",
        "email": "client@nouvelair.com",
    }
