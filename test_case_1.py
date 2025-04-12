import pytest
import pandas as pd
import math
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import ddt

def read_test_file(file_path,sheet_name):
    df = pd.read_excel(file_path,sheet_name=sheet_name)
    df["Test Result"] = df['Test Result'].apply(lambda x:"fail" if isinstance(x,float) and math.isnan(x) else x)
    print("Coloumns in the excel file",df.columns.tolist())
    return df.to_dict(orient='records')

EXCEL_FILE = r"D:\project\data_test.xlsx"
SHEET_NAME = "Sheet1"

test_data = read_test_file(EXCEL_FILE,SHEET_NAME)

@pytest.fixture(scope="class")
def setup():
    service=Service(ChromeDriverManager().install())
    driver=webdriver.Chrome(service=service)
    driver.get("https://opensource-demo.orangehrmlive.com/web/index.php/auth/login")
    driver.maximize_window()
    driver.implicitly_wait(5)
    yield driver
    driver.quit()

@pytest.mark.parametrize("username,password,expected_result",[(data['username'],data['password'],data['Test Result'])for data in test_data])
def test_login(setup,username,password,expected_result):
    driver=setup
    wait = WebDriverWait(driver,15)



    username_field = wait.until(EC.visibility_of_element_located((By.XPATH,"//input[@placeholder='Username']")))
    password_field = wait.until(EC.visibility_of_element_located((By.XPATH,"//input[@placeholder='Password']")))

    username_field.clear()
    username_field.send_keys(username)

    password_field.clear()
    password_field.send_keys(password)

    login_button = wait.until(EC.presence_of_element_located((By.XPATH,"//button[@type='submit']")))
    login_button.click()

    try:
        wait.until(EC.presence_of_element_located((By.XPATH,"//a[contains(text(),'Logout')]")))
        actual_result = "pass"

        cookies = driver.get_cookies()
        with open("cookies.pkl","wb") as f:
            import pickle
            pickle.dump(cookies,f)

    except:
        actual_result = "fail"

    assert actual_result == expected_result, f"login test failed for {username}"


def test_login_using_cookies(setup):
     driver = setup
     wait = WebDriverWait(driver,10)

     import os
     import pickle


     if os.path.exists("cookies.pkl"):
         with open("cookies.pkl","rb") as f:
             cookies = pickle.load(f)

         for  cookie in cookies:
             driver.add_cookie(cookie)


         driver.refresh()

         try:
             wait.until(EC.presence_of_element_located((By.XPATH,"//a[contains(text(),'Logout')]")))
             print("Login succesfully using cookies")

         except:
             print("Login failed using cookies")
     else:
         print("No saved cookies")
