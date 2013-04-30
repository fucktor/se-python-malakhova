import pytest
from selenium import webdriver
from model.application import Application
import pytest

def pytest_addoption(parser):
    parser.addoption("--browser_type", action="store", default="firefox", help="browser type")
    parser.addoption("--base_url", action="store", default="http://localhost/php4dvd/", help="base URL")


@pytest.fixture(scope="session")
def browser_type(request):
    return request.config.getoption("--browser_type")


@pytest.fixture(scope="session")
def base_url(request):
    return request.config.getoption("--base_url")


@pytest.fixture(scope="session")
def app(request, browser_type,base_url):
    if browser_type == "firefox":
        driver = webdriver.Firefox()
    elif browser_type == "chrome":
        driver = webdriver.Chrome()
    elif browser_type == "ie":
        driver = webdriver.Ie()
    request.addfinalizer(driver.quit)
    return Application(driver,base_url)


