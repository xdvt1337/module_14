import sqlite3

connection = sqlite3.connect('not_telegram.db')
cursor = connection.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS Users(
id INTEGER PRIMARY KEY,
username TEXT NOT NULL,
email TEXT NOT NULL,
age INTEGER,
balance INTEGER NOT NULL
)
''')

'''
for i in range(1, 11):
    cursor.execute("INSERT INTO Users (username, email, age, balance) VALUES(?, ?, ?, ?)", (f'User{i}', f'example{i}@gmail.com', i * 10, 1000,))

for a in range(1, 11, 2):
    cursor.execute('UPDATE Users SET balance = 500 WHERE id = ?', (a,))

for b in range(1, 11, 3):
    cursor.execute('DELETE FROM Users WHERE id  = ?', (b,))

cursor.execute("SELECT username, email, age, balance FROM Users WHERE age != 60")
users = cursor.fetchall()

for user in users:
    print(f'Имя: {user[0]} | Почта: {user[1]} | Возраст: {user[2]} | Баланс: {user[3]}')
'''

cursor.execute('DELETE FROM Users WHERE id = ?', (6,))

# COUNT OF ALL USERS ID
cursor.execute('SELECT COUNT(*) FROM Users')
id = cursor.fetchone()[0]

# SUM OF ALL USERS BALANCES
cursor.execute('SELECT SUM(balance) FROM Users')
balances = cursor.fetchone()[0]

# AVG BALANCE OF ALL USERS
print(balances/id)

connection.commit()
connection.close()