import tkinter as tk
from boundary.account_registration_view import AccountRegistrationView
from boundary.group_creation_view import GroupCreationView
from boundary.add_member_view import AddMemberView
from boundary.leave_group_view import LeaveGroupView
from control.account_manager import AccountManager


class MainView:

    def display(self):
        self.root = tk.Tk()
        self.root.title("食事予定管理システム")
        self.root.geometry("400x500")

        self.account_manager = AccountManager()

        tk.Label(
            self.root,
            text="食事予定管理システム",
            font=("Yu Gothic", 18)
        ).pack(pady=20)

        # ユーザー登録は常に表示
        tk.Button(
            self.root,
            text="ユーザー登録",
            width=20,
            command=self.open_account_registration_view
        ).pack(pady=5)

        # ユーザー登録済みの場合だけ表示
        if self.account_manager.has_user():

            tk.Button(
                self.root,
                text="グループ作成",
                width=20,
                command=self.open_group_creation_view
            ).pack(pady=5)

            tk.Button(
                self.root,
                text="メンバー追加",
                width=20,
                command=self.open_add_member_view
            ).pack(pady=5)

            tk.Button(
                self.root,
                text="グループ退出",
                width=20,
                command=self.open_leave_group_view
            ).pack(pady=5)

        self.root.mainloop()    
    def open_account_registration_view(self):
        view = AccountRegistrationView()
        view.display()

    def open_group_creation_view(self):
        view = GroupCreationView()
        view.display()

    def open_add_member_view(self):
        view = AddMemberView()
        view.display()

    def open_leave_group_view(self):
        view = LeaveGroupView()
        view.display()