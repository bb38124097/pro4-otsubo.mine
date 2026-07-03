import sqlite3
from entity.user import User

class AccountManager:
    def __init__(self):
        self.db_name = "meal_schedule.db"
        self.create_table()

    def create_table(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                account_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_name TEXT NOT NULL
            )
        """)

        conn.commit()
        conn.close()

    def check_user_name_length(self, user_name):
        return 0 < len(user_name) <= 20

    def register_user(self, user_name):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO users (user_name) VALUES (?)",
            (user_name,)
        )

        conn.commit()
        account_id = cursor.lastrowid
        conn.close()

        return User(account_id, user_name)
  
    def has_user(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) FROM users")
        count = cursor.fetchone()[0]

        conn.close()
        return count > 0