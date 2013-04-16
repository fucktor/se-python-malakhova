from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
import unittest, time, re


class Test_PHP4DVD(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.base_url = "http://localhost/php4dvd/"
        self.driver.get(self.base_url)

    def login(self, log, passw):
        l=self.driver.find_element_by_id("username")
        l.clear()
        l.send_keys(log)
        p=self.driver.find_element_by_name("password")
        p.clear()
        p.send_keys(passw)
        self.driver.find_element_by_name("submit").click()
        w= WebDriverWait(self.driver, 10).until(lambda driver : self.driver.find_element_by_xpath("//div[@class='center']//li[4]/*[.='Log out']"))

    def AddMovies(self, idMovie, nameMovie, yearMovie):
        w= WebDriverWait(self.driver, 10).until(lambda driver : self.driver.find_element_by_xpath("//img[@title='Add movie']"))
        w.click()
        w=WebDriverWait(self.driver, 10).until(lambda driver : self.driver.find_element_by_xpath("//div[@class='content']/div[@class='addmovie']"))
        try:
            self.assertTrue(self.is_element_present(By.XPATH, "//div[@class='content']/div[@class='addmovie']"), "Страница не загрузилась")
        except:
            pass
        f=self.driver.find_element_by_name("imdbid")
        f.clear()
        f.send_keys(idMovie)
        p=self.driver.find_element_by_name("name")
        p.clear()
        p.send_keys(nameMovie)
        t=self.driver.find_element_by_name("year")
        t.clear()
        t.send_keys(yearMovie)
        self.driver.find_element_by_xpath("//img[@title='Save']").click()

    def DeleteMovies(self, NameMovie):
        self.driver.find_element_by_xpath("//div[.='"+NameMovie+"']").click()
        w= WebDriverWait(self.driver, 10).until(lambda driver : self.driver.find_element_by_xpath("//img[@title='Remove']"))
        w.click()
        alert=self.driver.switch_to_alert()
        alert.accept()
        w= WebDriverWait(self.driver, 10).until(lambda driver : self.driver.find_element_by_id("results"))

    def test_AddMovies_Valid(self):
        """добавление фильма в коллекцию с валидными данными"""
        self.login("admin", "admin")
##        Movies={'Movies1': ('1', 'Game of thrones', '2013'),
##        'Movies2': ('2', 'Dead fish', '2005'),
##        'Movies3': ('3', 'Amazing grace', '2006')}
##        for l in range(1,4):
        self.AddMovies('1', 'Game of thrones', '2013')
        w=WebDriverWait(self.driver, 10).until(lambda driver : self.driver.find_element_by_xpath("//div[@class='content']/div[@id='movie']"))
        try:
            self.assertTrue(self.driver.find_element_by_xpath("//div[@class='content']/div[@id='movie']//h2").text==Movies['Movies'+str(l)][1], "Фильм не добавился в коллекцию")
        except:
            pass
        self.driver.find_element_by_xpath("//a[.='Home']").click()
        w=WebDriverWait(self.driver, 10).until(lambda driver : self.driver.find_element_by_id("results"))

    def test_AddMovies_InvalidID(self):
        """добавление фильма в коллекцию с некорректным ID"""
        self.login("admin", "admin")
        Movies={'Movies1': ('qq', 'Game of thrones', '2013')}
        self.AddMovies(Movies['Movies1'][0], Movies['Movies1'][1], Movies['Movies1'][2])
        w=WebDriverWait(self.driver, 10).until(lambda driver : self.driver.find_element_by_xpath("//label[@class='error']"))
        try:
            self.assertTrue(self.is_element_present(By.XPATH, "//label[@class='error']"), "Предупреждающее сообщение не появилось")
        except:
            pass

    def test_AddMovies_InvalidYear(self):
        """добавление фильма в коллекцию с некорректным годом"""
        self.login("admin", "admin")
        Movies={'Movies2': ('2', 'Dead fish', 'tttt'), 'Movies3': ('3', 'Game of thrones', '')}
        self.AddMovies(Movies['Movies2'][0], Movies['Movies2'][1], Movies['Movies2'][2])
        w=WebDriverWait(self.driver, 10).until(lambda driver : self.driver.find_element_by_xpath("//label[@class='error']"))
        try:
            self.assertTrue(self.is_element_present(By.XPATH, "//label[@class='error']"), "Предупреждающее сообщение не появилось")
        except:
            pass

    def test_DeleteMovie(self):
        """удаление фильма из коллекции """
        self.login("admin", "admin")
        self.DeleteMovies("Game of thrones")
        try:
            self.assertFalse(self.is_element_present(By.XPATH, "//div[.='Game of thrones']"), "Фильм не удалился")
        except:
            pass


    def tearDown(self):
        self.driver.quit()


if __name__ == "__main__":
    unittest.main()
