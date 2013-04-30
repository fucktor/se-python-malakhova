from php4dvd.pages.login_page import LoginPage
from php4dvd.pages.collection_page import CollectionPage
from php4dvd.pages.add_movie_page import AddMoviePage
from php4dvd.pages.movie_in_collection_page import MovieInCollectionPage
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import *
from selenium.webdriver.common.keys import Keys


class Application(object):

    def __init__(self, driver, base_url):
        driver.get(base_url)
        self.driver=driver
        self.wait = WebDriverWait(driver, 10)
        self.login_page=LoginPage(driver, base_url)
        self.collection_page=CollectionPage(driver, base_url)
        self.addmovie_page=AddMoviePage(driver, base_url)
        self.movie_in_collection_page=MovieInCollectionPage(driver, base_url)

    def login(self, user):
        lp=self.login_page
        lp.username_field.clear()
        lp.username_field.send_keys(user.username)
        lp.password_field.clear()
        lp.password_field.send_keys(user.passw)
        lp.submit_button.click()

    def is_logged_in(self):
        return self.collection_page.is_this_page

    def logout(self):
        self.collection_page.logout_button.click()
        self.driver.switch_to_alert().accept()

    def is_logout(self):
        return self.login_page.is_this_page

    def AddMovies(self, idMovie, nameMovie, yearMovie):
        cp=self.collection_page
        addp=self.addmovie_page
        cp.add_movie_button.click()
        self.is_add_page()
        addp.id_movie_field.clear()
        addp.id_movie_field.send_keys(idMovie)
        addp.name_movie_field.clear()
        addp.name_movie_field.send_keys(nameMovie)
        addp.year_movie_field.clear()
        addp.year_movie_field.send_keys(yearMovie)
        addp.save_button.click()

    def home_page_return(self):
        cp=self.collection_page
        self.wait.until(presence_of_element_located((By.XPATH, "//div[@class='content']/div[@id='movie']")))
        cp.home_link.click()
 ##       self.wait.until(lambda driver : self.driver.find_element_by_xpath("//div[@id='results']/a"))

    def is_add_page(self):
        return self.addmovie_page.is_this_page

    def is_add_movie_page(self):
        return self.movie_in_collection_page.is_this_page

    def check_add_movie(self, name, year):
        cp=self.collection_page
        self.wait.until(presence_of_element_located((By.XPATH, "//div[@id='results']/a")))
        AllMovies=cp.all_movies
        ListMovies=[]
        for l in AllMovies:
            ListMovies.append(l.text)
        try:
            if name in ListMovies:
                return True
        except WebDriverException:
            print("Фильм не сохранился")
            return False

    def check_add_movies_search(self, id, name, year):
        self.wait.until(presence_of_element_located((By.XPATH, "//div[@id='results']/a")))
        AllMovies=self.driver.find_elements_by_xpath("//div[@class='title']")
        ListMovies=[]
        for l in AllMovies:
            ListMovies.append(l.text)
        if not name in ListMovies:
            self.AddMovies(id, name, year)
            self.home_page_return()

    def check_movies(self, name):
        self.wait.until(presence_of_element_located((By.XPATH, "//div[@id='results']/a")))
        AllMovies=self.driver.find_elements_by_xpath("//div[@class='title']")
        ListM=[]
        for l in AllMovies:
            if l.text==name:
                ListM.append(l.text)
        if len(ListM)>-1:
            for i in ListM:
                self.DeleteMovies(i)
##                time.sleep(2)

    def check_message_err(self):
        try:
            self.wait.until(presence_of_element_located((By.XPATH, "//label[@class='error']")))
            return True
        except WebDriverException:
            print("Отсутствует предупреждающее сообщение")
            return False

    def DeleteMovies(self, Name):
        driver=self.driver
        addp=self.movie_in_collection_page
        w= self.wait.until(lambda driver : driver.find_element_by_xpath("//div[@id='results']/a"))
        s=driver.find_element_by_xpath("//div[@class='title'][.='"+Name+"']")
        s.click()
        self.movie_in_collection_page.is_this_page
        addp.delete_movie_button.click()
        driver.switch_to_alert().accept()
        w= self.wait.until(lambda driver : driver.find_element_by_xpath("//div[@id='results']/a"))

    def search_movie(self, nameMovie):
        cp=self.collection_page
        self.wait.until(presence_of_element_located((By.XPATH, "//div[@id='results']/a")))
        cp.search_field.clear()
        cp.search_field.send_keys(nameMovie)
        cp.search_field.send_keys(Keys.RETURN)
        self.wait.until(invisibility_of_element_located((By.XPATH, "//div[@class='title'][.!='"+nameMovie+"']")))


    def check_delete_movie(self, Name):
        self.wait.until(presence_of_element_located((By.XPATH, "//div[@id='results']/a")))
        try:
            self.wait.until(invisibility_of_element_located((By.XPATH, "//div[.='"+Name+"']")))
            return True
        except WebDriverException:
            print("Фильм не удалился")
            return False

    def check_search_valid_movie(self, nameMovie):
        self.wait.until(visibility_of_element_located((By.XPATH, "//div[@class='title'][.='"+nameMovie+"']")))
        AllMovies=self.driver.find_elements_by_xpath("//div[@class='title']")
        for l in AllMovies:
            s=l.text
            try:
                if s==nameMovie:
                    return True
            except WebDriverException:
                print("Выбрался фильм, не соответствующий условию поиска")
                return False

    def check_search_invalid_movie(self):
        self.wait.until(presence_of_element_located((By.XPATH, "//div[@class='content']")))
        AllMovies=self.driver.find_elements_by_xpath("//div[@class='title']")
        try:
            if (len(AllMovies)==0):
                return True
        except WebDriverException:
            print("Выбрался фильм, не соответствующий условию поиска")
            return False

