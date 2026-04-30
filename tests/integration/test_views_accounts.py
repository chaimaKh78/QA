"""
Tests d'intégration — Vues de l'application Accounts (10 tests).

Couvre : LoginView, LogoutView, RegisterView, ProfileView.
"""

import pytest
from django.test import Client
from django.urls import reverse
from django.contrib.auth.models import User
from accounts.models import UserProfile


# ── 1. test_login_page ───────────────────────────────────────────────────────


@pytest.mark.integration
@pytest.mark.django_db
def test_login_page(db):
    """GET accounts:login retourne 200 et affiche le formulaire de connexion."""
    client = Client()
    response = client.get(reverse("accounts:login"))
    assert response.status_code == 200
    assert "accounts/login.html" in [t.name for t in response.templates]


# ── 2. test_login_success ────────────────────────────────────────────────────


@pytest.mark.integration
@pytest.mark.django_db
def test_login_success(db, setup_db):
    """POST avec des identifiants valides redirige vers la page d'accueil."""
    client = Client()
    response = client.post(
        reverse("accounts:login"),
        data={
            "username": "testuser",
            "password": "TestPassword123!",
        },
    )
    assert response.status_code == 302
    # La redirection cible la page d'accueil (par défaut)
    assert response.url == reverse("flights:home")


# ── 3. test_login_invalid ────────────────────────────────────────────────────


@pytest.mark.integration
@pytest.mark.django_db
def test_login_invalid(db, setup_db):
    """POST avec un mot de passe invalide renvoie une erreur sur le formulaire."""
    client = Client()
    response = client.post(
        reverse("accounts:login"),
        data={
            "username": "testuser",
            "password": "WrongPassword999!",
        },
    )
    assert response.status_code == 200
    # Le formulaire contient des erreurs
    form = response.context.get("form")
    assert form is not None
    assert form.errors


# ── 4. test_register_page ────────────────────────────────────────────────────


@pytest.mark.integration
@pytest.mark.django_db
def test_register_page(db):
    """GET accounts:register retourne 200 et affiche le formulaire d'inscription."""
    client = Client()
    response = client.get(reverse("accounts:register"))
    assert response.status_code == 200
    assert "accounts/register.html" in [t.name for t in response.templates]


# ── 5. test_register_success ─────────────────────────────────────────────────


@pytest.mark.integration
@pytest.mark.django_db
def test_register_success(db):
    """
    POST avec des données valides crée un nouvel utilisateur, un profil,
    connecte l'utilisateur et redirige vers la page d'accueil.
    """
    client = Client()
    user_count_before = User.objects.count()
    profile_count_before = UserProfile.objects.count()

    response = client.post(
        reverse("accounts:register"),
        data={
            "username": "newuser",
            "first_name": "Nouveau",
            "last_name": "Utilisateur",
            "email": "newuser@example.com",
            "password1": "SecurePass123!",
            "password2": "SecurePass123!",
        },
    )

    # Un nouvel utilisateur et un profil ont été créés
    assert User.objects.count() == user_count_before + 1
    assert UserProfile.objects.count() == profile_count_before + 1

    # L'utilisateur est connecté → redirection vers l'accueil
    assert response.status_code == 302
    assert response.url == reverse("flights:home")

    # Vérifie que le profil est bien associé
    new_user = User.objects.get(username="newuser")
    assert hasattr(new_user, "profile")


# ── 6. test_register_duplicate_email ─────────────────────────────────────────


@pytest.mark.integration
@pytest.mark.django_db
def test_register_duplicate_email(db, setup_db):
    """POST avec un email déjà utilisé renvoie une erreur."""
    client = Client()
    response = client.post(
        reverse("accounts:register"),
        data={
            "username": "anotheruser",
            "first_name": "Autre",
            "last_name": "User",
            "email": "test@example.com",  # email déjà pris par setup_db
            "password1": "SecurePass123!",
            "password2": "SecurePass123!",
        },
    )
    assert response.status_code == 200
    form = response.context.get("form")
    assert form is not None
    assert form.errors
    # L'erreur doit mentionner l'email
    error_text = str(form.errors)
    assert "email" in error_text.lower()


# ── 7. test_logout ───────────────────────────────────────────────────────────


@pytest.mark.integration
@pytest.mark.django_db
def test_logout(db, setup_db):
    """GET accounts:logout déconnecte l'utilisateur et redirige vers l'accueil."""
    client = Client()
    # Connecte d'abord l'utilisateur
    client.login(username="testuser", password="TestPassword123!")

    response = client.get(reverse("accounts:logout"))
    assert response.status_code == 302
    assert response.url == reverse("flights:home")


# ── 8. test_profile_requires_login ───────────────────────────────────────────


@pytest.mark.integration
@pytest.mark.django_db
def test_profile_requires_login(db):
    """GET accounts:profile sans authentification redirige vers la page de connexion."""
    client = Client()
    response = client.get(reverse("accounts:profile"))
    assert response.status_code == 302
    # La redirection doit pointer vers la page de connexion
    assert "/login/" in response.url or "login" in response.url or "connexion" in response.url or "connexion" in response.url


# ── 9. test_profile_authenticated ────────────────────────────────────────────


@pytest.mark.integration
@pytest.mark.django_db
def test_profile_authenticated(db, setup_db):
    """GET accounts:profile avec un utilisateur authentifié retourne 200."""
    client = Client()
    client.login(username="testuser", password="TestPassword123!")
    response = client.get(reverse("accounts:profile"))
    assert response.status_code == 200
    assert "accounts/profile.html" in [t.name for t in response.templates]
    assert "user_form" in response.context
    assert "profile_form" in response.context


# ── 10. test_profile_update ──────────────────────────────────────────────────


@pytest.mark.integration
@pytest.mark.django_db
def test_profile_update(db, setup_db):
    """POST avec des données de profil valides met à jour le profil avec succès."""
    client = Client()
    client.login(username="testuser", password="TestPassword123!")

    response = client.post(
        reverse("accounts:profile"),
        data={
            # UserForm fields
            "first_name": "TestModifié",
            "last_name": "UserModifié",
            "email": "modified@example.com",
            # UserProfileForm fields
            "phone": "+21612345678",
            "address": "123 Rue de la Paix",
            "city": "Tunis",
            "country": "Tunisie",
            "date_of_birth": "1995-06-15",
            "nationality": "Tunisienne",
            "passport_number": "PASS12345",
            "gender": "M",
            "newsletter": "on",
        },
    )
    # Succès → redirection vers la page de profil
    assert response.status_code == 302
    assert response.url == reverse("accounts:profile")

    # Vérifie que les données ont été mises à jour en base
    setup_db["user"].refresh_from_db()
    assert setup_db["user"].first_name == "TestModifié"
    assert setup_db["user"].last_name == "UserModifié"
    assert setup_db["user"].email == "modified@example.com"

    setup_db["profile"].refresh_from_db()
    assert setup_db["profile"].phone == "+21612345678"
    assert setup_db["profile"].city == "Tunis"
    assert setup_db["profile"].newsletter is True
