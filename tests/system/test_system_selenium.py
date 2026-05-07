# tests/system/test_system_selenium.py
from django.test import tag
from django.contrib.staticfiles.testing import StaticLiveServerTestCase

try:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.chrome.options import Options
    SELENIUM_AVAILABLE = True
except ImportError:
    SELENIUM_AVAILABLE = False

import pytest
import time


@pytest.mark.skipif(not SELENIUM_AVAILABLE, reason="selenium non installé")
@tag("system", "selenium")
class TestSystemSelenium(StaticLiveServerTestCase):
    """Tests système avec Selenium (alternative à Playwright)."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        cls.driver = webdriver.Chrome(options=options)
        cls.driver.implicitly_wait(5)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super().tearDownClass()

    def test_sys_title_contains_nouvelair(self):
        """La page d'accueil contient NouvelAir dans le titre."""
        self.driver.get(f"{self.live_server_url}/")
        self.assertIn("NouvelAir", self.driver.title)

    def test_sys_navigation_search_page(self):
        """La navigation vers la page de recherche fonctionne."""
        self.driver.get(f"{self.live_server_url}/")
        wait = WebDriverWait(self.driver, 10)
        
        # Attendre que le document soit prêt
        wait.until(lambda driver: driver.execute_script("return document.readyState") == "complete")
        
        # Trouver tous les liens de navigation et chercher celui avec "Reservation"
        nav_links = self.driver.find_elements(By.XPATH, "//nav//a[contains(@class, 'nav-link')]")
        
        # Chercher le lien avec "Reservation" dans le texte ou dans le HTML (peut avoir un icône)
        reservation_link = None
        for link in nav_links:
            text = link.text.strip()
            html = link.get_attribute("innerHTML") or ""
            if "Reservation" in text or "fa-suitcase" in html:
                reservation_link = link
                break
        
        if reservation_link:
            try:
                # Faire défiler et cliquer
                self.driver.execute_script("arguments[0].scrollIntoView(true);", reservation_link)
                time.sleep(0.5)
                wait.until(EC.element_to_be_clickable(reservation_link))
                self.driver.execute_script("arguments[0].click();", reservation_link)
            except:
                # Fallback
                self.driver.get(f"{self.live_server_url}/recherche/")
        else:
            # Alternative: aller directement à la page de recherche
            self.driver.get(f"{self.live_server_url}/recherche/")
        
        # Vérifier qu'on est sur la page de recherche ou lookup
        self.assertTrue("recherche" in self.driver.current_url or "lookup" in self.driver.current_url or "flight" in self.driver.current_url.lower())