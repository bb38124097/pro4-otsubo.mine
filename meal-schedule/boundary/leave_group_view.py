import tkinter as tk
from tkinter import messagebox
from control.group_manager import GroupManager


class LeaveGroupView:
    def __init__(self):
        self.manager = GroupManager()

        # 仮
        self.group_id = 1
        self.account_id = 1
        self.group_name = "サンプルグループ"

    def display(self):
        self.window = tk.Toplevel()
        self.window.title("グループ退出")
        self.window.geometry("400x220")

        tk.Label(
            self.window,
            text="グループ退出",
            font=("Yu Gothic", 16)
        ).pack(pady=15)

        tk.Label(
            self.window,
            text=f"『{self.group_name}』から退出しますか？",
            font=("Yu Gothic", 12)
        ).pack(pady=20)

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
        self.manager.remove_member(
            self.group_id,
            self.account_id
        )

        messagebox.showinfo(
            "完了",
            f"{self.group_name}から退出しました"
        )

        self.window.destroy()
    def __init__(self):
        self.manager = GroupManager()

    def display(self):
        self.window = tk.Toplevel()
        self.window.title("グループ退出")
        self.window.geometry("400x230")

        tk.Label(
            self.window,
            text="グループ退出",
            font=("Yu Gothic", 16)
        ).pack(pady=15)

        tk.Label(self.window, text="グループID").pack()
        self.group_id_entry = tk.Entry(self.window, width=30)
        self.group_id_entry.pack(pady=5)

        tk.Label(self.window, text="アカウントID").pack()
        self.account_id_entry = tk.Entry(self.window, width=30)
        self.account_id_entry.pack(pady=5)

        tk.Button(
            self.window,
            text="退出",
            command=self.leave_group
        ).pack(pady=15)

    def leave_group(self):
        group_id = self.group_id_entry.get().strip()
        account_id = self.account_id_entry.get().strip()

        if not group_id or not account_id:
            messagebox.showerror("エラー", "グループIDとアカウントIDを入力してください")
            return

        try:
            self.manager.remove_member(int(group_id), int(account_id))

            messagebox.showinfo(
                "退出完了",
                f"アカウントID {account_id} をグループID {group_id} から退出させました"
            )

            self.window.destroy()

        except ValueError:
            messagebox.showerror("エラー", "グループIDとアカウントIDは数字で入力してください")