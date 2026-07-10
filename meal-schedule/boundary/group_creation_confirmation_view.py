import tkinter as tk
from tkinter import messagebox
from control.group_manager import GroupManager
from control.account_manager import AccountManager


class GroupCreationConfirmationView:
    def __init__(self, group_name):
        self.group_name = group_name
        self.group_manager = GroupManager()
        self.account_manager = AccountManager()

    def display(self):
        self.window = tk.Toplevel()
        self.window.title("グループ作成確認")
        self.window.geometry("400x240")

        tk.Label(
            self.window,
            text="以下の内容でグループを作成しますか？",
            font=("Yu Gothic", 13)
        ).pack(pady=20)

        tk.Label(
            self.window,
            text=f"グループ名：{self.group_name}",
            font=("Yu Gothic", 15, "bold")
        ).pack(pady=15)

        button_frame = tk.Frame(self.window)
        button_frame.pack(pady=20)

        tk.Button(
            button_frame,
            text="登録する",
            width=12,
            command=self.register_group
        ).pack(side=tk.LEFT, padx=10)

        tk.Button(
            button_frame,
            text="戻る",
            width=12,
            command=self.window.destroy
        ).pack(side=tk.LEFT, padx=10)

    def register_group(self):
        user = self.account_manager.get_current_user()

        if user is None:
            messagebox.showerror("エラー", "ユーザー情報が取得できません")
            return

        try:
            group = self.group_manager.create_group(
                user.account_id,
                self.group_name
            )

            messagebox.showinfo(
                "登録完了",
                f"グループを作成しました\n\n"
                f"グループID：{group.group_id}\n"
                f"グループ名：{group.group_name}"
            )

            self.parent_window.destroy()   # グループ名入力画面
            self.window.destroy()          # 確認画面
            self.refresh_callback()

            self.window.destroy()

        except ValueError as e:
            messagebox.showerror("エラー", str(e))