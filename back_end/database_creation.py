import sqlite3
from back_end.hashing import login


def create_password_table():
    conn = sqlite3.connect('mental_database.db')
    c = conn.cursor()
    c.execute('''
    CREATE TABLE IF NOT EXISTS passwords
    (
    [userid] INTEGER PRIMARY KEY AUTOINCREMENT,
    [email] TEXT NOT NULL,
    [salt] TEXT NOT NULL,
    [hashed_pwd] TEXT NOT NULL
    )
    ''')
    conn.commit()


def insert_into_password_table(email, salt, hashed_pwd):
    conn = sqlite3.connect('mental_database.db')
    c = conn.cursor()
    c.execute("SELECT * FROM passwords")
    rows = c.fetchall()
    accounts = []
    for row in rows:
        print(row)
        accounts.append(row[1])

    if email in accounts:
        # print('Already registered')
        conn.commit()
        return True
    else:
        c.execute('INSERT INTO passwords(email, salt, hashed_pwd) VALUES(?, ?, ?)', (email, salt, hashed_pwd))
        # print('Inserted')
        conn.commit()
        return False


def check_login(email, password):
    conn = sqlite3.connect('mental_database.db')
    c = conn.cursor()
    sql = "SELECT * FROM passwords WHERE email = ?"
    c.execute(sql, (email,))
    record = c.fetchall()
    salt = record[0][2]
    hashed_pwd = record[0][3]
    print(salt)
    print(hashed_pwd)
    if hashed_pwd == login(password, salt):
        conn.commit()
        return True
    else:
        conn.commit()
        return False


def check_user_exists(email, password):
    conn = sqlite3.connect('mental_database.db')
    c = conn.cursor()
    sql = "SELECT * FROM passwords WHERE email = ?"
    c.execute(sql, (email,))
    record = c.fetchall()
    if len(record) == 0:
        conn.commit()
        return False
    else:
        check_login(email, password)
        conn.commit()
        return True






