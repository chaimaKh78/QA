"""
Page Object Model – Classe de base (Jour 6).

Classe abstraite BasePage servant de fondation à toutes les Page Objects.
Encapsule les opérations de navigation et d'interaction communes
à toutes les pages de l'application NouvelAir.
"""

from playwright.sync_api import Page


class BasePage:
    """
    Classe de base pour le pattern Page Object Model.

    Fournit les méthodes génériques de navigation, d'attente,
    d'interaction et de capture d'écran utilisées par toutes les pages.

    Attributes:
        page (Page): instance de page Playwright.
        base_url (str): URL de base de l'application.
    """

    def __init__(self, page: Page, base_url: str = "http://127.0.0.1:8000"):
        """
        Initialise la page de base avec la page Playwright et l'URL de base.

        Args:
            page: instance de page Playwright (sync API).
            base_url: URL de base de l'application NouvelAir.
        """
        self.page = page
        self.base_url = base_url

    def navigate(self, url_path: str) -> None:
        """
        Navigue vers une URL relative à la base de l'application.

        Args:
            url_path: chemin relatif (ex: '/', '/accounts/login/').
        """
        full_url = f"{self.base_url}{url_path}"
        self.page.goto(full_url, wait_until="domcontentloaded")

    def get_title(self) -> str:
        """
        Retourne le titre de la page courante.

        Returns:
            str: titre de la page (<title>).
        """
        return self.page.title()

    def get_text(self, selector: str) -> str:
        """
        Retourne le texte contenu dans l'élément trouvé par le sélecteur.

        Args:
            selector: sélecteur CSS ou texte.

        Returns:
            str: texte intérieur de l'élément.

        Raises:
            Exception: si l'élément n'est pas trouvé.
        """
        return self.page.locator(selector).first.text_content()

    def click(self, selector: str) -> None:
        """
        Clique sur l'élément trouvé par le sélecteur.

        Attend automatiquement que l'élément soit visible et cliquable.

        Args:
            selector: sélecteur CSS, texte ou rôle de l'élément.
        """
        self.page.click(selector)

    def fill(self, selector: str, value: str) -> None:
        """
        Remplit un champ de formulaire avec la valeur donnée.

        Args:
            selector: sélecteur CSS ou nom du champ.
            value: valeur à saisir.
        """
        self.page.fill(selector, value)

    def wait_for_selector(self, selector: str, timeout: int = 10000) -> None:
        """
        Attend que l'élément correspondant au sélecteur soit attaché au DOM.

        Args:
            selector: sélecteur CSS de l'élément attendu.
            timeout: temps maximal d'attente en millisecondes (défaut: 10000).
        """
        self.page.wait_for_selector(selector, timeout=timeout)

    def wait_for_url(self, url_pattern: str, timeout: int = 10000) -> None:
        """
        Attend que l'URL de la page corresponde au motif donné.

        Args:
            url_pattern: motif de l'URL attendu (peut être une regex ou substring).
            timeout: temps maximal d'attente en millisecondes (défaut: 10000).
        """
        self.page.wait_for_url(url_pattern, timeout=timeout)

    def screenshot(self, filename: str) -> None:
        """
        Capture une capture d'écran complète de la page.

        Le fichier est sauvegardé dans test-results/screenshots/.

        Args:
            filename: nom du fichier de capture (ex: 'homepage.png').
        """
        import os
        screenshots_dir = os.path.join("test-results", "screenshots")
        os.makedirs(screenshots_dir, exist_ok=True)
        filepath = os.path.join(screenshots_dir, filename)
        self.page.screenshot(path=filepath, full_page=True)

    def is_element_visible(self, selector: str) -> bool:
        """
        Vérifie si un élément est visible sur la page.

        Args:
            selector: sélecteur CSS ou texte de l'élément.

        Returns:
            bool: True si l'élément est visible, False sinon.
        """
        return self.page.locator(selector).first.is_visible()

    def get_element_count(self, selector: str) -> int:
        """
        Retourne le nombre d'éléments correspondant au sélecteur.

        Args:
            selector: sélecteur CSS.

        Returns:
            int: nombre d'éléments trouvés.
        """
        return self.page.locator(selector).count()
