"""
Page Object Model – Page des réservations (Jour 6).

Encapsule les interactions avec la page Mes réservations (/bookings/my-bookings/) :
- Liste des réservations de l'utilisateur
- Vérification de la présence de réservations
- Détails d'une réservation
"""

from playwright.sync_api import Locator
from .base_page import BasePage


class BookingPage(BasePage):
    """
    Page Object pour la page "Mes réservations" de NouvelAir.

    Fournit des méthodes pour accéder à la liste des réservations
    d'un utilisateur authentifié et vérifier leur présence.

    Attributes:
        url (str): chemin relatif de la page Mes réservations.
    """

    url = "/bookings/my-bookings/"

    def get_bookings(self) -> list:
        """
        Retourne la liste des cartes de réservation affichées.

        Returns:
            list: liste des locators correspondant aux cartes de réservation.
        """
        return self.page.locator(
            ".booking-card, .reservation-card, .booking-item, "
            "[class*='booking'], [class*='reservation']"
        ).all()

    def has_bookings(self) -> bool:
        """
        Vérifie si au moins une réservation est affichée.

        Returns:
            bool: True si des réservations sont présentes, False sinon.
        """
        return len(self.get_bookings()) > 0
