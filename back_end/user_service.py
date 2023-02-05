import sqlite3


def user_login(email, password):
    print('User service: user_login')


def insert_user(name, email, password):
    try:
        connection = sqlite3.connect('sample.db')
        c = connection.cursor()
        sql_statement = 'INSERT INTO users(name, email, password) VALUES(?, ?, ?)'
        c.execute(sql_statement, (name, email, password))
        connection.commit()
        print('New user is created')
    except Exception as e:
        print('Error: ', e)

