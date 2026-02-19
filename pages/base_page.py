from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import allure


class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.timeout = 15

    def find_element(self, locator):
        """Поиск элемента с ожиданием"""
        return WebDriverWait(self.driver, self.timeout).until(
            EC.presence_of_element_located(locator)
        )

    def find_element_clickable(self, locator):
        """Поиск кликабельного элемента"""
        return WebDriverWait(self.driver, self.timeout).until(
            EC.element_to_be_clickable(locator)
        )

    def find_elements(self, locator):
        """Поиск нескольких элементов"""
        return WebDriverWait(self.driver, self.timeout).until(
            EC.presence_of_all_elements_located(locator)
        )

    def click_element(self, locator):
        """Клик по элементу"""
        element = self.find_element_clickable(locator)
        element.click()
        return element

    def click_element_js(self, locator):
        """Клик через JavaScript"""
        element = self.find_element(locator)
        self.driver.execute_script("arguments[0].click();", element)
        return element

    def scroll_to_element(self, locator):
        """Скролл до элемента"""
        element = self.find_element(locator)
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
        return element

    def scroll_to_element_js(self, element):
        """Скролл до элемента (принимает WebElement)"""
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)

    def send_keys(self, locator, text):
        """Ввод текста"""
        element = self.find_element_clickable(locator)
        element.clear()
        element.send_keys(text)
        return element

    def get_text(self, locator):
        """Получение текста элемента"""
        element = self.find_element(locator)
        return element.text

    def get_attribute(self, locator, attribute):
        """Получение атрибута элемента"""
        element = self.find_element(locator)
        return element.get_attribute(attribute)

    def is_element_visible(self, locator):
        """Проверка видимости элемента (без try/except)"""
        elements = self.driver.find_elements(*locator)
        if elements:
            return elements[0].is_displayed()
        return False

    def wait_for_url_contains(self, text):
        """Ожидание содержания текста в URL"""
        WebDriverWait(self.driver, self.timeout).until(
            lambda driver: text in driver.current_url
        )
        return True

    def switch_to_new_window(self):
        """Переключение на новое окно"""
        original_window = self.driver.current_window_handle
    
        WebDriverWait(self.driver, 10).until(lambda d: len(d.window_handles) > 1)
    
        for window_handle in self.driver.window_handles:
            if window_handle != original_window:
                self.driver.switch_to.window(window_handle)
                break
    
        return original_window

    def close_window_and_switch_back(self, original_window):
        """Закрытие текущего окна и возврат к исходному"""
        self.driver.close()
        self.driver.switch_to.window(original_window)