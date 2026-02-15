from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import allure


class HomePage:
    def __init__(self, driver):
        self.driver = driver
        self.faq_section = (By.CLASS_NAME, "Home_FAQ__3uVm4")
        self.top_order_button = (By.CLASS_NAME, "Button_Button__ra12g")  # Верхняя кнопка
        self.bottom_order_button = (By.XPATH, "//button[@class='Button_Button__ra12g' and text()='Заказать']")
        self.scooter_logo = (By.CLASS_NAME, "Header_LogoScooter__3lsAR")
        self.yandex_logo = (By.CLASS_NAME, "Header_LogoYandex__3TSOI")
    def get_question_locator(self, question_text):
        return By.XPATH, f"//div[text()='{question_text}']"
    def get_answer_locator(self, question_text):
        return By.XPATH, f"//div[text()='{question_text}']/ancestor::div[@class='accordion__item']//div[@class='accordion__panel']/p"
    def scroll_to_faq(self):
        with allure.step("Скролл до раздела 'Вопросы о важном'"):
            element = self.driver.find_element(*self.faq_section)
            self.driver.execute_script("arguments[0].scrollIntoView();", element)
    def click_question(self, question_text):
        with allure.step(f"Клик по вопросу: {question_text}"):
            locator = self.get_question_locator(question_text)
            element = WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable(locator)
            )
            element.click()
    def get_answer_text(self, question_text):
        with allure.step(f"Получение текста ответа для вопроса: {question_text}"):
            locator = self.get_answer_locator(question_text)
            answer = WebDriverWait(self.driver, 5).until(
                EC.visibility_of_element_located(locator)
            )
            return answer.text
    def click_top_order_button(self):
        with allure.step("Клик по верхней кнопке 'Заказать'"):
            self.driver.find_element(*self.top_order_button).click()
    def click_bottom_order_button(self):
        with allure.step("Клик по нижней кнопке 'Заказать'"):
            element = self.driver.find_element(*self.bottom_order_button)
            self.driver.execute_script("arguments[0].scrollIntoView();", element)
            element.click()
    def click_scooter_logo(self):
        with allure.step("Клик по логотипу Самоката"):
            self.driver.find_element(*self.scooter_logo).click()
    def click_yandex_logo(self):
        with allure.step("Клик по логотипу Яндекса"):
            self.driver.find_element(*self.yandex_logo).click()