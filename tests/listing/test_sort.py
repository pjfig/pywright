from pywright.pages.listing_page import ListingPage


def test_sort_by_name_asc(listing_page: ListingPage):
    listing_page.select_sort_option("name,asc")
    products_name = listing_page.get_products_name_text()
    assert sorted(products_name) == products_name


def test_sort_by_name_desc(listing_page: ListingPage):
    listing_page.select_sort_option("name,desc")
    products_name = listing_page.get_products_name_text()
    assert sorted(products_name, reverse=True) == products_name


def test_sort_by_price_asc(listing_page: ListingPage):
    listing_page.select_sort_option("price,asc")
    products_price = listing_page.get_products_price_text()
    assert sorted(products_price) == products_price


def test_sort_by_price_desc(listing_page: ListingPage):
    listing_page.select_sort_option("price,desc")
    products_price = listing_page.get_products_price_text()
    assert sorted(products_price, reverse=True) == products_price
