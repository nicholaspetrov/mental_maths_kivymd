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

    def get_db_connection(self):
        pass

    def close_db_conn(self, conn):
        pass

    def create_tables(self):
        pass

    def insert_user(self, name, email, password):
        user = None

        user_ref = self.db.collection('users').document(email)
        check_email = user_ref.get()
        if check_email.exists:
            logger.info(f'{email} already registered')
            return None
        try:
            users = self.db.collection("users")
            salt, hashed_pwd = password_to_denary(password)

            result = users.document(email).set({
                'name': name,
                'hash': hashed_pwd,
                'salt': salt
            })
            user = User(name, email)
        except Exception as e:
            logger.error(e)
        finally:
            return user

    def check_login(self, email, password):
        user_ref = self.db.collection('users').document(email)
        user = user_ref.get()
        if not user.exists:
            logger.info(f'Failed to log in for email: {email}')
            return None
        fields = user.to_dict()
        salt = fields['salt']
        hashed_pwd = fields['hash']
        if hashed_pwd == login(password, salt):
            logger.info(f'Successful log in for email: {email}')
            return User(
                user_id=email,
                name=fields['name'],
                email=email
            )
        logger.info(f'Incorrect password for: {email}')
        return None

    def insert_user_test(self, user_test: UserTest):
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
            # print(f'{test.id} => {test.to_dict()}')
        return result

    def get_addition_leaderboard(self, operator):
        test_ref = self.db.collection('tests').where('question_operator', '==', operator).stream()
        addition_leaderboard = {}
        for test in test_ref:
            addition_leaderboard[test.get('user_id')] = test.get('speed')
        return addition_leaderboard

    def get_subtraction_leaderboard(self, operator):
        test_ref = self.db.collection('tests').where('question_operator', '==', operator).stream()
        subtraction_leaderboard = {}
        for test in test_ref:
            subtraction_leaderboard[test.get('user_id')] = test.get('speed')
        return subtraction_leaderboard

    def get_division_leaderboard(self, operator):
        test_ref = self.db.collection('tests').where('question_operator', '==', operator).stream()
        division_leaderboard = {}
        for test in test_ref:
            division_leaderboard[test.get('user_id')] = test.get('speed')
        return division_leaderboard

    def get_multiplication_leaderboard(self, operator):
        test_ref = self.db.collection('tests').where('question_operator', '==', operator).stream()
        multiplication_leaderboard = {}
        for test in test_ref:
            multiplication_leaderboard[test.get('user_id')] = test.get('speed')
        return multiplication_leaderboard
