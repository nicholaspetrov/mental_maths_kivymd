import pytest
from back_end.database_manager import DatabaseManager
from back_end.user import User


def test_create_tables():
    dbm = DatabaseManager('test.db')
    dbm.create_tables()


def test_insert_user():
    dbm = DatabaseManager('test.db')
    user = User(
        name='Nick',
        email='gmail3',
        password='password123'
    )
    new_user = dbm.insert_user(user.name, user.email, user.password)
    assert new_user.user_id > 0





