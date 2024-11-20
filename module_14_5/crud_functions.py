import sqlite3

def initiate_db():
    connection = sqlite3.connect("Products.db")
    cursor = connection.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Products (
        id INTEGER PRIMARY KEY,
        title TEXT NOT NULL,
        description TEXT,
        price INTEGER NOT NULL
    )
    ''')

    connection1 = sqlite3.connect("database.db")
    cursor = connection1.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Users (
        id INTEGER PRIMARY KEY,
        username TEXT NOT NULL,
        email TEXT NOT NULL,
        age INTEGER NOT NULL,
        balance INTEGER NOT NULL
    )
    ''')

    connection1.commit()
    connection1.close()


def get_all_products():
    connection = sqlite3.connect("Products.db")
    cursor = connection.cursor()

    cursor.execute('SELECT * FROM Products')
    products = cursor.fetchall()

    connection.close()
    return products

def add_user(username, email, age):
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    cursor.execute('''
            INSERT INTO Users (username, email, age, balance)
            VALUES (?, ?, ?, 1000)
        ''', (username, email, age))
    connection.commit()
    connection.close()

def is_included(username):
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()

    cursor.execute('SELECT * FROM Users WHERE username = ?', (username,))
    user = cursor.fetchone()
    connection.close()

    return user is not None