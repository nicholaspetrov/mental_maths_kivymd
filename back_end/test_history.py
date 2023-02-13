from back_end.user import User
from back_end.test import Test
import datetime


class TestHistory:
    def __init__(self, user_id, test_id):
        self.user_id = user_id
        self.test_id = test_id
        self.timestamp = datetime.datetime.utcnow().strftime('%m/%d/%Y %H:%M:%S')
