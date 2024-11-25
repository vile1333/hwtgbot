import sqlite3

class Database:
    def __init__(self, path: str):
        self.path = path

    def create_tables(self):
        with sqlite3.connect(self.path) as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS reviews(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name1 TEXT,
                    phone_number TEXT,
                    ig_username TEXT,
                    visit_date TEXT,
                    food_rating INTEGER,
                    cleanliness_rating INTEGER,
                    extra_comment TEXT
                )
                """
            )
            conn.commit()
    def execute(self, query: str, params: tuple = ()):
        with sqlite3.connect(self.path) as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()
            return cursor.fetchall()

database = Database("database.sqlite")
database.create_tables()
