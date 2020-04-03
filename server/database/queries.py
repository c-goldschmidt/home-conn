
SQL_INIT_DB_QUERIES = ['''
    CREATE TABLE IF NOT EXISTS user (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        lc_name TEXT NOT NULL UNIQUE,
        password TEXT NULL,
        uuid TEXT NOT NULL UNIQUE
    );
''', '''
    CREATE TABLE IF NOT EXISTS chat_message (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        sender_id INTEGER,
        message TEXT NOT NULL,
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (sender_id) 
            REFERENCES user (id)
            ON DELETE CASCADE
    );
''']

SQL_GET_USERS = '''
    SELECT id, name, lc_name, uuid FROM user;
'''

SQL_CREATE_USER = '''
    INSERT INTO user (name, lc_name, password, uuid) VALUES (:name, :lc_name, :password, :uuid);
'''

SQL_GET_USER = '''
    SELECT id, name, uuid FROM user 
    WHERE 
        (name = :name AND password = :password AND :uuid = '_NONE_')
    OR
        (uuid = :uuid and :password = '_NONE_');
'''

SQL_SET_PASSWORD = '''
    UPDATE user set password = :new_pass
    WHERE name = :user_name AND password = :old_pass;
'''

SQL_SELECT_ALL_MESSAGES = '''
    SELECT id, sender_id, message, timestamp 
    FROM chat_message
    ORDER BY timestamp ASC;
'''

SQL_SELECT_MESSAGE = '''
    SELECT id, sender_id, message, timestamp 
    FROM chat_message
    WHERE id=:id;
'''

SQL_CREATE_MESSAGE = '''
    INSERT INTO chat_message (sender_id, message)
    VALUES (:sender_id, :message);
'''

SQL_DELETE_MESSAGE = '''
    DELETE FROM chat_message
    WHERE id = :message_id and sender_id = :sender_id;
'''