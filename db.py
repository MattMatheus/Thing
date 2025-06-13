import sqlite3

def get_db_connection():
    conn = sqlite3.connect('thing.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    with conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS thing_lists (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL
            )
        ''')
    conn.close()

def get_table_name(list_name):
    import re
    return re.sub(r'\W+', '_', list_name.strip().lower())

def create_list_type(list_name, properties):
    table_name = get_table_name(list_name)
    type_map = {'string': 'TEXT', 'number': 'REAL', 'boolean': 'INTEGER'}
    columns = ', '.join([
        f'"{p[0]}" {type_map.get(p[1], "TEXT")} DEFAULT ' +
        (repr(p[2]) if p[2] != '' and p[1] != 'boolean' else ('1' if p[2] == 'true' and p[1] == 'boolean' else '0' if p[2] == 'false' and p[1] == 'boolean' else 'NULL'))
        for p in properties
    ])
    create_sql = f'CREATE TABLE IF NOT EXISTS {table_name} (id INTEGER PRIMARY KEY AUTOINCREMENT, {columns})'
    conn = get_db_connection()
    try:
        conn.execute(create_sql)
        conn.execute('INSERT INTO thing_lists (name) VALUES (?)', (list_name,))
        conn.commit()
    finally:
        conn.close()

def get_all_lists(filter_value=None):
    conn = get_db_connection()
    if filter_value:
        rows = conn.execute('SELECT * FROM thing_lists WHERE name LIKE ?', (f'%{filter_value}%',)).fetchall()
    else:
        rows = conn.execute('SELECT * FROM thing_lists').fetchall()
    conn.close()
    return rows

def get_list_by_id(list_id):
    conn = get_db_connection()
    row = conn.execute('SELECT * FROM thing_lists WHERE id = ?', (list_id,)).fetchone()
    conn.close()
    return row

def delete_list(list_id, list_name):
    table_name = get_table_name(list_name)
    conn = get_db_connection()
    conn.execute('DELETE FROM thing_lists WHERE id = ?', (list_id,))
    conn.execute(f'DROP TABLE IF EXISTS {table_name}')
    conn.commit()
    conn.close()

def get_list_columns(list_name):
    table_name = get_table_name(list_name)
    conn = get_db_connection()
    columns = [col[1] for col in conn.execute(f'PRAGMA table_info({table_name})').fetchall() if col[1] != 'id']
    conn.close()
    return columns

def get_list_objects(list_name):
    table_name = get_table_name(list_name)
    conn = get_db_connection()
    objects = conn.execute(f'SELECT * FROM {table_name}').fetchall()
    conn.close()
    return objects

def add_object_to_list(list_name, data):
    table_name = get_table_name(list_name)
    columns = get_list_columns(list_name)
    values = [data.get(col, '') for col in columns]
    placeholders = ','.join(['?'] * len(columns))
    conn = get_db_connection()
    conn.execute(f'INSERT INTO {table_name} ({','.join(columns)}) VALUES ({placeholders})', values)
    conn.commit()
    conn.close()

def delete_object_from_list(list_name, obj_id):
    table_name = get_table_name(list_name)
    conn = get_db_connection()
    conn.execute(f'DELETE FROM {table_name} WHERE id = ?', (obj_id,))
    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
