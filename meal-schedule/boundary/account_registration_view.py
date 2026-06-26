import tkinter as tk
from tkinter import messagebox
from control.account_manager import AccountManager

class AccountRegistrationView:

    def __init__(self):
        self.manager = AccountManager()

    def display(self):
        self.window = tk.Toplevel()
        self.window.title("ユーザー登録")

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
        else:
            messagebox.showerror(
                "エラー",
                "ユーザー名は1～20文字で入力してください"
            )