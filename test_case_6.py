import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    driver.quit()

def test_verify_user_exists(driver):
    admin_username = "Admin"
    admin_password = "admin123"
    base_url = "https://opensource-demo.orangehrmlive.com/web/index.php/auth/login"
    new_user = "peter123"


    driver.get(base_url)
    wait = WebDriverWait(driver, 15)
    wait.until(EC.presence_of_element_located((By.NAME, "username"))).send_keys(admin_username)
    wait.until(EC.presence_of_element_located((By.NAME, "password"))).send_keys(admin_password)
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))).click()


    wait.until(EC.presence_of_element_located((By.XPATH, "//span[text()='Admin']"))).click()


    username_input = wait.until(EC.presence_of_element_located((By.XPATH, "//label[text()='Username']/ancestor::div[contains(@class,'oxd-input-group')]/following-sibling::div//input")))
    username_input.clear()
    username_input.send_keys(new_user)


    wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']"))).click()


    try:
        user_element = wait.until(EC.visibility_of_element_located((By.XPATH, f"//div[@class='oxd-table-body']//div[text()='{new_user}']")))
        assert user_element.is_displayed(), f"User '{new_user}' not visible in the user list."
    except:
        driver.save_screenshot("user_not_found.png")
        raise AssertionError(f" User '{new_user}' not found in search results.")
