from selenium import webdriver
import pytest
from config import *

@pytest.fixture(scope="module")

def driver(request):
    driver = webdriver.Firefox()
    request.addfinalizer(driver.quit)
    return driver

