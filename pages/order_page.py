from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import allure


class OrderPage:
    def __init__(self, driver):
        self.driver = driver
        self.name_input = (By.XPATH, "//input[@placeholder='* Имя']")
        self.surname_input = (By.XPATH, "//input[@placeholder='* Фамилия']")
        self.address_input = (By.XPATH, "//input[@placeholder='* Адрес: куда привезти заказ']")
        self.metro_input = (By.XPATH, "//input[@placeholder='* Станция метро']")
        self.phone_input = (By.XPATH, "//input[@placeholder='* Телефон: на него позвонит курьер']")
        self.next_button = (By.XPATH, "//button[text()='Далее']")

        self.delivery_date_input = (By.XPATH, "//input[@placeholder='* Когда привезти самокат']")
        self.rental_period_dropdown = (By.CLASS_NAME, "Dropdown-placeholder")
        self.color_black_checkbox = (By.ID, "black")
        self.color_grey_checkbox = (By.ID, "grey")
        self.comment_input = (By.XPATH, "//input[@placeholder='Комментарий для курьера']")
        self.order_button = (By.XPATH, "//button[contains(@class, 'Button_Middle__1CSJM') and text()='Заказать']")
        self.confirm_order_button = (By.XPATH, "//button[text()='Да']")

        self.success_popup = (By.XPATH, "//div[contains(text(), 'Заказ оформлен')]")

    def get_metro_station_locator(self, station_name):
        return By.XPATH, f"//div[text()='{station_name}']" # Локатор для выбора станции метро
    def get_rental_period_locator(self, period):
        return By.XPATH, f"//div[text()='{period}']" # Локатор для выбора периода аренды
    
    @allure.step("Заполнение формы 'Для кого самокат'")
    def fill_first_form(self, name, surname, address, metro_station, phone):
        self.driver.find_element(*self.name_input).send_keys(name)
        self.driver.find_element(*self.surname_input).send_keys(surname)
        self.driver.find_element(*self.address_input).send_keys(address)
        self.driver.find_element(*self.metro_input).click()
        station_locator = self.get_metro_station_locator(metro_station)
        WebDriverWait(self.driver, 5).until(
            EC.visibility_of_element_located(station_locator)
        ).click()
        
        self.driver.find_element(*self.phone_input).send_keys(phone)

    @allure.step("Клик по кнопке 'Далее'")
    def click_next(self):
        """Клик по кнопке 'Далее'"""
        self.driver.find_element(*self.next_button).click()

    @allure.step("Заполнение формы 'Про аренду'")
    def fill_second_form(self, delivery_date, rental_period, color, comment):
        """Заполнение второй формы заказа"""
        date_input = self.driver.find_element(*self.delivery_date_input)
        date_input.send_keys(delivery_date)
        date_input.send_keys("\n")
        self.driver.find_element(*self.rental_period_dropdown).click()
        period_locator = self.get_rental_period_locator(rental_period)
        WebDriverWait(self.driver, 5).until(
            EC.element_to_be_clickable(period_locator)
        ).click()

        if color == "black":
            self.driver.find_element(*self.color_black_checkbox).click()
        elif color == "grey":
            self.driver.find_element(*self.color_grey_checkbox).click()

        self.driver.find_element(*self.comment_input).send_keys(comment)

    @allure.step("Подтверждение заказа")
    def confirm_order(self):
        """Подтверждение заказа"""
        self.driver.find_element(*self.order_button).click()
        WebDriverWait(self.driver, 5).until(
            EC.element_to_be_clickable(self.confirm_order_button)
        ).click()

    @allure.step("Проверка успешного создания заказа")
    def is_order_successful(self):
        """Проверка появления попапа об успешном заказе"""
        try:
            popup = WebDriverWait(self.driver, 5).until(
                EC.visibility_of_element_located(self.success_popup)
            )
            return popup.is_displayed()
        except:
            return False