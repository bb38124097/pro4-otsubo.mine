import tkinter as tk
from tkinter import messagebox
from control.account_manager import AccountManager

class AccountRegistrationView:

    def __init__(self):
        self.manager = AccountManager()

    def display(self):
        self.window = tk.Toplevel()

        tk.Label(self.window, text="ユーザー名").pack()

        self.user_name_entry = tk.Entry(self.window)
        self.user_name_entry.pack()

        tk.Button(
            self.window,
            text="登録",
            command=self.register_user
        ).pack()

    def register_user(self):
        user_name = self.user_name_entry.get()

        if self.manager.check_user_name_length(user_name):
            self.manager.register_user(user_name)
            messagebox.showinfo("完了", "登録しました")
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