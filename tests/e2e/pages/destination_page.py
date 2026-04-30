"""
Page Object Model – Page des destinations (Jour 6).

Encapsule les interactions avec la page des destinations (/destinations/) :
- Liste des destinations disponibles
- Navigation vers le détail d'une destination
"""

from playwright.sync_api import Locator
from .base_page import BasePage


class DestinationPage(BasePage):
    """
    Page Object pour la page des destinations de NouvelAir.

    Fournit des méthodes pour parcourir la liste des destinations
    et naviguer vers la page de détail d'une destination.

    Attributes:
        url (str): chemin relatif de la page des destinations.
    """

    url = "/destinations/"

    def get_destination_cards(self) -> list:
        """
        Retourne la liste de toutes les cartes de destination affichées.

        Returns:
            list: liste des locators correspondant aux cartes de destination.
        """
        return self.page.locator(
            ".destination-card, .dest-card, [class*='destination']"
        ).all()

    def get_first_destination(self) -> Locator:
        """
        Retourne le locator de la première carte de destination.

        Returns:
            Locator: locator de la première carte de destination.
        """
        return self.page.locator(
            ".destination-card, .dest-card, [class*='destination']"
        ).first

    def click_destination(self, slug: str) -> None:
        """
        Navigue vers la page de détail d'une destination spécifique.

        Args:
            slug: slug de la destination (ex: 'paris', 'tunis').
        """
        self.page.click(f"a[href*='/destinations/{slug}/']")
