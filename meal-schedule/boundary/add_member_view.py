import tkinter as tk
from tkinter import messagebox
from control.group_manager import GroupManager


class AddMemberView:
    def __init__(self):
        self.manager = GroupManager()
        self.current_account_id = 1  # 仮。あとでログイン中ユーザーIDにする

    def display(self):
        self.window = tk.Toplevel()
        self.window.title("メンバー追加")
        self.window.geometry("400x220")

        tk.Label(
            self.window,
            text="メンバー追加",
            font=("Yu Gothic", 16)
        ).pack(pady=15)

        tk.Label(self.window, text="追加するアカウントID").pack()

        self.account_id_entry = tk.Entry(self.window, width=30)
        self.account_id_entry.pack(pady=5)

        tk.Button(
            self.window,
            text="追加",
            command=self.add_member
        ).pack(pady=15)

    def add_member(self):
        account_id = self.account_id_entry.get().strip()

        if not account_id:
            messagebox.showerror("エラー", "アカウントIDを入力してください")
            return

        try:
            group_id = self.manager.get_user_group_id(self.current_account_id)

            if group_id is None:
                messagebox.showerror("エラー", "自分が所属しているグループがありません")
                return

            self.manager.add_member(group_id, int(account_id))

            messagebox.showinfo(
                "追加完了",
                f"アカウントID {account_id} を自分のグループに追加しました"
            )

            self.window.destroy()

        except ValueError:
            messagebox.showerror("エラー", "アカウントIDは数字で入力してください")