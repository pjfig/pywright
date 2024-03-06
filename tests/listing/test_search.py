from playwright.sync_api import expect

from pywright.pages.listing_page import ListingPage


def test_full_name(listing_page: ListingPage):
    listing_page.search_product("thor hammer")
    listing_page.verify_search_results("thor hammer")


def test_partial_name(listing_page: ListingPage):
    listing_page.search_product("hammer")
    listing_page.verify_search_results("hammer")


def test_cancel_search(listing_page: ListingPage):
    products_before_search = listing_page.get_products_name_text()
    listing_page.reset_search_product("hammer")
    products = listing_page.get_products_name_text()

    expect(listing_page.search_input).to_have_text("")
    assert products == products_before_search


def test_empty_name(listing_page: ListingPage):
    products_before_search = listing_page.get_products_name_text()

    listing_page.search_product("")
    products_name = listing_page.get_products_name_text()

    assert products_before_search == products_name


def test_non_existing_name(listing_page: ListingPage):
    listing_page.search_product("error")

    expect(listing_page.search_completed).to_be_visible()
    expect(listing_page.search_no_results).to_be_visible()
