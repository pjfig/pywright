from playwright.sync_api import Page


class BasePage:
    URL: str

    def __init__(self, page: Page) -> None:
        self.page = page

    def load(self):
        self.page.goto(self.URL)
