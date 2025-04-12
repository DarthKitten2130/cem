import sqlite3

sqliteConnection = conn = sqlite3.connect('sql.db', check_same_thread=False)
cursor = sqliteConnection.cursor()


def create_table():
    # Create a table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            phone TEXT UNQIUE NOT NULL,
            branch TEXT NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL DEFAULT 'member'
        );
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            date TEXT NOT NULL,
            time TEXT,
            location TEXT NOT NULL,
            description TEXT,
            dept TEXT,
            type TEXT NOT NULL,
            contact TEXT,
            image TEXT,
            CONSTRAINT fk_contact FOREIGN KEY (contact) REFERENCES users(phone)
            );''')
    cursor.execute('''         
        CREATE TABLE IF NOT EXISTS reg (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            event_id INTEGER NOT NULL,
            user_id TEXT NOT NULL,
            FOREIGN KEY (event_id) REFERENCES events(id),
            FOREIGN KEY (user_id) REFERENCES users(id)
        );''')
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
        SELECT * FROM users WHERE id = "{id}"
    ''')
    user = cursor.fetchone()
    return user


def account_verification(id, password):
    global cursor
    cursor.execute(
        f'SELECT id,password from users where id = "{id}"')
    results = cursor.fetchall()
    acc = {}
    for result in results:
        acc[result[0]] = result[1]

    # Account Does Not Exist
    if id not in [x[0] for x in results]:
        return 'doesNotExist'

    # Entered the Wrong Password
    elif acc[id] != password:
        return 'wrongPassword'

    # Verified
    elif acc[id] == password:
        return 'verified'


def get_events():
    # Get all events
    cursor.execute('''
        SELECT * FROM events
    ''')
    events = cursor.fetchall()
    return events


def insert_reg(event_id, user_id):
    cursor.execute(f'''
        INSERT INTO reg (event_id, user_id)
        VALUES ('{event_id}', '{user_id}')
    ''')
    sqliteConnection.commit()


def get_reg(event_id):
    # Get all events
    cursor.execute(f'''
        SELECT * FROM reg WHERE event_id = "{event_id}"
    ''')
    events = cursor.fetchall()
    return events


def insert_event(name, date, time, location, description, dept, type, contact, image):
    # Insert an event
    cursor.execute(f'''
        INSERT INTO events (name, date, time, location, description, dept, type, contact,image)
        VALUES ('{name}', '{date}', '{time}', '{location}', '{description}', '{dept}', '{type}', '{contact}','{image}')
    ''')
    sqliteConnection.commit()


def get_event(event_id):
    # Get an event
    cursor.execute(f'''
        SELECT * FROM events WHERE id = "{event_id}"
    ''')
    event = cursor.fetchone()
    return event
