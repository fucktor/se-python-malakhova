from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
import unittest, time, re


class Test_PHP4DVD(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Ie()
        self.driver.implicitly_wait(10)
        self.base_url = "http://localhost/php4dvd/"
        self.verificationErrors = []
        self.accept_next_alert = True

    def test_untitled(self):
        driver = self.driver
        driver.get(self.base_url)
        l=driver.find_element_by_id("username")
        l.clear()
        l.send_keys("admin")
        p=driver.find_element_by_name("password")
        p.clear()
        p.send_keys("admin")
        driver.find_element_by_name("submit").click()
        w= WebDriverWait(self.driver, 10).until(lambda driver : driver.find_element_by_xpath("//div[@class='center']//li[4]/*[.='Log out']"))
        try:
            self.assertTrue(self.is_element_present(By.XPATH, "//div[@class='center']//li[4]/*[.='Log out']"), "Кнопка 'Выход' не загрузилась")
        except:
            pass

    def is_element_present(self, how, what):
        try: self.driver.find_element(by=how, value=what)
        except NoSuchElementException, e: return False
        return True

    def close_alert_and_get_its_text(self):
        try:
            alert = self.driver.switch_to_alert()
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert.text
        finally: self.accept_next_alert = True

    def tearDown(self):
        self.driver.quit()


if __name__ == "__main__":
    unittest.main()
