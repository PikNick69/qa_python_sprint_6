from selenium.webdriver.common.by import By
from pages.base_page import BasePage
import allure


class HomePage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        # Локаторы
        self.faq_section = (By.CLASS_NAME, "Home_FAQ__3uVm4")
        self.order_buttons = (By.XPATH, "//button[contains(@class, 'Button_Button__ra12g') and text()='Заказать']")
        self.scooter_logo = (By.CLASS_NAME, "Header_LogoScooter__3lsAR")
        self.yandex_logo = (By.CLASS_NAME, "Header_LogoYandex__3TSOI")

    @allure.step("Скролл до раздела 'Вопросы о важном'")
    def scroll_to_faq(self):
        self.scroll_to_element(self.faq_section)

    @allure.step("Клик по вопросу: {question_text}")
    def click_question(self, question_text):
        question_locator = (By.XPATH, f"//div[text()='{question_text}']")
        self.click_element(question_locator)

    @allure.step("Получение текста ответа")
    def get_answer_text(self, question_text):
        answer_locator = (By.XPATH, f"//div[text()='{question_text}']/ancestor::div[@class='accordion__item']//div[@class='accordion__panel']/p")
        return self.get_text(answer_locator)

    @allure.step("Проверка видимости ответа")
    def is_answer_visible(self, question_text):
        answer_locator = (By.XPATH, f"//div[text()='{question_text}']/ancestor::div[@class='accordion__item']//div[@class='accordion__panel']")
        return self.is_element_visible(answer_locator)

    @allure.step("Клик по верхней кнопке 'Заказать'")
    def click_top_order_button(self):
        buttons = self.find_elements(self.order_buttons)
        if buttons:
            self.click_element_js(self.order_buttons)

    @allure.step("Клик по нижней кнопке 'Заказать'")
    def click_bottom_order_button(self):
        buttons = self.find_elements(self.order_buttons)
        if len(buttons) > 1:
            self.scroll_to_element_js(buttons[1])
            self.driver.execute_script("arguments[0].click();", buttons[1])

    @allure.step("Клик по логотипу Самоката")
    def click_scooter_logo(self):
        self.click_element(self.scooter_logo)

    @allure.step("Клик по логотипу Яндекса")
    def click_yandex_logo(self):
        self.click_element(self.yandex_logo)