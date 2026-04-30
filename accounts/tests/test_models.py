"""
Tests unitaires pour l'application Accounts.
"""

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from accounts.models import UserProfile


class AccountModelTest(TestCase):
    """Tests du modèle UserProfile."""

    def test_profile_auto_creation(self):
        """Vérifie que le profil est créé automatiquement avec l'utilisateur."""
        user = User.objects.create_user(
            username='testuser', password='testpass123',
            email='test@example.com'
        )
        self.assertTrue(hasattr(user, 'profile'))
        self.assertEqual(user.profile.user, user)

    def test_profile_full_name(self):
        """Vérifie la propriété full_name."""
        user = User.objects.create_user(
            username='testuser', password='testpass123',
            first_name='Mohamed', last_name='Ali'
        )
        self.assertEqual(user.profile.full_name, 'Mohamed Ali')

    def test_profile_without_full_name(self):
        """Vérifie le fallback sur le username."""
        user = User.objects.create_user(
            username='testuser2', password='testpass123'
        )
        self.assertEqual(user.profile.full_name, 'testuser2')

    def test_booking_count(self):
        """Vérifie le compteur de réservations."""
        user = User.objects.create_user(
            username='testuser3', password='testpass123'
        )
        self.assertEqual(user.profile.booking_count, 0)


class AccountViewTest(TestCase):
    """Tests des vues de l'application Accounts."""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser', password='testpass123',
            email='test@example.com', first_name='Test', last_name='User'
        )

    def test_register_page(self):
        """Vérifie l'accès à la page d'inscription."""
        response = self.client.get(reverse('accounts:register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/register.html')

    def test_register_success(self):
        """Vérifie l'inscription réussie."""
        response = self.client.post(reverse('accounts:register'), {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'first_name': 'New',
            'last_name': 'User',
            'password1': 'SecurePass123!',
            'password2': 'SecurePass123!',
        })
        self.assertEqual(User.objects.count(), 2)
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_register_duplicate_email(self):
        """Vérifie qu'on ne peut pas utiliser un email en doublon."""
        response = self.client.post(reverse('accounts:register'), {
            'username': 'newuser',
            'email': 'test@example.com',
            'first_name': 'New',
            'last_name': 'User',
            'password1': 'SecurePass123!',
            'password2': 'SecurePass123!',
        })
        self.assertEqual(User.objects.count(), 1)

    def test_login_page(self):
        """Vérifie l'accès à la page de connexion."""
        response = self.client.get(reverse('accounts:login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/login.html')

    def test_login_success(self):
        """Vérifie la connexion réussie."""
        response = self.client.post(reverse('accounts:login'), {
            'username': 'testuser',
            'password': 'testpass123',
        })
        self.assertEqual(response.status_code, 302)

    def test_login_invalid(self):
        """Vérifie l'échec de connexion avec mauvais mot de passe."""
        response = self.client.post(reverse('accounts:login'), {
            'username': 'testuser',
            'password': 'wrongpassword',
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'valides')

    def test_logout(self):
        """Vérifie la déconnexion."""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('accounts:logout'))
        self.assertEqual(response.status_code, 302)

    def test_profile_requires_login(self):
        """Vérifie que le profil nécessite une connexion."""
        response = self.client.get(reverse('accounts:profile'))
        self.assertEqual(response.status_code, 302)

    def test_profile_authenticated(self):
        """Vérifie l'accès au profil quand connecté."""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('accounts:profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/profile.html')

    def test_profile_update(self):
        """Vérifie la mise à jour du profil."""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(reverse('accounts:profile'), {
            'first_name': 'Updated',
            'last_name': 'Name',
            'email': 'updated@example.com',
            'phone': '+21612345678',
        })
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, 'Updated')

    def test_authenticated_user_redirected_from_register(self):
        """Vérifie la redirection si déjà connecté."""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('accounts:register'))
        self.assertEqual(response.status_code, 302)
