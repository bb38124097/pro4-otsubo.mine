import tkinter as tk
from control.account_manager import AccountManager


class RegistrationInfoView:

    def __init__(self):
        self.manager = AccountManager()

    def display(self):
        window = tk.Toplevel()
        window.title("登録情報")
        window.geometry("300x180")

        user = self.manager.get_user()

        tk.Label(
            window,
            text="登録情報",
            font=("Yu Gothic", 16)
        ).pack(pady=10)

        if user is None:
            tk.Label(window, text="登録されていません").pack()
            return

        tk.Label(
            window,
            text=f"ユーザーID：{user.account_id}"
        ).pack(pady=5)

        tk.Label(
            window,
            text=f"ユーザー名：{user.user_name}"
        ).pack(pady=5)