import sqlite3

sqliteConnection = conn = sqlite3.connect('sql.db', check_same_thread=False)
cursor = sqliteConnection.cursor()


def create_table():
    # Create a table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            phone TEXT NOT NULL,
            branch TEXT NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    sqliteConnection.commit()


def insert_user(id, name, email, phone, branch, password):
    # Insert a user
    cursor.execute(f'''
        INSERT INTO users (id, name, email, phone, branch, password)
        VALUES ('{id}','{name}', '{email}', '{phone}', '{branch}', '{password}')''')
    sqliteConnection.commit()


def get_user(id):
    # Get a user
    cursor.execute(f'''
        SELECT * FROM users WHERE id = {id}
    ''')
    user = cursor.fetchone()
    return user


def account_verification(username, password):
    global cursor
    cursor.execute(
        f'SELECT username,password from users where username = "{username}"')
    results = cursor.fetchall()
    acc = {}
    for result in results:
        acc[result[0]] = result[1]

    # Account Does Not Exist
    if username not in [x[0] for x in results]:
        return 'doesNotExist'

    # Entered the Wrong Password
    elif acc[username] != password:
        return 'wrongPassword'

    # Verified
    elif acc[username] == password:
        return 'verified'
