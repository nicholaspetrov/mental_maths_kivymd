import pyrebase

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


def login():
    print('Log in...')
    email = input('Enter email: ')
    password = input('Enter password: ')
    try:
        login = auth.sign_in_with_email_and_password(email, password)
        print('Successfully logged in')
    except:
        print('Invalid email or password')
    return


def signup():
    print('Sign up...')
    email = input('Enter email: ')
    password = input('Enter password: ')
    try:
        user = auth.create_user_with_email_and_password(email, password)
        print('Successfully registered')
    except:
        print('Email already exists')
    return


ans = input('Are you a new user? [y/n]: ')

if ans == 'n':
    login()
if ans == 'y':
    signup()

