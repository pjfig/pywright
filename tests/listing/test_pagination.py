from pywright.pages.listing_page import ListingPage


def test_select_page_num(listing_page: ListingPage):
    products_text = listing_page.get_products_name_text()
    listing_page.click_nth_page_item(-1)

    products_text_after_page_click = listing_page.get_products_name_text()

    assert products_text != products_text_after_page_click


def test_next_previous_page(listing_page: ListingPage):
    products_text = listing_page.get_products_name_text()

    listing_page.click_next_page()
    listing_page.click_previous_page()

    products_text_after_clicks = listing_page.get_products_name_text()

    assert products_text == products_text_after_clicks
