import sqlite3

sqliteConnection = conn = sqlite3.connect('sql.db', check_same_thread=False)
cursor = sqliteConnection.cursor()


def create_table():
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
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL
            );''')
    cursor.execute('''         
        CREATE TABLE IF NOT EXISTS reg (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            event_id TEXT NOT NULL,
            user_id TEXT NOT NULL,
            FOREIGN KEY (event_id) REFERENCES events(id),
            FOREIGN KEY (user_id) REFERENCES users(id)
        );''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS feedback (
                   id TEXT,
                   message TEXT NOT NULL);''')
    sqliteConnection.commit()


def insert_event():
    cursor.execute('''
                   
                   INSERT INTO events (id, name) VALUES 

                   ('aiml','AI/ML Workshop'),
                   ('kingoftheweb','King of the Web Workshop'),
                   ('ds','Data Science Workshop'),
                   ('finadv','Financial Advisor Workshop'),
                   ('promptengg','Prompt Engineering Workshop'),
                   ('marketing','Power of Marketing Workshop'),
                   ('wnw','A Whole New World Workshop'),
                   ('rr','Robot Ravager Workshop'),
                   ('techquizshowdown','Tech Quiz Showdown'),
                   ('roborace','Robo Race'),
                   ('codegladiators','Code Gladiators'),
                   ('ctf','Capture the Flag (CTF)'),
                   ('startuppitch','Startup Pitch'),
                   ('bestmanager','Best Manager'),
                   ('adzap','AdZap'),
                   ('bizquiz','Biz Quiz'),
                   ('wallstreetwars','Wall Street Wars'),
                   ('dessertduel','Dessert Duel'),
                   ('maincoursemadness','Main Course Madness'),
                   ('startershowdown','Starter Showdown');''')
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


def get_reg(user_id):
    # Get all events
    cursor.execute(f'''
        SELECT name FROM events,reg where user_id = "{user_id}" and events.id = reg.event_id;
    ''')
    events = cursor.fetchall()
    return events


def insert_feedback(id, message):
    cursor.execute(f'''
        INSERT INTO feedback (id, message)
        VALUES ('{id}', '{message}')
    ''')
    sqliteConnection.commit()
