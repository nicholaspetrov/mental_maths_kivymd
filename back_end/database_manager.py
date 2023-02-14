import sqlite3
from back_end.hashing import login
from back_end.test import Test
from back_end.user import User
from back_end.test_history import TestHistory
from back_end.hashing import password_to_denary
from loguru import logger


class DatabaseManager:
    def __init__(self, db_name='mental_database.db'):
        self.db_name = db_name

    def get_db_connection(self):
        try:
            conn = sqlite3.connect(self.db_name)
            return conn
        except Exception as e:
            logger.error(e)

    def close_db_conn(self, conn):
        if conn is not None:
            conn.close()


    def create_tables(self):
        logger.info('Creating database tables...')
        conn = self.get_db_connection()
        conn.execute("PRAGMA foreign_keys = 1")
        c = conn.cursor()
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
                    [num_q] INTEGER NOT NULL,
                    [num_correct_a] INTEGER NOT NULL,
                    [timestamp] TEXT NOT NULL,
                    [user_id] INTEGER,
                    FOREIGN KEY (user_id) REFERENCES users(user_id)
                    )
                    ''')

        # c.execute('''
        #             CREATE TABLE IF NOT EXISTS test_history
        #             (
        #             test_history_id INTEGER PRIMARY KEY AUTOINCREMENT,
        #             timestamp TEXT NOT NULL,
        #             user_id INTEGER NOT NULL,
        #             test_id INTEGER NOT NULL
        #             )
        #             ''')
        conn.commit()
        self.close_db_conn(conn)
        logger.info('Database tables created successfully')

    def insert_user(self, name, email, password):
        logger.info(f'Inserting new user: {email}')

        salt, hashed_pwd = password_to_denary(password)

        conn = self.get_db_connection()
        c = conn.cursor()
        sql = "SELECT * FROM users WHERE email = ?"
        c.execute(sql, (email,))
        rows = c.fetchall()
        emails = []
        for row in rows:
            emails.append(row[2])

        if email in emails:
            logger.info(f'{email} already registered')
            self.close_db_conn(conn)
            return None
        else:
            result = c.execute('INSERT INTO users(name, email, salt, hashed_pwd) VALUES(?, ?, ?, ?)', (name, email, salt, hashed_pwd))
            conn.commit()
            self.close_db_conn(conn)
            logger.info(f'New user registered under {email}')
            user = User(name=name, email=email, user_id=result.lastrowid, password=None)
            return user

    def check_login(self, email, password):
        logger.info(f'Checking login for email: {email}')
        conn = self.get_db_connection()
        c = conn.cursor()
        sql = "SELECT * FROM users WHERE email = ?"
        c.execute(sql, (email,))
        record = c.fetchall()
        salt = record[0][3]
        hashed_pwd = record[0][4]
        if hashed_pwd == login(password, salt):
            logger.info(f'Successful log in for email: {email}')
            # user = User()
            self.close_db_conn(conn)
            return True
        else:
            logger.info(f'Failed to log in for email: {email}')
            self.close_db_conn(conn)
            return False

    def check_user_exists(self, email, password):
        try:
            conn = self.get_db_connection()
            c = conn.cursor()
            sql = "SELECT * FROM users WHERE email = ?"
            c.execute(sql, (email,))
            record = c.fetchall()
            self.close_db_conn(conn)
            if len(record) == 0:
                return False
            return self.check_login(email, password)
        except Exception as e:
            self.close_db_conn(conn)
            return False

    def insert_test(self, test):
        try:
            conn = self.get_db_connection()
            c = conn.cursor()
            sql = '''
            INSERT INTO tests(difficulty, duration, test_type, num_q, num_correct_a) 
            VALUES(?, ?, ?, ?, ?)
            '''
            c.execute(
                sql,
                (
                    test.difficulty,
                    test.duration,
                    test.question_operator,
                    test.number_q,
                    test.number_correct_a
                )
            )
            conn.commit()
            self.close_db_conn(conn)
            logger.info('Test has successfully been inserted')
        except Exception as e:
            self.close_db_conn(conn)
            logger.error(e)


    def insert_test_history(self, test_history):
        try:
            conn = self.get_db_connection()
            c = conn.cursor()
            sql = '''
            INSERT INTO test_history(timestamp, user_id, test_id) 
            VALUES(?, ?, ?)
            '''
            c.execute(
                sql,
                (
                    test_history.timestamp,
                    test_history.user_id,
                    test_history.test_id
                )
            )
            conn.commit()
            self.close_db_conn(conn)
            logger.info('Test has successfully been inserted')
        except Exception as e:
            self.close_db_conn(conn)
            logger.error(e)




