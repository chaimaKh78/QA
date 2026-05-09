from __future__ import annotations

from datetime import date
from playwright.sync_api import Page

from pages.base_page import BasePage


class HomePage(BasePage):
    """Page Object Model pour la page d'accueil (formulaire de recherche)."""

    url = "/"

    # Sélecteurs (essayent plusieurs variantes pour être robuste)
    _FORM_SELECTOR = "form"

    _ORIGIN_SELECT = "select[name='origin'], select[name='from'], select#origin, #origin"
    _DEST_SELECT = "select[name='destination'], select[name='to'], select#destination, #destination"

    _TRIP_TYPE = "select[name='trip_type'], select[name='tripType'], input[name='trip_type']"

    _DEPARTURE_DATE = "input[name='departure_date'], input[name='departureDate'], #departure_date"
    _RETURN_DATE = "input[name='return_date'], input[name='returnDate'], #return_date"

    _PASSENGERS = "input[name='passengers'], select[name='passengers'], #passengers"

    _SUBMIT = "form button[type='submit'], button[type='submit'], button:has-text('Search'), button:has-text('Rechercher')"

    def __init__(self, page: Page, base_url: str):
        super().__init__(page, base_url)

    def _select_option_by_code(self, select_locator: str, code: str) -> None:
        self.page.wait_for_selector(select_locator, timeout=5000)

        options = self.page.locator(f"{select_locator} option")
        count = options.count()
        code_norm = code.strip().upper()

        for i in range(count):
            opt = options.nth(i)
            opt_text = (opt.inner_text() or "").strip().upper()
            opt_value = (opt.get_attribute("value") or "").strip().upper()

            # Ignorer les options "placeholder" vides
            if not opt_text and not opt_value:
                continue

            # Matches:
            # - valeur = code
            # - texte = code
            # - texte contient "CODE -" / "CODE " / "(CODE)"
            if opt_value == code_norm:
                self.page.select_option(select_locator, opt_value)
                return

            if opt_text == code_norm or opt_text.startswith(f"{code_norm} ") or opt_text.startswith(f"{code_norm}-"):
                # select_option attend une valeur de l'option; si la valeur est vide,
                # on ne peut pas l'utiliser -> fallback sur valeur = code_norm
                self.page.select_option(select_locator, opt_value if opt_value else code_norm)
                return

            if f"{code_norm} -" in opt_text or f"({code_norm})" in opt_text or f" {code_norm} " in opt_text:
                self.page.select_option(select_locator, opt_value if opt_value else code_norm)
                return

        # Debug utile: liste les options disponibles pour comprendre pourquoi TUN manque
        available = []
        for i in range(count):
            opt = options.nth(i)
            available.append({
                "text": (opt.inner_text() or "").strip(),
                "value": opt.get_attribute("value"),
            })

        raise ValueError(
            f"Aéroport '{code}' introuvable dans la liste (locateur: {select_locator}). "
            f"Options détectées: {available[:20]}"
        )


    def select_origin(self, code: str) -> None:
        self._select_option_by_code(self._ORIGIN_SELECT, code)

    def select_destination(self, code: str) -> None:
        self._select_option_by_code(self._DEST_SELECT, code)

    def select_trip_type(self, trip_type: str) -> None:
        # Optionnel (si absent, pas bloquant)
        try:
            self.page.wait_for_selector(self._TRIP_TYPE, timeout=2000)
        except Exception:
            return

        trip_norm = trip_type.strip().lower()
        # Sélection flexible par value ou texte
        locator = self.page.locator(f"{self._TRIP_TYPE} option")
        for i in range(locator.count()):
            opt = locator.nth(i)
            txt = (opt.inner_text() or "").strip().lower()
            val = (opt.get_attribute('value') or '').strip().lower()
            if trip_norm in txt or trip_norm in val:
                chosen = opt.get_attribute('value')
                if chosen:
                    self.page.select_option(self._TRIP_TYPE, chosen)
                else:
                    # fallback: selection par texte via valeur vide n'est pas possible,
                    # donc on sélectionne par valeur si possible.
                    self.page.select_option(self._TRIP_TYPE, opt.get_attribute('value'))
                return

    def set_departure_date(self, value: str) -> None:
        self.page.wait_for_selector(self._DEPARTURE_DATE, timeout=5000)
        self.page.fill(self._DEPARTURE_DATE, value)

    def set_return_date(self, value: str) -> None:
        # retour optionnel
        try:
            self.page.wait_for_selector(self._RETURN_DATE, timeout=2000)
        except Exception:
            return
        self.page.fill(self._RETURN_DATE, value)

    def set_passengers(self, count: int) -> None:
        self.page.wait_for_selector(self._PASSENGERS, timeout=5000)
        # gère input ou select
        tag_name = self.page.eval_on_selector(self._PASSENGERS, "el => el.tagName")
        if (tag_name or "").upper() == "SELECT":
            self.page.select_option(self._PASSENGERS, str(count))
        else:
            self.page.fill(self._PASSENGERS, str(count))

    def submit_search(self) -> None:
        # Attend le bouton submit ou un submit via Enter
        self.page.wait_for_selector(self._FORM_SELECTOR, timeout=5000)
        if self.page.locator(self._SUBMIT).count() > 0:
            self.page.click(self._SUBMIT)
        else:
            self.page.locator(self._FORM_SELECTOR).press("Enter")

