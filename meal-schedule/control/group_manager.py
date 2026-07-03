import sqlite3
from entity.group import Group


class GroupManager:
    def __init__(self):
        self.db_name = "meal_schedule.db"
        self.create_table()

    def create_table(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS groups (
                group_id INTEGER PRIMARY KEY AUTOINCREMENT,
                group_name TEXT NOT NULL
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS group_members (
                group_id INTEGER NOT NULL,
                account_id INTEGER NOT NULL
            )
        """)

        conn.commit()
        conn.close()

    def check_group_name_length(self, group_name):
        return 0 < len(group_name) <= 20

    def create_group(self, group_name):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO groups (group_name) VALUES (?)",
            (group_name,)
        )

        conn.commit()
        group_id = cursor.lastrowid
        conn.close()

        return Group(group_id, group_name)

    def add_member(self, group_id, account_id):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO group_members (group_id, account_id) VALUES (?, ?)",
            (group_id, account_id)
        )

        conn.commit()
        conn.close()
    def __init__(self):
        self.db_name = "meal_schedule.db"
        self.create_table()

    def create_table(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS groups (
                group_id INTEGER PRIMARY KEY AUTOINCREMENT,
                group_name TEXT NOT NULL
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS group_members (
                group_id INTEGER NOT NULL,
                account_id INTEGER NOT NULL
            )
        """)

        conn.commit()
        conn.close()

    def check_group_name_length(self, group_name):
        return 0 < len(group_name) <= 20

    def create_group(self, group_name):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO groups (group_name) VALUES (?)",
            (group_name,)
        )

        conn.commit()
        group_id = cursor.lastrowid
        conn.close()

        return Group(group_id, group_name)

    def add_member(self, group_id, account_id):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO group_members (group_id, account_id) VALUES (?, ?)",
            (group_id, account_id)
        )

        conn.commit()
        conn.close()

    def remove_member(self, group_id, account_id):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        cursor.execute(
            "DELETE FROM group_members WHERE group_id = ? AND account_id = ?",
            (group_id, account_id)
        )

        conn.commit()
        conn.close()