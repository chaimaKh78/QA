"""
Page Object Model – Page de résultats de recherche (Jour 6).

Encapsule les interactions avec la page de résultats de recherche de vols :
- Liste des vols trouvés
- Filtres et tri
- Message d'absence de résultats
"""

from playwright.sync_api import Locator
from .base_page import BasePage


class SearchResultsPage(BasePage):
    """
    Page Object pour la page de résultats de recherche de vols.

    Fournit des méthodes pour accéder aux résultats de vol,
    vérifier la présence de résultats et interagir avec les filtres.

    Attributes:
        url (str): chemin relatif de la page de résultats.
    """

    url = "/flights/search/"

    def get_flight_cards(self) -> list:
        """
        Retourne la liste de toutes les cartes de résultats de vol.

        Returns:
            list: liste des locators correspondant aux cartes de vol.
        """
        return self.page.locator(".flight-result, .flight-card, .search-result, [class*='flight-result'], [class*='vol-result']").all()

    def get_first_flight(self) -> Locator:
        """
        Retourne le locator du premier résultat de vol.

        Returns:
            Locator: locator de la première carte de résultat.
        """
        return self.page.locator(".flight-result, .flight-card, .search-result, [class*='flight-result']").first

    def has_results(self) -> bool:
        """
        Vérifie si la page affiche des résultats de vol.

        Returns:
            bool: True si au moins un résultat est affiché, False sinon.
        """
        return len(self.get_flight_cards()) > 0

    def get_no_results_message(self) -> str:
        """
        Retourne le texte du message affiché quand aucun résultat n'est trouvé.

        Returns:
            str: texte du message d'absence de résultats.
        """
        no_results = self.page.locator(".no-results, .empty-state, [class*='no-result'], p:has-text('Aucun'), p:has-text('aucun')")
        if no_results.count() > 0:
            return no_results.first.text_content()
        return ""

    def get_filters(self) -> Locator:
        """
        Retourne le locator des contrôles de filtre sur la page de résultats.

        Returns:
            Locator: locator de la section filtres.
        """
        return self.page.locator(".filters, .search-filters, aside, [class*='filter'], [class*='filtre']")
