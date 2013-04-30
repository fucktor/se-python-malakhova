from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import *
from selenium.webdriver.common.keys import Keys
from config import *
from php4dvd_fixture import driver
import time
import pytest

def login(driver, username, passw):
    l=driver.find_element_by_id("username")
    l.clear()
    l.send_keys(username)
    p=driver.find_element_by_name("password")
    p.clear()
    p.send_keys(password)
    driver.find_element_by_name("submit").click()
    w= WebDriverWait(driver, 10).until(lambda driver : driver.find_element_by_xpath("//div[@class='center']//li[4]/*[.='Log out']"))

def logout(driver):
    driver.find_element_by_xpath("//div[@class='center']//li[4]/*[.='Log out']").click()
    alert=driver.switch_to_alert()
    alert.accept()
    WebDriverWait(driver, 10).until(lambda driver : driver.find_element_by_id("login"))

def check_add_movies(driver):
    time.sleep(3)
    AllMovies=driver.find_elements_by_xpath("//div[@class='title']")
    ListMovies=[]
    for l in AllMovies:
        ListMovies.append(l.text)
    for i in range(1,4):
        if not (Movies['movie'+str(i)][1]) in ListMovies:
            AddMovies(driver, Movies['movie'+str(i)][0], Movies['movie'+str(i)][1], Movies['movie'+str(i)][2])

def AddMovies(driver, idMovie, nameMovie, yearMovie):
    w= WebDriverWait(driver, 10).until(lambda driver : driver.find_element_by_xpath("//img[@title='Add movie']"))
    w.click()
    w=WebDriverWait(driver, 10).until(lambda driver : driver.find_element_by_xpath("//div[@class='content']/div[@class='addmovie']"))
    f=driver.find_element_by_name("imdbid")
    f.clear()
    f.send_keys(idMovie)
    p=driver.find_element_by_name("name")
    p.clear()
    p.send_keys(nameMovie)
    t=driver.find_element_by_name("year")
    t.clear()
    t.send_keys(yearMovie)
    driver.find_element_by_xpath("//img[@title='Save']").click()
    driver.find_element_by_xpath("//a[.='Home']").click()
    w=WebDriverWait(driver, 10).until(lambda driver : driver.find_element_by_id("results"))

def search_movie(driver, nameMovie):
    s=driver.find_element_by_id("q")
    s.clear()
    s.send_keys(nameMovie)
    s.send_keys(Keys.RETURN)
    WebDriverWait(driver, 10).until(invisibility_of_element_located((By.XPATH, "//div[@class='title'][.!='"+nameMovie+"']")))


def check_search_valid_movie(driver, title, nameMovie):
    try:
        if title==nameMovie:
            return True
    except WebDriverException:
        print("Выбрался фильм, не соответствующий условию поиска")
        return False

def check_search_invalid_movie(driver, s):
    try:
        if (s==0):
            return True
    except WebDriverException:
        print("Выбрался фильм, не соответствующий условию поиска")
        return False


def test_SearchMovies1(driver):
    """поиск существующего в коллекции фильма"""
    driver.get(base_url)
    login(driver,username, password)
    check_add_movies(driver)
    search_movie(driver, Test_Movie2)
    AllMovies=driver.find_elements_by_xpath("//div[@class='title']")
    for l in AllMovies:
        s=l.text
        assert check_search_valid_movie(driver, s, Test_Movie2)
    logout(driver)


def test_SearchMovies2(driver):
    """поиск несуществующего в коллекции фильма"""
    driver.get(base_url)
    login(driver,username, password)
    search_movie(driver, Test_Movie3)
    AllMovies=driver.find_elements_by_xpath("//div[@class='title']")
    assert check_search_invalid_movie(driver, len(AllMovies))
    logout(driver)




