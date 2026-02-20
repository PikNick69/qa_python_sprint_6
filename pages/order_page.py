from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from pages.base_page import BasePage
import allure


class OrderPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        # Локаторы для первой формы
        self.name_input = (By.XPATH, "//input[@placeholder='* Имя']")
        self.surname_input = (By.XPATH, "//input[@placeholder='* Фамилия']")
        self.address_input = (By.XPATH, "//input[@placeholder='* Адрес: куда привезти заказ']")
        self.metro_input = (By.XPATH, "//input[@placeholder='* Станция метро']")
        self.phone_input = (By.XPATH, "//input[@placeholder='* Телефон: на него позвонит курьер']")
        self.next_button = (By.XPATH, "//button[text()='Далее']")
        
        # Локаторы для второй формы
        self.delivery_date_input = (By.XPATH, "//input[@placeholder='* Когда привезти самокат']")
        self.rental_period_placeholder = (By.XPATH, "//div[contains(@class, 'Dropdown-placeholder')]")
        self.rental_period_option = (By.XPATH, "//div[contains(@class, 'Dropdown-option')]")
        self.color_black_checkbox = (By.ID, "black")
        self.color_grey_checkbox = (By.ID, "grey")
        self.comment_input = (By.XPATH, "//input[@placeholder='Комментарий для курьера']")
        self.order_button = (By.XPATH, "//button[text()='Заказать']")
        self.confirm_order_button = (By.XPATH, "//button[text()='Да']")
        
        # Локатор для попапа об успешном заказе
        self.success_popup = (By.XPATH, "//div[contains(text(), 'Заказ оформлен')]")

    @allure.step("Заполнение формы 'Для кого самокат'")
    def fill_first_form(self, name, surname, address, metro_station, phone):
        self.send_keys(self.name_input, name)
        self.send_keys(self.surname_input, surname)
        self.send_keys(self.address_input, address)
        
        metro_input = self.find_element_clickable(self.metro_input)
        metro_input.click()
        metro_input.clear()
        metro_input.send_keys(metro_station)
        
        self.driver.find_elements(By.CLASS_NAME, "select-search__select")
        metro_input.send_keys(Keys.ARROW_DOWN)
        metro_input.send_keys(Keys.ENTER)
        
        self.send_keys(self.phone_input, phone)

    @allure.step("Клик по кнопке 'Далее'")
    def click_next(self):
        self.click_element(self.next_button)
        self.find_element(self.delivery_date_input)

    @allure.step("Заполнение формы 'Про аренду'")
    def fill_second_form(self, delivery_date, rental_period_index, color, comment):
        date_input = self.find_element_clickable(self.delivery_date_input)
        date_input.click()
        date_input.clear()
        date_input.send_keys(delivery_date)
        date_input.send_keys(Keys.ENTER)
        
        self.click_element(self.rental_period_placeholder)
        
        options = self.find_elements(self.rental_period_option)
        if len(options) > rental_period_index:
            self.scroll_to_element_js(options[rental_period_index])
            options[rental_period_index].click()
        else:
            if options:
                self.scroll_to_element_js(options[0])
                options[0].click()

        color_locator = self.color_black_checkbox if color == "black" else self.color_grey_checkbox
        self.scroll_to_element(color_locator)
        self.click_element_js(color_locator)

        self.send_keys(self.comment_input, comment)

    @allure.step("Подтверждение заказа")
    def confirm_order(self):
        order_buttons = self.find_elements(self.order_button)
        order_btn = None
        
        for btn in order_buttons:
            if "Button_Middle" in btn.get_attribute("class"):
                order_btn = btn
                break
        
        if not order_btn and order_buttons:
            order_btn = order_buttons[-1]
        
        if order_btn:
            self.scroll_to_element_js(order_btn)
            order_btn.click()
            self.find_element(self.confirm_order_button)
            self.click_element(self.confirm_order_button)

    @allure.step("Проверка успешного создания заказа")
    def is_order_successful(self):
        return self.is_element_visible(self.success_popup)