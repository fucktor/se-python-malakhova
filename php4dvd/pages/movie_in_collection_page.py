from php4dvd.pages.collection_page import CollectionPage
from selenium.webdriver.common.by import By


class MovieInCollectionPage(CollectionPage):

    @property
    def add_movie_in_collection(self):
        return self.driver.find_element_by_xpath("//div[@class='content']/div[@id='movie']//h2")

    @property
    def delete_movie_button(self):
        return self.driver.find_element_by_xpath("//img[@title='Remove']")

    @property
    def is_this_page(self):
        return self.is_element_visible((By.XPATH, "//div[@class='content']/div[@id='movie']"))