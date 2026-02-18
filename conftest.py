import pytest
from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager


@pytest.fixture
def driver():
    firefox_options = webdriver.FirefoxOptions()
    firefox_options.add_argument("--width=1366")
    firefox_options.add_argument("--height=768")
    
    service = FirefoxService(GeckoDriverManager().install())
    driver = webdriver.Firefox(service=service, options=firefox_options)
    driver.get("https://qa-scooter.praktikum-services.ru/")
    
    yield driver
    
    driver.quit()