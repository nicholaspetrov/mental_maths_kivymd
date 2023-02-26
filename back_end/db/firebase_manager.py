import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from loguru import logger

from back_end.db.database_manager import DatabaseManager
from back_end.hashing import password_to_denary
from pathlib import Path

from back_end.user import User
from back_end.hashing import login


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

    def insert_test(self, test):
        pass
