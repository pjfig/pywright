import pytest
from playwright.sync_api import Playwright, Page

from pywright.pages.listing_page import ListingPage


@pytest.fixture(scope="session", autouse=True)
def define_data_test(playwright: Playwright):
    playwright.selectors.set_test_id_attribute("data-test")


@pytest.fixture
def listing_page(page: Page):
    listing_page = ListingPage(page)
    listing_page.load()
    return ListingPage(page)
