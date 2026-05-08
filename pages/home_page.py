"""
Page Object Model – Page d'accueil (Jour 6).

Encapsule les interactions avec la page d'accueil de NouvelAir :
- Sélection des aéroports (origine, destination) via champs select
- Choix des dates (aller, retour)
- Sélection du nombre de passagers et classe
- Type de voyage (aller simple / aller-retour)
- Soumission du formulaire de recherche
"""

from playwright.sync_api import Page
from .base_page import BasePage


class HomePage(BasePage):
    """Page Object for the NouvelAir homepage."""

    url = "/"

    def __init__(self, page: Page, base_url: str):
        super().__init__(page, base_url)

    # -------------------------------------------------------------------------
    # Sélecteurs des champs du formulaire (conforme au template Django)
    # -------------------------------------------------------------------------

    _ORIGIN_SELECT = 'select[name="origin"]'
    _DESTINATION_SELECT = 'select[name="destination"]'
    _DEPARTURE_DATE_INPUT = 'input[name="departure_date"]'
    _RETURN_DATE_INPUT = 'input[name="return_date"]'
    _PASSENGERS_INPUT = 'input[name="passengers"]'
    _TRAVEL_CLASS_SELECT = 'select[name="travel_class"]'
    _TRIP_TYPE_RADIO = 'input[name="trip_type"]'
    _SUBMIT_BUTTON = 'button[type="submit"]'

    # -------------------------------------------------------------------------
    # Actions du formulaire
    # -------------------------------------------------------------------------

    def select_origin(self, code: str) -> None:
        """
        Sélectionne l'aéroport d'origine par code IATA (ex: 'TUN').

        Le widget est un <select> dont les options affichent le texte
        « CODE - Ville (Pays) ». On sélectionne l'option dont le texte
        commence par le code fourni.
        """
        # Cherche une option dont le texte commence par le code (ex: "TUN - ...")
        options = self.page.locator(f"{self._ORIGIN_SELECT} option")
        count = options.count()
        for i in range(count):
            opt_text = options.nth(i).inner_text().strip()
            if opt_text.startswith(code + " "):
                # Get the value attribute and call select_option on the select element
                opt_value = options.nth(i).get_attribute("value")
                self.page.select_option(self._ORIGIN_SELECT, opt_value)
                return
        raise ValueError(f"Aéroport origine '{code}' introuvable dans la liste.")

    def select_destination(self, code: str) -> None:
        """Sélectionne l'aéroport de destination par code IATA."""
        options = self.page.locator(f"{self._DESTINATION_SELECT} option")
        count = options.count()
        for i in range(count):
            opt_text = options.nth(i).inner_text().strip()
            if opt_text.startswith(code + " "):
                # Get the value attribute and call select_option on the select element
                opt_value = options.nth(i).get_attribute("value")
                self.page.select_option(self._DESTINATION_SELECT, opt_value)
                return
        raise ValueError(f"Aéroport destination '{code}' introuvable dans la liste.")

    def set_departure_date(self, date_str: str) -> None:
        """Définit la date de départ (format YYYY-MM-DD)."""
        self.fill(self._DEPARTURE_DATE_INPUT, date_str)

    def set_return_date(self, date_str: str) -> None:
        """Définit la date de retour (format YYYY-MM-DD). Ignoré si champ absent."""
        try:
            self.fill(self._RETURN_DATE_INPUT, date_str)
        except Exception:
            pass  # Champ optionnel pour les allers simples

    def set_passengers(self, count: int) -> None:
        """Définit le nombre de passagers (1-9)."""
        self.fill(self._PASSENGERS_INPUT, str(count))

    def set_travel_class(self, travel_class: str = "economy") -> None:
        """
        Définit la classe de voyage.

        Args:
            travel_class: 'economy' ou 'business'.
        """
        self.page.select_option(self._TRAVEL_CLASS_SELECT, label=travel_class.capitalize())

    def select_trip_type(self, trip_type: str) -> None:
        """
        Sélectionne le type de trajet.

        Args:
            trip_type: "oneway" ou "roundtrip".
        """
        value = "oneway" if trip_type == "oneway" else "roundtrip"
        self.page.check(f'{self._TRIP_TYPE_RADIO}[value="{value}"]')

    def submit_search(self) -> None:
        """Soumet le formulaire de recherche."""
        self.click(self._SUBMIT_BUTTON)
