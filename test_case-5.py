import pytest
import time
import uuid
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Setup logging
logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

# Admin credentials and employee to assign
ADMIN_USERNAME = "Admin"
ADMIN_PASSWORD = "admin123"
EMPLOYEE_NAME = "Thomas Kutty Benny"
NEW_PASSWORD = "Test@1234"
URL = "https://opensource-demo.orangehrmlive.com/web/index.php/auth/login"

# Dynamically generate a unique username to avoid conflicts
NEW_USERNAME = "thomas1234"


@pytest.fixture
def browser():
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get(URL)
    yield driver
    driver.quit()


def login_(browser, username, password):
    wait = WebDriverWait(browser, 15)
    wait.until(EC.presence_of_element_located((By.NAME, "username"))).send_keys(username)
    wait.until(EC.presence_of_element_located((By.NAME, "password"))).send_keys(password)
    wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']"))).click()


def logout(browser):
    wait = WebDriverWait(browser, 10)
    wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "oxd-userdropdown-tab"))).click()
    wait.until(EC.element_to_be_clickable((By.XPATH, "//a[text()='Logout']"))).click()


def test_create_and_login_new_user(browser):
    wait = WebDriverWait(browser, 15)

    # Step 1: Login as admin
    log.info(" Logging in as Admin.")
    login_(browser, ADMIN_USERNAME, ADMIN_PASSWORD)
    wait.until(EC.visibility_of_element_located((By.XPATH, "//h6[text()='Dashboard']")))

    # Step 2: Navigate to Admin module
    log.info(" Navigating to Admin module")
    admin_menu = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[text()='Admin']")))
    browser.execute_script("arguments[0].scrollIntoView();", admin_menu)
    admin_menu.click()
    time.sleep(1)


    try:
        header = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "h6.oxd-text.oxd-text--h6")))
        assert "Admin" in header.text
    except Exception:
        browser.save_screenshot("admin_page_not_loaded.png")
        raise Exception("Admin page failed to load properly.")


    log.info(f" Creating new user: {NEW_USERNAME}")
    browser.save_screenshot("before_add_button_click.png")
    try:
        add_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Add')]")))
        browser.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", add_button)
        time.sleep(0.5)
        add_button.click()
    except Exception:
        browser.save_screenshot("add_button_not_found.png")
        raise Exception("Failed to click the 'Add' button.")


    wait.until(EC.presence_of_element_located((By.XPATH, "//label[text()='User Role']/../following-sibling::div"))).click()
    wait.until(EC.presence_of_element_located((By.XPATH, "//div[@role='listbox']//span[text()='ESS']"))).click()

    emp_input = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Type for hints...']")))
    emp_input.send_keys(EMPLOYEE_NAME)
    wait.until(EC.presence_of_element_located((By.XPATH, "//div[@role='listbox']")))
    time.sleep(1)
    try:
        wait.until(EC.visibility_of_element_located((By.XPATH, f"//span[contains(text(), '{EMPLOYEE_NAME}')]"))).click()
    except Exception:
        browser.save_screenshot("employee_suggestion_not_found.png")
        raise Exception(f"Employee '{EMPLOYEE_NAME}' not selectable.")

    wait.until(EC.presence_of_element_located((By.XPATH, "//label[text()='Username']/../following-sibling::div//input"))).send_keys(NEW_USERNAME)
    wait.until(EC.presence_of_element_located((By.XPATH, "//label[text()='Status']/../following-sibling::div"))).click()
    wait.until(EC.presence_of_element_located((By.XPATH, "//div[@role='listbox']//span[text()='Enabled']"))).click()
    wait.until(EC.presence_of_element_located((By.XPATH, "//label[text()='Password']/../following-sibling::div//input"))).send_keys(NEW_PASSWORD)
    wait.until(EC.presence_of_element_located((By.XPATH, "//label[text()='Confirm Password']/../following-sibling::div//input"))).send_keys(NEW_PASSWORD)

    save_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@type='submit' and contains(., 'Save')]")))
    save_button.click()


    try:
        wait.until(EC.visibility_of_element_located((By.XPATH, "//div[contains(@class,'oxd-toast-content') and contains(., 'Successfully Saved')]")))
        log.info("✅ User created successfully.")
    except:
        browser.save_screenshot("user_creation_failed.png")
        raise Exception("User creation likely failed.")

    wait.until(EC.presence_of_element_located((By.XPATH, f"//div[@class='oxd-table-body']//div[text()='{NEW_USERNAME}']")))


    log.info(f" Logging out and logging in as new user: {NEW_USERNAME}")
    logout(browser)
    login_(browser, NEW_USERNAME, NEW_PASSWORD)
    browser.save_screenshot("after_login_new_user.png")

