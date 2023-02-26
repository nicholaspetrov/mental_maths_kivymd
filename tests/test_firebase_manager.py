from faker import Faker

from back_end.db.firebase_manager import FirebaseManager

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
