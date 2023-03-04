import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from loguru import logger

from back_end.db.database_manager import DatabaseManager
from back_end.hashing import password_to_denary
from pathlib import Path

from back_end.user import User
from back_end.hashing import login
from back_end.usertest import UserTest
from back_end.utils import get_string_for_datetime, get_datetime_for_string


class FirebaseManager(DatabaseManager):
    def __init__(self, db_name=None):
        super().__init__()
        config_file = Path(__file__).resolve().parent / "mental-maths-firebase.json"
        self.cred = credentials.Certificate(config_file)
        firebase_admin.initialize_app(self.cred)
        self.db = firestore.client()
        # Connection established

    def get_db_connection(self):
        pass

    def close_db_conn(self, conn):
        pass

    def create_tables(self):
        pass

    def insert_user(self, name, email, password):
        user = None

        # Collects all users with specific email from 'users' collection
        user_ref = self.db.collection('users').document(email)
        check_email = user_ref.get()
        # If email already used for registration then
        if check_email.exists:
            logger.info(f'{email} already registered')
            return None
        try:
            users = self.db.collection("users")
            # password fed into password_to_denary method which returns a salt and hashed_pwd
            salt, hashed_pwd = password_to_denary(password)

            # Name input and password_to_denary outputs stored in database (more specifically in 'users' collection)
            result = users.document(email).set({
                'name': name,
                'hash': hashed_pwd,
                'salt': salt
            })
            # User object created with name and email parameters now filled
            user = User(name, email)
        except Exception as e:
            logger.error(e)
        finally:
            return user

    def check_login(self, email, password):
        # All users with email selected
        user_ref = self.db.collection('users').document(email)
        user = user_ref.get()
        # If user is empty, then user doesn't exist
        if not user.exists:
            logger.info(f'Failed to log in for email: {email}')
            return None
        # Salt and hash retrieved from users collection
        fields = user.to_dict()
        salt = fields['salt']
        hashed_pwd = fields['hash']
        if hashed_pwd == login(password, salt):
            # Inputted password and retrieved salt run through the same hashing algorithm used in registration and if
            # equal, then user logs in
            logger.info(f'Successful log in for email: {email}')
            # User object created
            return User(
                user_id=email,
                name=fields['name'],
                email=email
            )
        logger.info(f'Incorrect password for: {email}')
        return None

    def check_password(self, email, password):
        # For resetting User's password in settings of App
        user_ref = self.db.collection('users').document(email)
        user = user_ref.get()
        fields = user.to_dict()
        salt = fields['salt']
        hashed_pwd = fields['hash']
        # If password is correct, then user is allowed to reset
        if hashed_pwd == login(password, salt):
            return True
        else:
            return False

    def reset_password(self, email, password):
        # Password set to newly inputted password, name stays the same under the same email document in users collection
        user_ref = self.db.collection('users').document(email)
        users = self.db.collection('users')
        user = user_ref.get()
        fields = user.to_dict()
        salt, hashed_pwd = password_to_denary(password)
        result = users.document(email).set({
            'name': fields['name'],
            'hash': hashed_pwd,
            'salt': salt
        })

    def insert_user_test(self, user_test: UserTest):
        # Test inserted
        user_ref = self.db.collection('users').document(user_test.user_id)
        user_test = self.db.collection('tests').document().set({
            'user_id': user_ref,
            'difficulty': user_test.difficulty,
            'duration': user_test.duration,
            'question_operator': user_test.question_operator,
            'total_score': user_test.total_score,
            'user_score': user_test.user_score,
            'speed': user_test.speed,
            'number_incorrect': user_test.number_incorrect,
            'number_correct': user_test.number_correct,
            'mixed_mode': user_test.mixed_mode,
            'timestamp': get_string_for_datetime()
        })
        return user_test

    def get_user_tests_for_operator(self, email, operator):
        # For generating graph at end of test
        user_ref = self.db.collection('users').document(email)
        test_ref = self.db.collection('tests').where(
            'user_id', '==', user_ref
        ).where(
            'question_operator', '==', operator
        ).order_by(
            "timestamp"
        ).stream()

        result = []
        for test in test_ref:
            user_test = UserTest(
                user_id=test.get('user_id'),
                question_operator=test.get('question_operator'),
                duration=test.get('duration'),
                difficulty=test.get('difficulty'),
            )
            user_test.set_test_results(
                speed=test.get('speed'),
                time_created=get_datetime_for_string(test.get('timestamp'))
            )
            result.append(user_test)
        # result consisting of user_test is later used to retrieve user's speed and timestamp/date they did the test
        # this is then used to display a graph at the end of the test, y-axis = speed, x-axis=date
        return result

    def get_leaderboard(self, operator):
        # Given the operator, a leaderboard is constructed consisting of names of the users that did it and their speed
        test_ref = self.db.collection('tests').where('question_operator', '==', operator).stream()
        leaderboard = {}
        for test in test_ref:
            email = test.get('user_id').get().to_dict()['name']
            speed = test.get('speed')
            if email in leaderboard:
                if speed > leaderboard[email]:
                    leaderboard.update({email: speed})
                else:
                    pass
            else:
                leaderboard[email] = speed
        return leaderboard
