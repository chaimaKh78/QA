\
"""
Tests API - Authentification (Jour 5).

Teste les endpoints liés à l'authentification:
    - POST /accounts/connexion/   → login
    - POST /accounts/inscription/ → register
    - GET  /accounts/deconnexion/ → logout
    - GET  /accounts/profil/      → page protégée

Couverture:
    - Connexion valide/invalide
    - Vérification CSRF
    - Inscription avec email dupliqué
    - Protection des pages authentifiées
    - Persistance de session
"""

import pytest
from django.test import Client
from django.contrib.auth.models import User
from accounts.models import UserProfile


# ── Helpers ───────────────────────────────────────────────────────────────────

def _create_test_user(username="testuser", password="SecurePass123!", **kwargs):
    """Crée un utilisateur de test avec profil."""
    defaults = {
        "email": f"{username}@nouvelair.com",
        "first_name": "Test",
        "last_name": "User",
    }
    defaults.update(kwargs)
    user = User.objects.create_user(
        username=username,
        password=password,
        email=defaults["email"],
        first_name=defaults["first_name"],
        last_name=defaults["last_name"],
    )
    UserProfile.objects.create(user=user)
    return user


# ── Tests ─────────────────────────────────────────────────────────────────────

@pytest.mark.api
@pytest.mark.django_db
class TestAuthLoginAPI:
    """Suite de tests pour l'endpoint de connexion."""

    def setup_method(self):
        """Initialise le client et crée un utilisateur."""
        self.user = _create_test_user()
        self.login_url = "/accounts/connexion/"
        self.client = Client()

    # ─── Test 1: Login avec identifiants valides → redirect ───────────────

    def test_login_api_valid(self):
        """POST /accounts/connexion/ avec identifiants valides → 302 redirect."""
        response = self.client.post(self.login_url, {
            "username": "testuser",
            "password": "SecurePass123!",
        }, follow=False)

        assert response.status_code == 302
        # Le redirect va vers l'accueil ou la page 'next'
        assert response.url in ["/", "/accounts/profil/"]

        # Vérifier que l'utilisateur est bien connecté
        assert "_auth_user_id" in self.client.session

    # ─── Test 2: Login avec mot de passe invalide → 200 avec erreur ───────

    def test_login_api_invalid(self):
        """POST avec mauvais mot de passe → 200 avec formulaire d'erreur."""
        response = self.client.post(self.login_url, {
            "username": "testuser",
            "password": "WrongPassword999!",
        })

        assert response.status_code == 200
        # Vérifier que l'utilisateur n'est PAS connecté
        assert "_auth_user_id" not in self.client.session

    # ─── Test 3: Login sans CSRF token → 403 ─────────────────────────────

    def test_login_api_csrf(self):
        """POST sans token CSRF → 403 Forbidden."""
        csrf_client = Client(enforce_csrf_checks=True)

        response = csrf_client.post(self.login_url, {
            "username": "testuser",
            "password": "SecurePass123!",
        })

        # Avec enforce_csrf_checks=True et sans token, Django renvoie 403
        assert response.status_code == 403


@pytest.mark.api
@pytest.mark.django_db
class TestAuthRegisterAPI:
    """Suite de tests pour l'endpoint d'inscription."""

    def setup_method(self):
        """Initialise le client."""
        self.register_url = "/accounts/inscription/"
        self.client = Client()

    # ─── Test 4: Inscription avec données valides → nouvel utilisateur ────

    def test_register_api_valid(self):
        """POST /accounts/inscription/ avec données valides → nouvel utilisateur + redirect."""
        user_count_before = User.objects.count()

        response = self.client.post(self.register_url, {
            "username": "newtraveler",
            "email": "newtraveler@nouvelair.com",
            "password1": "StrongPassword456!",
            "password2": "StrongPassword456!",
            "first_name": "Voyageur",
            "last_name": "Nouveau",
        }, follow=False)

        assert response.status_code == 302
        assert User.objects.count() == user_count_before + 1

        # Vérifier que le nouvel utilisateur existe
        new_user = User.objects.get(username="newtraveler")
        assert new_user.email == "newtraveler@nouvelair.com"
        assert new_user.first_name == "Voyageur"

        # Vérifier que le profil a été créé
        assert hasattr(new_user, "profile")

        # Vérifier que l'utilisateur est connecté après inscription
        assert "_auth_user_id" in self.client.session

    # ─── Test 5: Inscription avec email dupliqué → erreur ─────────────────

    def test_register_api_duplicate_email(self):
        """POST avec un email déjà utilisé → erreur dans le formulaire."""
        _create_test_user(username="existinguser", email="dup@example.com")

        response = self.client.post(self.register_url, {
            "username": "anotheruser",
            "email": "dup@example.com",
            "password1": "StrongPassword456!",
            "password2": "StrongPassword456!",
            "first_name": "Autre",
            "last_name": "Utilisateur",
        })

        assert response.status_code == 200
        content = response.content.decode()

        # Le formulaire doit afficher une erreur concernant l'email
        assert (
            "email" in content.lower()
            or "déjà" in content.lower()
            or "existe" in content.lower()
        )

        # Aucun nouvel utilisateur ne doit avoir été créé
        assert User.objects.filter(username="anotheruser").count() == 0


@pytest.mark.api
@pytest.mark.django_db
class TestAuthLogoutAPI:
    """Suite de tests pour la déconnexion."""

    def setup_method(self):
        """Initialise le client et connecte un utilisateur."""
        self.user = _create_test_user()
        self.logout_url = "/accounts/deconnexion/"
        self.client = Client()
        self.client.force_login(self.user)

    # ─── Test 6: Logout → redirect vers accueil ───────────────────────────

    def test_logout_api(self):
        """GET /accounts/deconnexion/ → déconnecte l'utilisateur et redirige."""
        # Vérifier que l'utilisateur est connecté
        assert "_auth_user_id" in self.client.session

        response = self.client.get(self.logout_url, follow=False)

        assert response.status_code == 302
        assert response.url == "/"

        # Vérifier que l'utilisateur est déconnecté
        assert "_auth_user_id" not in self.client.session


@pytest.mark.api
@pytest.mark.django_db
class TestProtectedPagesAPI:
    """Suite de tests pour la protection des pages authentifiées."""

    def setup_method(self):
        """Initialise le client."""
        self.client = Client()
        self.profile_url = "/accounts/profil/"

    # ─── Test 7: Page protégée sans auth → redirect vers login ────────────

    def test_protected_api_redirect(self):
        """GET page protégée sans authentification → 302 vers la page de login."""
        response = self.client.get(self.profile_url, follow=False)

        assert response.status_code == 302
        # Le redirect doit pointer vers la page de connexion
        assert "/accounts/connexion/" in response.url or "/compte/login/" in response.url

    # ─── Test 8: Persistance de session après login ───────────────────────

    def test_session_persistence(self):
        """Login → accéder page protégée → succès (session persistante)."""
        user = _create_test_user(username="sessionuser")

        # Étape 1: Login
        self.client.post("/accounts/connexion/", {
            "username": "sessionuser",
            "password": "SecurePass123!",
        })
        assert "_auth_user_id" in self.client.session

        # Étape 2: Accéder à la page protégée
        response = self.client.get(self.profile_url)

        assert response.status_code == 200
        content = response.content.decode()
        # Vérifier que le profil est affiché (contient au moins le formulaire)
        assert "profil" in content.lower() or "profile" in content.lower()
