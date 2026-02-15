import allure
import pytest
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.home_page import HomePage


@allure.epic("Тестирование сервиса 'Яндекс.Самокат'")
@allure.feature("Навигация")
class TestNavigation:

    @pytest.mark.navigation
    @allure.title("Проверка перехода на главную страницу по логотипу Самоката")
    @allure.description("Тест проверяет, что при клике на логотип Самоката происходит переход на главную страницу")
    def test_scooter_logo_navigation(self, driver):
        home_page = HomePage(driver)
        current_url = driver.current_url
        
        with allure.step("Клик по логотипу Самоката"):
            home_page.click_scooter_logo()

        with allure.step("Проверка, что URL не изменился (мы уже на главной)"):
            assert driver.current_url == current_url, "Переход на другую страницу не ожидался"
    
    @pytest.mark.navigation
    @allure.title("Проверка перехода на Дзен по логотипу Яндекса")
    @allure.description("Тест проверяет, что при клике на логотип Яндекса открывается Дзен в новом окне")
    def test_yandex_logo_navigation(self, driver):
        home_page = HomePage(driver)
        
        with allure.step("Клик по логотипу Яндекса"):
            home_page.click_yandex_logo()
        
        with allure.step("Переключение на новое окно"):
            original_window = driver.current_window_handle
            new_window = [window for window in driver.window_handles if window != original_window][0]
            driver.switch_to.window(new_window)
        
        with allure.step("Ожидание загрузки страницы Дзена"):
            WebDriverWait(driver, 10).until(
                lambda d: "dzen.ru" in d.current_url or "yandex.ru" in d.current_url
            )
        
        with allure.step("Проверка URL новой страницы"):
            assert "dzen.ru" in driver.current_url or "yandex.ru" in driver.current_url, \
                f"Ожидался переход на Дзен, получен URL: {driver.current_url}"
        
        with allure.step("Закрытие нового окна и возврат к исходному"):
            driver.close()
            driver.switch_to.window(original_window)