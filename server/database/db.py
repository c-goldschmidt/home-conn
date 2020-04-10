import sqlite3

from server.database.queries import SQL_INIT_DB_QUERIES


class CursorContext:
    def __init__(self, conn):
        self.conn = conn
        self.count = 0
        self.cursor = None

    def __enter__(self):
        self.cursor = self.cursor or self.conn.cursor()
        self.count += 1
        return self.cursor

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.count -= 1
        if self.count == 0:
            self.cursor.close()
            self.cursor = None


class Database:
    def __init__(self, config):
        self.conn = sqlite3.connect(config.server.get('database', 'database.db'))
        self._cursor = CursorContext(self.conn)

        for query in SQL_INIT_DB_QUERIES:
            self.execute(query, commit=True)

    def execute_fetch_one(self, query, params=None, commit=False):
        with self.cursor() as cur:
            cur.execute(query, params or {})

            if commit:
                self.commit()

            return cur.fetchone()

    def execute_fetch_all(self, query, params=None, commit=False):
        with self.cursor() as cur:
            cur.execute(query, params or {})

            if commit:
                self.commit()

            return cur.fetchall()

    def execute(self, query, params=None, commit=False):
        with self.cursor() as cur:
            cur.execute(query, params or {})

            if commit:
                self.commit()

            return cur.lastrowid

    def commit(self):
        self.conn.commit()

    def cursor(self):
        return self._cursor
