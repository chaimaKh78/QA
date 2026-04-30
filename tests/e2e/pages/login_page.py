@'
from playwright.sync_api import Page


class LoginPage:
    """Page Object for the NouvelAir login page."""

    def __init__(self, page: Page):
        self.page = page
        self.url = "/accounts/login/"

    def go_to(self):
        self.page.goto(self.url)
        return self

    def login(self, username, password):
        self.page.fill('input[name="username"]', username)
        self.page.fill('input[name="password"]', password)
        self.page.click('button[type="submit"]')

    def get_error_message(self):
        return self.page.locator(".alert-danger, .errorlist").text_content()
'@ | Set-Content "tests\e2e\pages\login_page.py"