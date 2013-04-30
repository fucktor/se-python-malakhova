from model.user import User
from config_data_tests import *
import pytest

@pytest.mark.parametrize(("id", "title", "year"),[
    ('1', 'Game of thrones', '2013'),
    ('2', 'Dead fish', '2005'),
    ('3', 'Amazing grace', '2006'),
])

def test_AddMovies_Valid(app, id, title, year):
    """добавление фильма в коллекцию с валидными данными"""

    app.login(User.Admin())
    app.is_logged_in()
    app.check_movies(title)
    app.AddMovies(id, title, year)
    app.is_add_movie_page()
    app.home_page_return()
    assert app.check_add_movie(title, year)
    app.logout()
    app.is_logout()

@pytest.mark.parametrize(("id", "title", "year"),[
    ('ab', 'Pulp Fiction', '1994'),
    ('!@', 'A Beautiful Mind', '2001'),
])

def test_AddMovies_InvalidID(app, id, title, year):
    """добавление фильма в коллекцию с некорректным ID"""

    app.login(User.Admin())
    app.is_logged_in()
    app.AddMovies(id, title, year)
    assert app.check_message_err()
    app.logout()
    app.is_logout()

@pytest.mark.parametrize(("id", "title", "year"),[
    ('4', 'The Green Mile', ''),
    ('5', 'Big fish', '    '),
    ('6', 'The Terminator', 'abcd'),
    ('7', 'True Lies', '_1994'),
])

def test_AddMovies_InvalidYear(app,id, title, year):
    """добавление фильма в коллекцию с некорректным годом"""
    app.login(User.Admin())
    app.is_logged_in()
    app.AddMovies(id, title, year)
    assert app.check_message_err()
    app.logout()
    app.is_logout()


def test_DeleteMovie(app):
    """удаление фильма из коллекции """
    app.login(User.Admin())
    app.is_logged_in()
    app.DeleteMovies(Test_Movie)
    assert app.check_delete_movie(Test_Movie)
    app.logout()
    app.is_logout()

