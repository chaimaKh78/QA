from playwright.sync_api import Page


class HomePage:
    """Page Object for the NouvelAir homepage."""

    def __init__(self, page: Page):
        self.page = page
        self.url = "/"

    def go_to(self):
        self.page.goto(self.url)
        return self

    def search_flight(self, departure, destination, date):
        self.page.fill('input[name="departure"]', departure)
        self.page.fill('input[name="destination"]', destination)
        self.page.fill('input[name="date"]', date)
        self.page.click('button[type="submit"]')

    def get_title(self):
        return self.page.title()

    def is_loaded(self):
        return self.page.locator("body").is_visible()