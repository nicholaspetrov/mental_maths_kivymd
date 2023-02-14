import pytest
from back_end.database_manager import DatabaseManager
from back_end.user import User
from faker import Faker

fake = Faker()


def test_create_tables():
    dbm = DatabaseManager('test.db')
    dbm.create_tables()


def test_insert_user():
    dbm = DatabaseManager('test.db')
    user = User(
        name=fake.name(),
        email=fake.email(),
        password=fake.password(6)
    )
    new_user = dbm.insert_user(user.name, user.email, user.password)
    assert new_user.user_id > 0





