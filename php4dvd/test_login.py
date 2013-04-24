from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import *
from config import *
from php4dvd_fixture import driver

def is_logged(driver):
    try:
        WebDriverWait(driver, 10).until(presence_of_element_located((By.XPATH, "//div[@class='center']//li[4]/*[.='Log out']")))
        return True
    except WebDriverException:
        print("Не удалось залогиниться")
        return False

def test_login(driver):
    driver.get(base_url)
    l=driver.find_element_by_id("username")
    l.clear()
    l.send_keys(username)
    p=driver.find_element_by_name("password")
    p.clear()
    p.send_keys(password)
    driver.find_element_by_name("submit").click()
    assert is_logged(driver)

