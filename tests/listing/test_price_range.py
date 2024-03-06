from playwright.sync_api import expect
from pywright.pages.listing_page import ListingPage


def test_price_range_limits(listing_page: ListingPage):
    listing_page.assert_slider_limits(0, 200)


def test_price_range_with_products(listing_page: ListingPage):
    listing_page.set_price_range(30, 60)
    prices = listing_page.get_products_price_text()
    assert all(30.0 <= price <= 60.0 for price in prices)


def test_price_range_without_products(listing_page: ListingPage):
    listing_page.set_price_range(105, 115)
    expect(listing_page.search_no_results).to_be_visible()
    expect(listing_page.product_card.first).not_to_be_visible()
