import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC


@pytest.fixture(scope="class")
def setup():
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    driver.maximize_window()
    yield driver
    driver.quit()

def test_home_url(setup):
    driver = setup
    home_url = "https://opensource-demo.orangehrmlive.com/web/index.php/auth/login"
    driver.get(home_url)

    wait = WebDriverWait(driver,10)
    login_field = wait.until(EC.presence_of_element_located((By.XPATH,"//input[@placeholder='Username']")))

    assert driver.current_url == home_url,"Home URl  did not load correctly"
    assert login_field.is_displayed(),"Login field is not visible on the home page"



