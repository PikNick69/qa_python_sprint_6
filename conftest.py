import pytest
from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
from data.urls import Urls



@pytest.fixture
def driver():
    firefox_options = webdriver.FirefoxOptions()
    firefox_options.add_argument("--width=1366")
    firefox_options.add_argument("--height=768")
    
    service = FirefoxService(GeckoDriverManager().install())
    driver = webdriver.Firefox(service=service, options=firefox_options)
    driver.get(Urls.BASE_URL)
    
    yield driver
    
    driver.quit()

@pytest.fixture
def close_cookie(home_page):
    """Фикстура для закрытия куки"""
    home_page.close_cookie_banner()
    return home_page