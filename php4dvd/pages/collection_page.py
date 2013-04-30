from php4dvd.pages.page import Page
from selenium.webdriver.common.by import By


class CollectionPage(Page):

    @property
    def logout_button(self):
        return self.driver.find_element_by_link_text("Log out")

    @property
    def add_movie_button(self):
        return self.driver.find_element_by_xpath("//img[@title='Add movie']")

    @property
    def all_movies(self):
        return self.driver.find_elements_by_xpath("//div[@class='title']")

    @property
    def table_movies(self):
        return self.driver.find_elements_by_id("results")

    @property
    def home_link(self):
        return self.driver.find_element_by_link_text("Home")

    @property
    def search_field(self):
        return self.driver.find_element_by_id("q")


    @property
    def is_this_page(self):
        return self.is_element_visible((By.CSS_SELECTOR, "nav"))


