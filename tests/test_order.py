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
    @allure.description("Тест проверяет полный флоу оформления заказа с разными данными")
    @pytest.mark.parametrize("order_data", ORDER_DATA)
    def test_successful_order(self, driver, order_data):
        home_page = HomePage(driver)
        order_page = OrderPage(driver)
        
        with allure.step("Клик по верхней кнопке 'Заказать'"):
            home_page.click_top_order_button()
        
        with allure.step("Заполнение первой формы заказа"):
            order_page.fill_first_form(
                order_data["name"],
                order_data["surname"],
                order_data["address"],
                order_data["metro"],
                order_data["phone"]
            )
        
        with allure.step("Клик по кнопке 'Далее'"):
            order_page.click_next()
        
        with allure.step("Заполнение второй формы заказа"):
            order_page.fill_second_form(
                order_data["delivery_date"],
                order_data["rental_period"],
                order_data["color"],
                order_data["comment"]
            )
        
        with allure.step("Подтверждение заказа"):
            order_page.confirm_order()
        
        with allure.step("Проверка успешного создания заказа"):
            assert order_page.is_order_successful(), "Заказ не был оформлен успешно"

    @pytest.mark.order
    @allure.title("Оформление заказа через нижнюю кнопку 'Заказать'")
    @allure.description("Тест проверяет оформление заказа при клике на нижнюю кнопку заказа")
    def test_order_via_bottom_button(self, driver):
        home_page = HomePage(driver)
        order_page = OrderPage(driver)
        test_data = ORDER_DATA[0]
        
        with allure.step("Клик по нижней кнопке 'Заказать'"):
            home_page.click_bottom_order_button()
        
        with allure.step("Заполнение форм и оформление заказа"):
            order_page.fill_first_form(
                test_data["name"],
                test_data["surname"],
                test_data["address"],
                test_data["metro"],
                test_data["phone"]
            )
            order_page.click_next()
            order_page.fill_second_form(
                test_data["delivery_date"],
                test_data["rental_period"],
                test_data["color"],
                test_data["comment"]
            )
            order_page.confirm_order()
        
        with allure.step("Проверка успешного создания заказа"):
            assert order_page.is_order_successful(), "Заказ не был оформлен успешно"