import sqlite3
from loguru import logger

from back_end.hashing import login
from back_end.user import User
from back_end.hashing import password_to_denary
from back_end.utils import get_string_for_datetime
from back_end.cloud.database_manager import DatabaseManager


class SqliteManager(DatabaseManager):
    def __init__(self, db_name='mental_database.cloud'):
        self.db_name = db_name

    def get_db_connection(self):
        # Establishes database connection
        try:
            conn = sqlite3.connect(self.db_name)
            return conn
        except Exception as e:
            logger.error(e)

    def close_db_conn(self, conn):
        # Closes database connection
        if conn is not None:
            conn.close()


    def create_tables(self):
        # For creating users and tests table
        logger.info('Creating database tables...')
        conn = self.get_db_connection()
        conn.execute("PRAGMA foreign_keys = 1")
        c = conn.cursor()
        # Salt and hash stored in table rather than password - harder to hack
        c.execute('''
            CREATE TABLE IF NOT EXISTS users
            (
            [user_id] INTEGER PRIMARY KEY AUTOINCREMENT,
            [name] TEXT NOT NULL,
            [email] TEXT NOT NULL,
            [salt] TEXT NOT NULL,
            [hashed_pwd] TEXT NOT NULL
            )
            ''')

        c.execute('''
                    CREATE TABLE IF NOT EXISTS tests
                    (
                    [test_id] INTEGER PRIMARY KEY AUTOINCREMENT,
                    [difficulty] TEXT NOT NULL,
                    [duration] INTEGER NOT NULL,
                    [test_type] TEXT NOT NULL,
                    [score] INTEGER NOT NULL,
                    [time_created] TEXT NOT NULL,
                    [user_id] INTEGER,
                    FOREIGN KEY (user_id) REFERENCES users(user_id)
                    )
                    ''')

        conn.commit()
        self.close_db_conn(conn)
        logger.info('Database tables created successfully')

    def insert_user(self, name, email, password):
        # Registering account for first time
        logger.info(f'Inserting new user: {email}')
        try:
            # Password run through hashing algorithm which automatically generates a salt and produces a hash
            salt, hashed_pwd = password_to_denary(password)

            conn = self.get_db_connection()
            c = conn.cursor()
            # Check for existing user with same email
            sql = "SELECT * FROM users WHERE email = ?"
            c.execute(sql, (email,))
            rows = c.fetchall()
            emails = []
            for row in rows:
                emails.append(row[2])

            if email in emails:
                logger.info(f'{email} already registered')
                return None
            else:
                # If new email then email and salt, hash from password inserted into users table
                result = c.execute('INSERT INTO users(name, email, salt, hashed_pwd) VALUES(?, ?, ?, ?)', (name, email, salt, hashed_pwd))
                conn.commit()
                logger.info(f'New user registered under {email}')
                # User object created with attributes filled out with inputs from actual user
                user = User(name=name, email=email, user_id=result.lastrowid, password=None)
                return user
        except Exception as e:
            logger.error(e)
        finally:
            self.close_db_conn(conn)

    def check_login(self, email, password):
        # Logging into account
        logger.info(f'Checking login for email: {email}')
        try:
            conn = self.get_db_connection()
            c = conn.cursor()
            sql = "SELECT * FROM users WHERE email = ?"
            c.execute(sql, (email,))
            records = c.fetchall()
            # Salt, hash retrieved - later used to compare salt and hash produced from password inputted by user
            # attempting to log in and if equal (i.e. password entered correctly), user allowed into app
            salt = records[0][3]
            hashed_pwd = records[0][4]
            if hashed_pwd == login(password, salt):
                logger.info(f'Successful log in for email: {email}')
                record = records[0]
                user = User(
                    user_id=record[0],
                    name=record[1],
                    email=record[2]
                )
                return user
            else:
                logger.info(f'Failed to log in for email: {email}')
                return None
        except Exception as e:
            logger.error(e)
        finally:
            self.close_db_conn(conn)


    def check_user_exists(self, email, password):
        pass

    def insert_user_test(self, test):
        try:
            conn = self.get_db_connection()
            c = conn.cursor()
            # Returns time in %Y-%m-%d %H:%M:%S format
            test.time_created = get_string_for_datetime()
            sql = '''
            INSERT INTO tests(difficulty, duration, test_type, score, time_created, user_id) 
            VALUES(?, ?, ?, ?, ?, ?)
            '''
            result = c.execute(
                sql,
                (
                    test.difficulty,
                    test.duration,
                    test.question_operator,
                    test.score,
                    test.time_created,
                    test.user_id
                )
            )
            conn.commit()
            logger.info('Test has successfully been inserted')
            test.test_id = result.lastrowid
            return test
        except Exception as e:
            logger.error(e)
        finally:
            self.close_db_conn(conn)
