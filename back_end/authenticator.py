import pyrebase
from loguru import logger

firebaseConfig = {
    "apiKey": "AIzaSyAguPa3Dy_HgzyLn0jF2_TH2j3kgPbsZ-w",
    "authDomain": "mental-maths-test.firebaseapp.com",
    "databaseURL": "https://mental-maths-test-default-rtdb.europe-west1.firebasedatabase.app/",
    "projectId": "mental-maths-test",
    "storageBucket": "mental-maths-test.appspot.com",
    "messagingSenderId": "411203772667",
    "appId": "1:411203772667:web:308ba6709e67a8ea09105e",
    "measurementId": "G-N9RXLCQ8HG"
}

firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()


def login(email, password):
    result = None
    try:
        result = auth.sign_in_with_email_and_password(email, password)
        logger.debug(f'User {email} successfully logged in')
    except Exception as e:
        logger.error(e)
    return result


def signup(email, password, name):
    user_with_name = None
    try:
        user = auth.create_user_with_email_and_password(email, password)
        logger.debug(f'User {email} successfully registered')
        user_with_name = auth.update_profile(id_token=user['idToken'], display_name=name)
    except Exception as e:
        logger.error(e)
    return user_with_name


if __name__ == '__main__':
    # login('nicholas.a.petrov@gmail.com', 'oxford123', 'Nick')
    signup('ivan.s.petrov@gmail.com', 'standrews', 'Daniel')
    login('ivan.s.petrov@gmail.com', 'standrews')

auth.credentials()