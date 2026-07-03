import tkinter as tk
from tkinter import messagebox
from control.group_manager import GroupManager
from control.account_manager import AccountManager


class LeaveGroupView:
    def __init__(self):
        self.manager = GroupManager()
        self.account_manager = AccountManager()

    def display(self):
        self.window = tk.Toplevel()
        self.window.title("グループ退出")
        self.window.geometry("400x200")

        tk.Label(
            self.window,
            text="グループから退出しますか？",
            font=("Yu Gothic", 16)
        ).pack(pady=25)

        tk.Button(
            self.window,
            text="退出する",
            command=self.leave_group
        ).pack(pady=10)

        tk.Button(
            self.window,
            text="キャンセル",
            command=self.window.destroy
        ).pack()

    def leave_group(self):
        user = self.account_manager.get_current_user()

        if user is None:
            messagebox.showerror("エラー", "ユーザー情報が取得できません")
            return

        group_id = self.manager.get_user_group_id(user.account_id)

        if group_id is None:
            messagebox.showerror("エラー", "所属しているグループがありません")
            return

        self.manager.remove_member(group_id, user.account_id)

        messagebox.showinfo("退出完了", "グループから退出しました")
        self.window.destroy()