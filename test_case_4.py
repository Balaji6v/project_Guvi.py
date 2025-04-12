import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

URL = "https://opensource-demo.orangehrmlive.com/web/index.php/auth/login"

USERNAME = "Admin"
PASSWORD = "admin123"

USERNAME_FIELD = (By.NAME,"username")
PASSWORD_FIELD = (By.NAME,"password")
LOGIN_BUTTON = (By.XPATH,"//button[@type='submit']")


MENU_ITEMS = {
    "admin" : (By.XPATH,"//span[text()='Admin']"),
    "PIM" : (By.XPATH,"//span[text()= 'PIM']"),
    "Leave" : (By.XPATH,"//span[text()='Leave']"),
    "Time" : (By.XPATH,"//span[text()='Time']"),
    "Recruitment" : (By.XPATH,"//span[text()='Recruitment']"),
    "My Info" :(By.XPATH,"//span[text()='My Info']"),
    "Performance" : (By.XPATH,"//span[text()='Performance']"),
    "Dashboard" : (By.XPATH,"//span[text()='Dashboard']")

}

@pytest.fixture
def browser():
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get(URL)
    yield driver
    driver.quit()


def test_verify_menu_after_login(browser):
    wait = WebDriverWait(browser,10)

    wait.until(EC.presence_of_element_located(USERNAME_FIELD)).send_keys(USERNAME)
    wait.until(EC.presence_of_element_located(PASSWORD_FIELD)).send_keys(PASSWORD)

    wait.until(EC.element_to_be_clickable(LOGIN_BUTTON)).click()

    for menu_name,locator in MENU_ITEMS.items():
        menu_element =wait.until(EC.presence_of_element_located(locator))

        assert menu_element.is_displayed(), f"{menu_name} menu is not visible"

        assert EC.element_to_be_clickable(locator)(browser), f"{menu_name} menu is not clickable"