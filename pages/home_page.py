from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import allure


class HomePage:
    def __init__(self, driver):
        self.driver = driver
        # Локатор для раздела "Вопросы о важном"
        self.faq_section = (By.CLASS_NAME, "Home_FAQ__3uVm4")
        # Локатор для верхней кнопки "Заказать" в хедере
        self.top_order_button = (By.XPATH, "//button[contains(@class, 'Button_Button__ra12g') and text()='Заказать']")
        # Локатор для нижней кнопки "Заказать" в теле страницы
        self.bottom_order_button = (By.XPATH, "//button[contains(@class, 'Button_Button__ra12g') and text()='Заказать']")
        # Локатор для логотипа Самоката (ведет на главную)
        self.scooter_logo = (By.CLASS_NAME, "Header_LogoScooter__3lsAR")
        # Локатор для логотипа Яндекса (ведет на Дзен)
        self.yandex_logo = (By.CLASS_NAME, "Header_LogoYandex__3TSOI")
        # Локатор для баннера с куки
        self.cookie_banner = (By.XPATH, "//div[contains(@class, 'App_CookieConsent')]")
        # Локатор для кнопки принятия куки
        self.cookie_accept_button = (By.XPATH, "//button[contains(text(), 'да все привычны')]")

    @allure.step("Закрытие куки-баннера")
    def close_cookie_banner(self):
        try:
            banner = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(self.cookie_banner))
            if banner.is_displayed():
                accept_button = WebDriverWait(self.driver, 3).until(EC.element_to_be_clickable(self.cookie_accept_button))
                accept_button.click()
        except:
            pass

    def scroll_to_faq(self):
        element = self.driver.find_element(*self.faq_section)
        self.driver.execute_script("arguments[0].scrollIntoView();", element)

    def click_question(self, question_text):
        # Динамический локатор для вопроса по его тексту
        locator = (By.XPATH, f"//div[text()='{question_text}']")
        element = WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable(locator))
        element.click()

    def get_answer_text(self, question_text):
        # Динамический локатор для ответа, связанного с конкретным вопросом
        locator = (By.XPATH, f"//div[text()='{question_text}']/ancestor::div[@class='accordion__item']//div[@class='accordion__panel']/p")
        answer = WebDriverWait(self.driver, 5).until(EC.visibility_of_element_located(locator))
        return answer.text

    def click_top_order_button(self):
        self.close_cookie_banner()
        button = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.top_order_button))
        button.click()

    def click_bottom_order_button(self):
        self.close_cookie_banner()
        button = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(self.bottom_order_button))
        self.driver.execute_script("arguments[0].scrollIntoView();", button)
        WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable(self.bottom_order_button))
        button.click()

    def click_scooter_logo(self):
        self.driver.find_element(*self.scooter_logo).click()

    def click_yandex_logo(self):
        self.driver.find_element(*self.yandex_logo).click()