import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



URL = "https://opensource-demo.orangehrmlive.com/web/index.php/auth/login"
USERNAME_FIELD  = (By.NAME,"username")
PASSWORD_FIELD = (By.NAME,"password")


@pytest.fixture
def browser():
    driver = webdriver.Chrome()
    driver.get(URL)
    yield driver
    driver.quit()

def test_input_boxes_visible(browser):


    WebDriverWait(browser,10).until(EC.presence_of_element_located(USERNAME_FIELD))
    WebDriverWait(browser,10).until(EC.presence_of_element_located(PASSWORD_FIELD))


    username_input = browser.find_element(*USERNAME_FIELD)
    password_input = browser.find_element(*PASSWORD_FIELD)

    assert username_input.is_displayed(), "username input boxes is not visible"
    assert password_input.is_displayed(), "password input boxes is not visible"

