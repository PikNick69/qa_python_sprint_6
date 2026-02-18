import allure
import pytest
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.home_page import HomePage
from pages.order_page import OrderPage
from data.test_data import ORDER_DATA


@allure.epic("Тестирование сервиса 'Яндекс.Самокат'")
@allure.feature("Оформление заказа")
class TestOrder:
    @pytest.mark.order
    @allure.title("Позитивный сценарий заказа самоката")
    @pytest.mark.parametrize("order_data", ORDER_DATA)
    def test_successful_order(self, driver, order_data):
        home_page = HomePage(driver)
        home_page.close_cookie_banner()
        
        home_page.click_top_order_button()
        WebDriverWait(driver, 10).until(EC.url_contains("order"))
        
        order_page = OrderPage(driver)
        order_page.fill_first_form(
            order_data["name"], order_data["surname"], order_data["address"],
            order_data["metro"], order_data["phone"]
        )
        order_page.click_next()
        order_page.fill_second_form(
            order_data["delivery_date"], order_data["rental_period_index"],
            order_data["color"], order_data["comment"]
        )
        order_page.confirm_order()
        assert order_page.is_order_successful()

    @pytest.mark.order
    @allure.title("Оформление заказа через нижнюю кнопку 'Заказать'")
    def test_order_via_bottom_button(self, driver):
        home_page = HomePage(driver)
        home_page.close_cookie_banner()
        test_data = ORDER_DATA[0]
        
        home_page.click_bottom_order_button()
        WebDriverWait(driver, 10).until(EC.url_contains("order"))
        
        order_page = OrderPage(driver)
        order_page.fill_first_form(
            test_data["name"], test_data["surname"], test_data["address"],
            test_data["metro"], test_data["phone"]
        )
        order_page.click_next()
        order_page.fill_second_form(
            test_data["delivery_date"], test_data["rental_period_index"],
            test_data["color"], test_data["comment"]
        )
        order_page.confirm_order()
        assert order_page.is_order_successful()