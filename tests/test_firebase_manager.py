from faker import Faker

from back_end.cloud.firebase_manager import FirebaseManager
from back_end.usertest import UserTest

fake = Faker()


def test_insert_user():
    fm = FirebaseManager()
    user = fm.insert_user(
        name=fake.name(),
        email=fake.email(),
        password=fake.password(6)
    )
    assert user is not None


def test_check_login():
    fm = FirebaseManager()
    pwd = fake.password(6)
    email = fake.email()
    user = fm.insert_user(
        name=fake.name(),
        email=email,
        password=pwd
    )
    assert user is not None
    user2 = fm.check_login(email, pwd)
    assert user2 is not None
    user3 = fm.check_login(email, 'wqergthyjughfdsafg')
    assert user3 is None
    user4 = fm.check_login('dsafghgfwdqefrgewfd', pwd)
    assert user4 is None


def test_insert_user_test():
    fm = FirebaseManager()

    pwd = fake.password(6)
    email = fake.email()
    user = fm.insert_user(
        name=fake.name(),
        email=email,
        password=pwd
    )

    user_test = UserTest(
        user_id=email,
        difficulty='Hard',
        duration='5 min',
        question_operator='/'
    )
    user_test.set_test_results(
        total_score=100,
        user_score=79,
        speed=5,
        number_correct=20,
        number_incorrect=10
    )
    test1 = fm.insert_user_test(user_test)
    assert test1


def test_get_user_tests_for_operator():
    fm = FirebaseManager()
    fm.get_user_tests_for_operator('nicholas.a.petrov@gmail.com', '+')
