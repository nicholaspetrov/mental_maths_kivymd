from abc import ABC, abstractmethod


class DatabaseManager(ABC):

    def __init__(self, db_name=None):
        self.db_name = db_name
        super().__init__()

    @abstractmethod
    def get_db_connection(self):
        pass

    @abstractmethod
    def close_db_conn(self, conn):
        pass

    @abstractmethod
    def create_tables(self):
        pass

    @abstractmethod
    def insert_user(self, name, email, password):
        pass

    @abstractmethod
    def check_login(self, email, password):
        pass

    @abstractmethod
    def insert_user_test(self, test):
        pass

    @abstractmethod
    def get_user_tests_for_operator(self, email, operator):
        pass
