import tkinter as tk
from boundary.account_registration_view import AccountRegistrationView
from boundary.group_creation_view import GroupCreationView

class MainView:

    def display(self):
        self.root = tk.Tk()
        self.root.title("食事予定管理システム")
        self.root.geometry("400x500")

        tk.Label(
            self.root,
            text="食事予定管理システム",
            font=("Yu Gothic", 18)
        ).pack(pady=20)

        tk.Button(
            self.root,
            text="ユーザー登録",
            width=20,
            command=self.open_account_registration_view
        ).pack(pady=5)

        tk.Button(
            self.root,
            text="グループ作成",
            width=20,
            command=self.open_group_creation_view
        ).pack(pady=5)

        tk.Button(
            self.root,
            text="メンバー追加",
            width=20
        ).pack(pady=5)

        tk.Button(
            self.root,
            text="予定入力",
            width=20
        ).pack(pady=5)

        tk.Button(
            self.root,
            text="終了",
            width=20,
            command=self.root.destroy
        ).pack(pady=20)

        self.root.mainloop()
    
    def open_account_registration_view(self):
        view = AccountRegistrationView()
        view.display()

    def open_group_creation_view(self):
        view = GroupCreationView()
        view.display()