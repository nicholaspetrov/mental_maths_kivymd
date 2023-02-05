import sqlite3
conn = sqlite3.connect('mental_database.db')

# def create_password_table():
#     c = conn.cursor()
#     c.execute('''
#     CREATE TABLE IF NOT EXISTS passwords
#     (
#     [email] TEXT PRIMARY KEY NOT NULL,
#     [password] TEXT NOT NULL
#     )
#     ''')
#     conn.commit()


def insert_into_password_table(email, password):
    pass


def create_connection(db_file='mental.db'):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        conn.execute('''
            CREATE TABLE IF NOT EXISTS users
            (
            [id] INT PRIMARY KEY NOT NULL,
            [name] TEXT NOT NULL,
            [email] TEXT NOT NULL,
            [password] TEXT NOT NULL
            )
            ''')
        print('Database is created')
    except Exception as e:
        print(e)
    finally:
        if conn:
            conn.close()


create_connection()




