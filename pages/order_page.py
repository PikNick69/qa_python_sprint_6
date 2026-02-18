from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import allure
import time


class OrderPage:
    def __init__(self, driver):
        self.driver = driver
        # Локаторы для первой формы (Для кого самокат)
        self.name_input = (By.XPATH, "//input[@placeholder='* Имя']")                     # Поле ввода имени
        self.surname_input = (By.XPATH, "//input[@placeholder='* Фамилия']")              # Поле ввода фамилии
        self.address_input = (By.XPATH, "//input[@placeholder='* Адрес: куда привезти заказ']")  # Поле ввода адреса
        self.metro_input = (By.XPATH, "//input[@placeholder='* Станция метро']")          # Поле выбора метро
        self.phone_input = (By.XPATH, "//input[@placeholder='* Телефон: на него позвонит курьер']")  # Поле телефона
        self.next_button = (By.XPATH, "//button[text()='Далее']")                         # Кнопка "Далее"
        
        # Локаторы для второй формы (Про аренду)
        self.delivery_date_input = (By.XPATH, "//input[@placeholder='* Когда привезти самокат']")  # Поле даты
        self.rental_period_placeholder = (By.CLASS_NAME, "Dropdown-placeholder")          # Дропдаун выбора периода
        self.rental_period_option = (By.CLASS_NAME, "Dropdown-option")                    # Опции в дропдауне
        self.color_black_checkbox = (By.ID, "black")                                      # Чекбокс черного цвета
        self.color_grey_checkbox = (By.ID, "grey")                                        # Чекбокс серого цвета
        self.comment_input = (By.XPATH, "//input[@placeholder='Комментарий для курьера']")  # Поле комментария
        self.order_button = (By.XPATH, "//button[text()='Заказать']")                    # Кнопка "Заказать"
        self.confirm_order_button = (By.XPATH, "//button[text()='Да']")                  # Кнопка подтверждения "Да"
        
        # Локатор для попапа об успешном заказе
        self.success_popup = (By.XPATH, "//div[contains(text(), 'Заказ оформлен')]")

    @allure.step("Заполнение формы 'Для кого самокат'")
    def fill_first_form(self, name, surname, address, metro_station, phone):
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(self.name_input))
        
        name_field = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.name_input))
        name_field.send_keys(name)
        
        surname_field = WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable(self.surname_input))
        surname_field.send_keys(surname)
        
        address_field = WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable(self.address_input))
        address_field.send_keys(address)
        
        metro_input = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.metro_input))
        metro_input.click()
        metro_input.clear()
        metro_input.send_keys(metro_station)
        time.sleep(1)
        metro_input.send_keys(Keys.ARROW_DOWN)
        time.sleep(0.5)
        metro_input.send_keys(Keys.ENTER)
        time.sleep(1)
        
        phone_field = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.phone_input))
        phone_field.send_keys(phone)
        
        allure.attach(self.driver.get_screenshot_as_png(), name="after_first_form", attachment_type=allure.attachment_type.PNG)

    @allure.step("Клик по кнопке 'Далее'")
    def click_next(self):
        next_btn = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.next_button))
        self.driver.execute_script("arguments[0].scrollIntoView(true);", next_btn)
        time.sleep(0.5)
        self.driver.execute_script("arguments[0].click();", next_btn)
        WebDriverWait(self.driver, 15).until(EC.presence_of_element_located(self.delivery_date_input))
        time.sleep(1)
        allure.attach(self.driver.get_screenshot_as_png(), name="after_click_next", attachment_type=allure.attachment_type.PNG)

    @allure.step("Заполнение формы 'Про аренду'")
    def fill_second_form(self, delivery_date, rental_period_index, color, comment):
        date_input = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.delivery_date_input))
        date_input.click()
        date_input.clear()
        date_input.send_keys(delivery_date)
        date_input.send_keys(Keys.ENTER)
        time.sleep(1)
        
        dropdown = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.rental_period_placeholder))
        dropdown.click()
        time.sleep(1)
        
        options = self.driver.find_elements(By.CLASS_NAME, "Dropdown-option")
        if len(options) > rental_period_index:
            options[rental_period_index].click()
        elif len(options) > 0:
            options[0].click()
        time.sleep(1)
        
        color_checkbox = self.driver.find_element(*self.color_black_checkbox) if color == "black" else self.driver.find_element(*self.color_grey_checkbox)
        self.driver.execute_script("arguments[0].scrollIntoView(true);", color_checkbox)
        time.sleep(0.5)
        self.driver.execute_script("arguments[0].click();", color_checkbox)
        time.sleep(1)
        
        comment_input = self.driver.find_element(*self.comment_input)
        comment_input.send_keys(comment)
        allure.attach(self.driver.get_screenshot_as_png(), name="after_second_form", attachment_type=allure.attachment_type.PNG)

    @allure.step("Подтверждение заказа")
    def confirm_order(self):
        # Ищем все кнопки с текстом "Заказать" и выбираем нужную (с классом Button_Middle)
        order_buttons = self.driver.find_elements(By.XPATH, "//button[text()='Заказать']")
        order_btn = None
        for btn in order_buttons:
            if "Button_Middle__1CSJM" in btn.get_attribute("class"):
                order_btn = btn
                break
        if not order_btn and len(order_buttons) > 0:
            order_btn = order_buttons[0]
        
        self.driver.execute_script("arguments[0].scrollIntoView(true);", order_btn)
        time.sleep(1)
        order_btn.click()
        time.sleep(2)
        
        confirm_btn = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.confirm_order_button))
        confirm_btn.click()
        time.sleep(2)
        allure.attach(self.driver.get_screenshot_as_png(), name="after_confirmation", attachment_type=allure.attachment_type.PNG)

    @allure.step("Проверка успешного создания заказа")
    def is_order_successful(self):
        try:
            popup = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(self.success_popup))
            allure.attach(self.driver.get_screenshot_as_png(), name="order_success", attachment_type=allure.attachment_type.PNG)
            return True
        except:
            allure.attach(self.driver.get_screenshot_as_png(), name="order_failure", attachment_type=allure.attachment_type.PNG)
            return False