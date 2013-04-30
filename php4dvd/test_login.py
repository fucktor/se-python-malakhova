from model.user import User

def test_login(app):
    app.login(User.Admin())
    assert app.is_logged_in()
    app.logout()
    app.is_logout()

