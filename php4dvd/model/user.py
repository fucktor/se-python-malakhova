class User(object):

    def __init__(self, username="", passw="", email=""):
        self.username=username
        self.passw=passw
        self.email=email

    @classmethod
    def Admin(cls):
        return cls(username='admin', passw='admin')
