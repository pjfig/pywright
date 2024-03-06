import pytest

from pywright.pages.listing_page import ListingPage


@pytest.fixture(autouse=True)
def skip_filter_tests():
    pytest.skip(
        "Filter tests not ready yet, as this functionality is not yet implemented"
    )


def test_category_single_selection(listing_page: ListingPage):
    pass


def test_category_multiple_selection(listing_page: ListingPage):
    pass


def test_category_brand_filter_selection(listing_page: ListingPage):
    pass
