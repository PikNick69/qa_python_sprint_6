import allure
import pytest
from pages.home_page import HomePage


@allure.epic("Тестирование сервиса 'Яндекс.Самокат'")
@allure.feature("Навигация")
class TestNavigation:
    @pytest.mark.navigation
    @allure.title("Проверка перехода на главную страницу по логотипу Самоката")
    def test_scooter_logo_navigation(self, driver):
        home_page = HomePage(driver)
        current_url = driver.current_url
        home_page.click_scooter_logo()
        assert driver.current_url == current_url

    @pytest.mark.navigation
    @allure.title("Проверка перехода на Дзен по логотипу Яндекса")
    def test_yandex_logo_navigation(self, driver):
        home_page = HomePage(driver)
        home_page.click_yandex_logo()
        
        original_window = home_page.switch_to_new_window()
        
        home_page.wait_for_url_contains("dzen.ru") or home_page.wait_for_url_contains("yandex.ru")
        
        current_url = driver.current_url
        assert "dzen.ru" in current_url or "yandex.ru" in current_url
        
        home_page.close_window_and_switch_back(original_window)