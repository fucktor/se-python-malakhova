from model.user import User
from config_data_tests import *
import pytest

def test_SearchMovies1(app):
    """поиск существующего в коллекции фильма"""
    app.login(User.Admin())
    app.is_logged_in()
    for i in range(1,4):
        app.check_add_movies_search(Movies['movie'+str(i)][0], Movies['movie'+str(i)][1], Movies['movie'+str(i)][2])
    app.search_movie(Test_Movie2)
    assert app.check_search_valid_movie(Test_Movie2)
    app.logout()
    app.is_logout()

def test_SearchMovies2(app):
    """поиск несуществующего в коллекции фильма"""
    app.login(User.Admin())
    app.is_logged_in()
    app.search_movie(Test_Movie3)
    assert app.check_search_invalid_movie()
    app.logout()
    app.is_logout()




