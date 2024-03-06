import re

from playwright.sync_api import Page, expect, Locator

from pywright.pages.base_page import BasePage


class ListingPage(BasePage):
    URL: str = "/"

    def __init__(self, page: Page) -> None:
        super().__init__(page)

        self.sort_select = self.page.get_by_test_id("sort")

        self.products_container = self.page.locator("app-overview .container")

        self.product_card = self.page.locator(".card")
        self.product_name = self.page.get_by_test_id("product-name")
        self.product_price = self.page.get_by_test_id("product-price")

        self.search_input = self.page.get_by_test_id("search-query")
        self.search_btn = self.page.get_by_test_id("search-submit")
        self.search_reset = self.page.get_by_test_id("search-reset")
        self.search_completed = self.page.get_by_test_id("search_completed")
        self.search_no_results = self.page.get_by_test_id("no-results")

        self.category_filters = self.page.locator("[name*='category_id']")

        self.previous_page = self.page.get_by_label("Previous")
        self.next_page = self.page.get_by_label("Next")
        self.page_item = self.page.locator(".page-item")
        self.active_page = self.page.locator("css=.page-item.active >> css=.page-link")

        self.price_slider_pointers = self.page.locator("span[aria-label^='ngx-slider']")
        self.price_slider_min_pointer = self.page.locator(".ngx-slider-pointer-min")
        self.price_slider_max_pointer = self.page.locator(".ngx-slider-pointer-max")

        self.price_slider_floor = self.page.locator(".ngx-slider-floor")
        self.price_slider_ceil = self.page.locator(".ngx-slider-ceil")

    def load(self):
        self.page.goto(self.URL)
        self.products_container.wait_for()

    def select_sort_option(self, option_value: str) -> None:
        with self.page.expect_response(lambda response: option_value in response.url):
            self.sort_select.select_option(option_value)

    def get_products_name_text(self) -> list[str]:
        self.products_container.wait_for()
        return [text.strip() for text in self.product_name.all_text_contents()]

    def __extract_price_from_text(self, price_text) -> float:
        price = re.findall(r"(?:[\£\$\€]{1})([,\d]+.?\d*)", price_text)[0]
        return float(price)

    def get_products_price_text(self) -> list[float]:
        return [
            self.__extract_price_from_text(price)
            for price in self.product_price.all_text_contents()
        ]

    def search_product(self, product: str) -> None:
        self.search_input.fill(product)
        self.search_btn.click()
        self.page.wait_for_load_state("networkidle")

    def reset_search_product(self, product: str) -> None:
        self.search_input.fill(product)
        self.search_reset.click()

    def verify_search_results(self, search_string: str) -> None:
        expect(self.search_completed).to_be_visible()
        assert all(
            search_string.lower() in name.lower()
            for name in self.get_products_name_text()
        )

    def verify_no_search_results(self) -> None:
        expect(self.search_completed).to_be_visible()
        expect(self.search_no_results).to_be_visible()

    def get_pagination_elements(self) -> list[Locator]:
        pages_count = self.page_item.count()
        pagination_elems = []
        for i in range(pages_count):
            page_elem = self.page_item.nth(i)
            if re.findall(r"\d+", page_elem.text_content()):
                pagination_elems.append(page_elem)

        return pagination_elems

    def click_nth_page_item(self, nth: int) -> None:
        page_num_elem = self.get_pagination_elements()[nth]
        with self.page.expect_response(lambda response: response.url.endswith(f"page={page_num_elem.text_content()}")):
            page_num_elem.click()
        expect(page_num_elem).to_have_class("page-item active")

    def click_next_page(self) -> None:
        previous_selected_page = self.get_active_page_num()
        previous_text_content = self.product_name.first.text_content()

        self.next_page.click()

        expect(self.product_name.first).not_to_have_text(previous_text_content)
        expect(self.active_page).not_to_have_text(previous_selected_page)

    def click_previous_page(self) -> None:
        previous_selected_page = self.get_active_page_num()
        previous_text_content = self.product_name.first.text_content()

        self.previous_page.click()

        expect(self.product_name.first).not_to_have_text(previous_text_content)
        expect(self.active_page).not_to_have_text(previous_selected_page)

    def get_active_page_num(self) -> int:
        return self.active_page.inner_text()

    def move_pointer_to_price_value(self, pointer_locator: Locator, price: int) -> None:
        curr_val = int(pointer_locator.get_attribute("aria-valuenow"))
        pointer_locator.click()

        while price < curr_val:
            self.page.keyboard.press("ArrowLeft")
            curr_val = int(pointer_locator.get_attribute("aria-valuenow"))

        while price > curr_val:
            self.page.keyboard.press("ArrowRight")
            curr_val = int(pointer_locator.get_attribute("aria-valuenow"))

    # TODO: Find a solution with better performance
    def set_price_range(self, min_price: int, max_price: int) -> None:
        if max_price < min_price:
            raise Exception("Cannot set a price range with ")

        curr_min = int(self.price_slider_min_pointer.get_attribute("aria-valuenow"))
        curr_max = int(self.price_slider_max_pointer.get_attribute("aria-valuenow"))
        max_pointer_set = False

        if min_price < curr_min:
            self.move_pointer_to_price_value(self.price_slider_min_pointer, min_price)
        elif min_price > curr_min:
            if min_price < curr_max:
                self.move_pointer_to_price_value(
                    self.price_slider_min_pointer, min_price
                )
            elif min_price > curr_max:
                self.move_pointer_to_price_value(
                    self.price_slider_max_pointer, max_price
                )
                max_pointer_set = True

                self.move_pointer_to_price_value(
                    self.price_slider_min_pointer, min_price
                )

        if not max_pointer_set:
            self.move_pointer_to_price_value(self.price_slider_max_pointer, max_price)

        self.assert_price_pointer_values(min_price, max_price)
        self.page.wait_for_load_state("networkidle")

    def assert_price_pointer_values(
        self, min_pointer_value: int, max_pointer_value: int
    ) -> None:
        expect(self.price_slider_min_pointer).to_have_attribute(
            "aria-valuenow", str(min_pointer_value)
        )
        expect(self.price_slider_max_pointer).to_have_attribute(
            "aria-valuenow", str(max_pointer_value)
        )

    def assert_slider_limits(self, min_limit: int, max_limit: int) -> None:
        expect(self.price_slider_floor).to_have_text(str(min_limit))
        expect(self.price_slider_ceil).to_have_text(str(max_limit))
