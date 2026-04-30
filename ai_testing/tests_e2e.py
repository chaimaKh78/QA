"""
NouvelAir - Tests de bout en bout (E2E) avec Selenium.
========================================================

Ce module contient les tests E2E automatisés qui simulent des parcours
utilisateur complets dans l'application NouvelAir.

Prérequis:
    pip install selenium webdriver-manager

Usage:
    python manage.py test ai_testing.tests_e2e
"""

import os
import sys
import unittest
import time
from django.test import LiveServerTestCase, TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

# Si Selenium n'est pas disponible, on saute les tests E2E
try:
    from selenium import webdriver
    SELENIUM_AVAILABLE = True
except ImportError:
    SELENIUM_AVAILABLE = False


@unittest.skipUnless(SELENIUM_AVAILABLE, "Selenium non installé")
class E2EHomeAndSearchTest(LiveServerTestCase):
    """
    Test E2E: Parcours complet depuis la page d'accueil jusqu'à la recherche.
    """

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        cls.driver = webdriver.Chrome(options=chrome_options)
        cls.driver.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super().tearDownClass()

    def test_home_page_loads(self):
        """Vérifie que la page d'accueil se charge correctement."""
        self.driver.get(self.live_server_url)
        self.assertIn('NouvelAir', self.driver.title)

    def test_navigation_links(self):
        """Vérifie que les liens de navigation fonctionnent."""
        self.driver.get(self.live_server_url)

        # Vérifier le lien Destinations
        destinations_link = self.driver.find_element(By.LINK_TEXT, 'Destinations')
        destinations_link.click()
        WebDriverWait(self.driver, 10).until(
            EC.title_contains('Destinations')
        )

        # Vérifier le lien Offres
        self.driver.get(self.live_server_url)
        offres_link = self.driver.find_element(By.LINK_TEXT, 'Offres')
        offres_link.click()

    def test_flight_search_form_present(self):
        """Vérifie la présence du formulaire de recherche de vols."""
        self.driver.get(self.live_server_url)

        # Vérifier que le formulaire existe
        form = self.driver.find_element(By.CSS_SELECTOR, '.search-card')
        self.assertIsNotNone(form)

        # Vérifier les champs
        origin_select = self.driver.find_element(By.ID, 'origin-select')
        destination_select = self.driver.find_element(By.ID, 'destination-select')
        self.assertIsNotNone(origin_select)
        self.assertIsNotNone(destination_select)


@unittest.skipUnless(SELENIUM_AVAILABLE, "Selenium non installé")
class E2EAuthenticationTest(LiveServerTestCase):
    """Test E2E: Parcours d'inscription et connexion."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        cls.driver = webdriver.Chrome(options=chrome_options)
        cls.driver.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super().tearDownClass()

    def test_registration_flow(self):
        """Test le flux d'inscription complet."""
        self.driver.get(f"{self.live_server_url}{reverse('accounts:register')}")

        # Remplir le formulaire
        self.driver.find_element(By.NAME, 'username').send_keys('e2e_user')
        self.driver.find_element(By.NAME, 'email').send_keys('e2e@example.com')
        self.driver.find_element(By.NAME, 'first_name').send_keys('E2E')
        self.driver.find_element(By.NAME, 'last_name').send_keys('Test')
        self.driver.find_element(By.NAME, 'password1').send_keys('SecurePass123!')
        self.driver.find_element(By.NAME, 'password2').send_keys('SecurePass123!')

        # Soumettre
        submit = self.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
        submit.click()

        # Vérifier la redirection
        WebDriverWait(self.driver, 10).until(
            EC.url_contains('/')
        )

    def test_login_flow(self):
        """Test le flux de connexion."""
        # Créer un utilisateur
        User.objects.create_user('login_test', 'login@example.com', 'TestPass123!')

        self.driver.get(f"{self.live_server_url}{reverse('accounts:login')}")

        self.driver.find_element(By.NAME, 'username').send_keys('login_test')
        self.driver.find_element(By.NAME, 'password').send_keys('TestPass123!')

        submit = self.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
        submit.click()

        WebDriverWait(self.driver, 10).until(
            EC.url_contains('/')
        )

    def test_logout_flow(self):
        """Test le flux de déconnexion."""
        user = User.objects.create_user('logout_test', 'logout@example.com', 'TestPass123!')

        # Se connecter d'abord
        self.client.force_login(user)
        cookie = self.client.cookies['sessionid']
        self.driver.add_cookie({
            'name': 'sessionid',
            'value': cookie.value,
            'path': '/',
            'domain': self.live_server_url.split('//')[1].split(':')[0]
        })

        self.driver.get(f"{self.live_server_url}{reverse('accounts:logout')}")
        WebDriverWait(self.driver, 10).until(
            EC.url_contains('/')
        )


@unittest.skipUnless(SELENIUM_AVAILABLE, "Selenium non installé")
class E2EBookingTest(LiveServerTestCase):
    """Test E2E: Parcours de réservation."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        cls.driver = webdriver.Chrome(options=chrome_options)
        cls.driver.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super().tearDownClass()

    def test_booking_lookup_page(self):
        """Test la page de recherche de réservation."""
        self.driver.get(f"{self.live_server_url}{reverse('bookings:lookup')}")
        self.assertIn('Retrouvez', self.driver.page_source)
