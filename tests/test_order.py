import allure
import pytest
from pages.home_page import HomePage
from pages.order_page import OrderPage
from data.test_data import ORDER_DATA


@allure.epic("Тестирование сервиса 'Яндекс.Самокат'")
@allure.feature("Оформление заказа")
class TestOrder:
    
    @pytest.mark.order
    @allure.title("Позитивный сценарий заказа самоката")
    @pytest.mark.parametrize("order_data, button_type", [
        (ORDER_DATA[0], "top"),
        (ORDER_DATA[1], "top"),
        (ORDER_DATA[0], "bottom"),
    ])
    def test_successful_order(self, driver, order_data, button_type):
        home_page = HomePage(driver)
        
        if button_type == "top":
            home_page.click_top_order_button()
        else:
            home_page.click_bottom_order_button()
        
        home_page.wait_for_url_contains("order")
        
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