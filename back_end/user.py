from back_end.usertest import UserTest


class User:

    def __init__(self, name, email, password=None, user_id=None):
        self.name = name
        self.email = email
        self.password = password
        self.user_id = user_id
