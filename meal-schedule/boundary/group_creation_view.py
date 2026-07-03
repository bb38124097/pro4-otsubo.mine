import tkinter as tk
from tkinter import messagebox
from control.group_manager import GroupManager
from control.account_manager import AccountManager

class GroupCreationView:
    def __init__(self):
        self.manager = GroupManager()
        self.account_manager = AccountManager()

    def display(self):
        self.window = tk.Toplevel()
        self.window.title("グループ作成")
        self.window.geometry("400x220")

        tk.Label(
            self.window,
            text="グループ名を入力してください",
            font=("Yu Gothic", 14)
        ).pack(pady=15)

        self.group_name_entry = tk.Entry(self.window, width=30)
        self.group_name_entry.pack(pady=10)

        tk.Button(
            self.window,
            text="作成",
            command=self.create_group
        ).pack(pady=15)

    def create_group(self):
        group_name = self.group_name_entry.get().strip()

        if not self.manager.check_group_name_length(group_name):
            messagebox.showerror(
                "エラー",
                "グループ名は1～20文字で入力してください"
            )
            return

        user = self.account_manager.get_current_user()

        if user is None:
            messagebox.showerror(
                "エラー",
                "ユーザー情報が取得できません。"
            )
            return

        try:
            group = self.manager.create_group(
                user.account_id,
                group_name
            )

            messagebox.showinfo(
                "作成完了",
                f"グループを作成しました\n\n"
                f"グループID：{group.group_id}\n"
                f"グループ名：{group.group_name}"
            )

            self.window.destroy()

        except ValueError as e:
            messagebox.showerror(
                "エラー",
                str(e)
            )
