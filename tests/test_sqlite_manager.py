from faker import Faker

from back_end.db.sqlite_manager import SqliteManager
from back_end.user import User
from back_end.usertest import UserTest


fake = Faker()


def test_create_tables():
    dbm = SqliteManager('test.db')
    dbm.create_tables()


def test_insert_user():
    dbm = SqliteManager('test.db')
    user = User(
        name=fake.name(),
        email=fake.email(),
        password=fake.password(6)
    )
    new_user = dbm.insert_user(user.name, user.email, user.password)
    assert new_user.user_id > 0


def test_insert_test():
    dbm = SqliteManager('test.db')
    user = dbm.insert_user(fake.name(), fake.email(), fake.password(6))
    test = UserTest(
        user_id=user.user_id,
        difficulty='Medium',
        duration=300,
        question_operator='/'
    )
    test.score = 100
    new_test = dbm.insert_test(test)
    assert new_test.test_id > 0






