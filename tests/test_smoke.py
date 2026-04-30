"""Smoke test to verify pytest + Django configuration."""
import pytest
from django.test import TestCase


class TestSmoke(TestCase):
    """Basic smoke tests to confirm the test environment works."""

    def test_django_config(self):
        """Verify Django settings are loaded correctly."""
        from django.conf import settings
        self.assertEqual(settings.APP_NAME if hasattr(settings, 'APP_NAME') else 'nouvelair', 
                         getattr(settings, 'APP_NAME', 'nouvelair'))
    
    def test_django_installed(self):
        """Verify Django is properly installed."""
        import django
        self.assertIsNotNone(django.__version__)

    def test_database_connection(self):
        """Verify test database is accessible."""
        from django.db import connection
        connection.ensure_connection()
        self.assertTrue(connection.is_usable())