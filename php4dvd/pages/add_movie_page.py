from php4dvd.pages.collection_page import CollectionPage
from selenium.webdriver.common.by import By


class AddMoviePage(CollectionPage):

    @property
    def id_movie_field(self):
        return self.driver.find_element_by_name("imdbid")

    @property
    def name_movie_field(self):
        return self.driver.find_element_by_name("name")

    @property
    def year_movie_field(self):
        return self.driver.find_element_by_name("year")

    @property
    def save_button(self):
        return self.driver.find_element_by_xpath("//img[@title='Save']")


    @property
    def is_this_page(self):
        return self.is_element_visible((By.XPATH, "//div[@class='content']/div[@class='addmovie']"))


