import tkinter as tk
from tkinter import messagebox
from control.group_manager import GroupManager


class AddMemberView:
    def __init__(self):
        self.manager = GroupManager()

    def display(self):
        self.window = tk.Toplevel()
        self.window.title("メンバー追加")
        self.window.geometry("400x250")

        tk.Label(
            self.window,
            text="メンバー追加",
            font=("Yu Gothic", 16)
        ).pack(pady=15)

        tk.Label(self.window, text="グループID").pack()
        self.group_id_entry = tk.Entry(self.window, width=30)
        self.group_id_entry.pack(pady=5)

        tk.Label(self.window, text="追加するアカウントID").pack()
        self.account_id_entry = tk.Entry(self.window, width=30)
        self.account_id_entry.pack(pady=5)

        tk.Button(
            self.window,
            text="追加",
            command=self.add_member
        ).pack(pady=15)

    def add_member(self):
        group_id = self.group_id_entry.get().strip()
        account_id = self.account_id_entry.get().strip()

        if not group_id or not account_id:
            messagebox.showerror(
                "エラー",
                "グループIDとアカウントIDを入力してください"
            )
            return

        try:
            self.manager.add_member(int(group_id), int(account_id))

            messagebox.showinfo(
                "追加完了",
                f"アカウントID {account_id} をグループID {group_id} に追加しました"
            )

            self.window.destroy()

        except ValueError:
            messagebox.showerror(
                "エラー",
                "グループIDとアカウントIDは数字で入力してください"
            )
