from back_end.usertest import UserTest


class User:

    def __init__(self, name, email, password=None, user_id=None):
        self.name = name
        self.email = email
        self.password = password
        self.user_id = user_id

    def create_test(self, test_id, difficulty, duration, test_type):
        test = UserTest(test_id, difficulty, duration, test_type)

    def start_test(self):
        pass
