import sqlite3

def get_db_connection():
    conn = sqlite3.connect('thing.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    with conn:
        # Capsule table
        conn.execute('''
            CREATE TABLE IF NOT EXISTS capsules (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT,
                created_at TEXT NOT NULL
            )
        ''')
        # Thread table
        conn.execute('''
            CREATE TABLE IF NOT EXISTS threads (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                capsule_id INTEGER NOT NULL,
                name TEXT NOT NULL,
                tags TEXT,
                created_at TEXT NOT NULL,
                FOREIGN KEY (capsule_id) REFERENCES capsules(id) ON DELETE CASCADE
            )
        ''')
        # Entry table
        conn.execute('''
            CREATE TABLE IF NOT EXISTS entries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                thread_id INTEGER NOT NULL,
                timestamp TEXT NOT NULL,
                properties TEXT,
                FOREIGN KEY (thread_id) REFERENCES threads(id) ON DELETE CASCADE
            )
        ''')
    conn.close()

# Capsule CRUD

def create_capsule(name, description, created_at):
    conn = get_db_connection()
    cur = conn.execute('INSERT INTO capsules (name, description, created_at) VALUES (?, ?, ?)', (name, description, created_at))
    conn.commit()
    capsule_id = cur.lastrowid
    conn.close()
    return capsule_id

def get_all_capsules():
    conn = get_db_connection()
    rows = conn.execute('SELECT * FROM capsules').fetchall()
    conn.close()
    return rows

def get_capsule_by_id(capsule_id):
    conn = get_db_connection()
    row = conn.execute('SELECT * FROM capsules WHERE id = ?', (capsule_id,)).fetchone()
    conn.close()
    return row

def delete_capsule(capsule_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM capsules WHERE id = ?', (capsule_id,))
    conn.commit()
    conn.close()

# Thread CRUD

def create_thread(capsule_id, name, tags, created_at):
    conn = get_db_connection()
    cur = conn.execute('INSERT INTO threads (capsule_id, name, tags, created_at) VALUES (?, ?, ?, ?)', (capsule_id, name, tags, created_at))
    conn.commit()
    thread_id = cur.lastrowid
    conn.close()
    return thread_id

def get_threads_by_capsule(capsule_id):
    conn = get_db_connection()
    rows = conn.execute('SELECT * FROM threads WHERE capsule_id = ?', (capsule_id,)).fetchall()
    conn.close()
    return rows

def get_thread_by_id(thread_id):
    conn = get_db_connection()
    row = conn.execute('SELECT * FROM threads WHERE id = ?', (thread_id,)).fetchone()
    conn.close()
    return row

def delete_thread(thread_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM threads WHERE id = ?', (thread_id,))
    conn.commit()
    conn.close()

# Entry CRUD

def create_entry(thread_id, timestamp, properties_json):
    conn = get_db_connection()
    cur = conn.execute('INSERT INTO entries (thread_id, timestamp, properties) VALUES (?, ?, ?)', (thread_id, timestamp, properties_json))
    conn.commit()
    entry_id = cur.lastrowid
    conn.close()
    return entry_id

def get_entries_by_thread(thread_id):
    conn = get_db_connection()
    rows = conn.execute('SELECT * FROM entries WHERE thread_id = ?', (thread_id,)).fetchall()
    conn.close()
    return rows

def get_entry_by_id(entry_id):
    conn = get_db_connection()
    row = conn.execute('SELECT * FROM entries WHERE id = ?', (entry_id,)).fetchone()
    conn.close()
    return row

def delete_entry(entry_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM entries WHERE id = ?', (entry_id,))
    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
