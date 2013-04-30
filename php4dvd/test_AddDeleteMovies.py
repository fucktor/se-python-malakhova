from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import *
from config import *
from php4dvd_fixture import driver
import pytest
import time

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

def check_add_movie(driver, title, year):
    try:
        driver.find_element_by_xpath("//div[@class='content']/div[@id='movie']//h2").text==(title+" ("+year+")")
        return True
    except WebDriverException:
        print("Фильм не сохранился")
        return False

def check_movies(driver, name):
    WebDriverWait(driver, 5).until(presence_of_element_located((By.XPATH, "//div[@id='results']")))
    time.sleep(3)
    AllMovies=driver.find_elements_by_xpath("//div[@class='title']")
    ListM=[]
    for l in AllMovies:
        if l.text==name:
            ListM.append(l.text)
    if len(ListM)>-1:
        for i in ListM:
            DeleteMovies(driver, i)
            time.sleep(2)


def check_message_err(driver):
    try:
        WebDriverWait(driver, 5).until(presence_of_element_located((By.XPATH, "//label[@class='error']")))
        return True
    except WebDriverException:
        print("Отсутствует предупреждающее сообщение")
        return False

def DeleteMovies(driver, Name):
    w= WebDriverWait(driver, 10).until(lambda driver : driver.find_element_by_id("results"))
    s=driver.find_element_by_xpath("//div[@class='title'][.='"+Name+"']")
    s.click()
    w= WebDriverWait(driver, 10).until(lambda driver : driver.find_element_by_xpath("//img[@title='Remove']"))
    w.click()
    alert=driver.switch_to_alert()
    alert.accept()
    w= WebDriverWait(driver, 10).until(lambda driver : driver.find_element_by_id("results"))

def check_delete_movie(driver):
    try:
        WebDriverWait(driver, 10).until(invisibility_of_element_located((By.XPATH, "//div[.='Game of thrones']")))
        return True
    except WebDriverException:
        print("Фильм не удалился")
        return False

@pytest.mark.parametrize(("id", "title", "year"),[
    ('1', 'Game of thrones', '2013'),
    ('2', 'Dead fish', '2005'),
    ('3', 'Amazing grace', '2006'),
])

def test_AddMovies_Valid(driver, id, title, year):
    """добавление фильма в коллекцию с валидными данными"""
    driver.get(base_url)
    login(driver,username, password)
    check_movies(driver, title)
    AddMovies(driver, id, title, year)
    w=WebDriverWait(driver, 10).until(lambda driver : driver.find_element_by_xpath("//div[@class='content']/div[@id='movie']"))
    assert check_add_movie(driver, title, year)
    driver.find_element_by_xpath("//a[.='Home']").click()
    w=WebDriverWait(driver, 10).until(lambda driver : driver.find_element_by_id("results"))
    logout(driver)

@pytest.mark.parametrize(("id", "title", "year"),[
    ('ab', 'Pulp Fiction', '1994'),
    ('!@', 'A Beautiful Mind', '2001'),
])

def test_AddMovies_InvalidID(driver, id, title, year):
    """добавление фильма в коллекцию с некорректным ID"""
    driver.get(base_url)
    login(driver,username, password)
    AddMovies(driver, id, title, year)
    assert check_message_err(driver)
    logout(driver)

@pytest.mark.parametrize(("id", "title", "year"),[
    ('4', 'The Green Mile', ''),
    ('5', 'Big fish', '    '),
    ('6', 'The Terminator', 'abcd'),
    ('7', 'True Lies', '_1994'),
])

def test_AddMovies_InvalidYear(driver,id, title, year):
    """добавление фильма в коллекцию с некорректным годом"""
    driver.get(base_url)
    login(driver,username, password)
    AddMovies(driver, id, title, year)
    assert check_message_err(driver)
    logout(driver)


def test_DeleteMovie(driver):
    """удаление фильма из коллекции """
    driver.get(base_url)
    login(driver,username, password)
    time.sleep(2)
    DeleteMovies(driver, Test_Movie)
    assert check_delete_movie(driver)
    logout(driver)

