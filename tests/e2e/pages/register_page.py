"""
Page Object Model – Page d'inscription (Jour 6).

Encapsule les interactions avec la page d'inscription (/accounts/register/) :
- Remplissage du formulaire d'inscription
- Soumission et validation
"""

from .base_page import BasePage


class RegisterPage(BasePage):
    """
    Page Object pour la page d'inscription de NouvelAir.

    Fournit des méthodes pour remplir le formulaire d'inscription
    avec toutes les informations requises et le soumettre.

    Attributes:
        url (str): chemin relatif de la page d'inscription.
    """

    url = "/accounts/register/"

    def fill_form(
        self,
        username: str,
        email: str,
        password1: str,
        password2: str,
    ) -> None:
        """
        Remplit tous les champs du formulaire d'inscription.

        Args:
            username: nom d'utilisateur souhaité.
            email: adresse email.
            password1: mot de passe.
            password2: confirmation du mot de passe.
        """
        self.fill("input#id_username, input[name='username']", username)
        self.fill("input#id_email, input[name='email']", email)
        self.fill("input#id_password1, input[name='password1']", password1)
        self.fill("input#id_password2, input[name='password2']", password2)

    def submit(self) -> None:
        """
        Soumet le formulaire d'inscription.
        """
        submit_btn = self.page.locator(
            "button[type='submit'], input[type='submit'], "
            "form button:has-text('Inscription'), form button:has-text('Register'), "
            "form button:has-text('S\'inscrire')"
        )
        submit_btn.click()
