import tkinter as tk
import calendar
from datetime import date
from control.group_manager import GroupManager

from boundary.group_creation_view import GroupCreationView
from boundary.add_member_view import AddMemberView
from boundary.leave_group_view import LeaveGroupView
from boundary.date_detail_view import DateDetailView
from control.account_manager import AccountManager
from boundary.account_registration_view import AccountRegistrationView

class MainView:

    def display(self):
        self.root = tk.Tk()
        self.root.title("食事予定管理システム")
        self.root.geometry("520x720")

        self.account_manager = AccountManager()
        self.group_manager = GroupManager()

        self.year = date.today().year
        self.month = date.today().month

        tk.Label(
            self.root,
            text="食事予定管理システム",
            font=("Yu Gothic", 18)
        ).pack(pady=10)

        if not self.account_manager.has_user():
            self.create_registration_form()

        else:
            self.create_menu_buttons()
            self.calendar_area = tk.Frame(self.root)
            self.calendar_area.pack()
            self.create_calendar()

        self.root.mainloop()

    def create_menu_buttons(self):
        frame = tk.Frame(self.root)
        frame.pack(pady=5)

        user = self.account_manager.get_current_user()
        has_group = False

        if user is not None:
            has_group = self.group_manager.has_group(user.account_id)

        tk.Button(
            frame,
            text="登録情報",
            width=14,
            command=self.open_registration_info_view
        ).grid(row=0, column=0, padx=5, pady=5)

        if not has_group:
            tk.Button(
                frame,
                text="グループ作成",
                width=14,
                command=self.open_group_creation_view
            ).grid(row=0, column=1, padx=5, pady=5)

        if has_group:
            tk.Button(
                frame,
                text="メンバー追加",
                width=14,
                command=self.open_add_member_view
            ).grid(row=0, column=1, padx=5, pady=5)

            tk.Button(
                frame,
                text="グループ退出",
                width=14,
                command=self.open_leave_group_view
            ).grid(row=0, column=2, padx=5, pady=5)
            
    def create_calendar(self):
        for widget in self.calendar_area.winfo_children():
            widget.destroy()

        header = tk.Frame(self.calendar_area)
        header.pack(pady=10)

        prev_month = 12 if self.month == 1 else self.month - 1
        next_month = 1 if self.month == 12 else self.month + 1

        tk.Button(
            header,
            text=f"{prev_month}月",
            command=self.previous_month,
            width=6
        ).pack(side=tk.LEFT, padx=15)

        tk.Label(
            header,
            text=f"{self.year}年 {self.month}月",
            font=("Yu Gothic", 16, "bold")
        ).pack(side=tk.LEFT, padx=20)

        tk.Button(
            header,
            text=f"{next_month}月",
            command=self.next_month,
            width=6
        ).pack(side=tk.LEFT, padx=15)

        calendar_frame = tk.Frame(self.calendar_area)
        calendar_frame.pack()

        days = ["月", "火", "水", "木", "金", "土", "日"]

        for col, day_name in enumerate(days):
            tk.Label(
                calendar_frame,
                text=day_name,
                width=6,
                font=("Yu Gothic", 10, "bold")
            ).grid(row=0, column=col, padx=2, pady=2)

        month_calendar = calendar.monthcalendar(self.year, self.month)

        for row, week in enumerate(month_calendar, start=1):
            for col, day in enumerate(week):
                if day == 0:
                    tk.Label(calendar_frame, text="", width=6).grid(row=row, column=col)
                else:
                    target_date = f"{self.year}-{self.month:02d}-{day:02d}"

                    tk.Button(
                        calendar_frame,
                        text=str(day),
                        width=6,
                        command=lambda d=target_date: self.show_date_detail(d)
                    ).grid(row=row, column=col, padx=2, pady=2)

        self.detail_frame = tk.Frame(self.calendar_area)
        self.detail_frame.pack(pady=20)

    def show_date_detail(self, target_date):
        for widget in self.detail_frame.winfo_children():
            widget.destroy()

        detail_view = DateDetailView(self.detail_frame, target_date)
        detail_view.display()

    def open_account_registration_view(self):
        view = AccountRegistrationView()
        view.display()

    def open_group_creation_view(self):
        view = GroupCreationView(self.refresh_main_view)
        view.display()

    def create_registration_form(self):
        tk.Label(
            self.root,
            text="ユーザー登録",
            font=("Yu Gothic", 16)
        ).pack(pady=20)

        tk.Label(self.root, text="ユーザー名").pack()

        self.user_name_entry = tk.Entry(self.root, width=30)
        self.user_name_entry.pack(pady=5)

        tk.Button(
            self.root,
            text="登録",
            command=self.register_user_from_main
        ).pack(pady=10)

    def register_user_from_main(self):
        user_name = self.user_name_entry.get().strip()

        if not self.account_manager.check_user_name_length(user_name):
            from tkinter import messagebox
            messagebox.showerror("エラー", "ユーザー名は1～20文字で入力してください")
            return

        self.account_manager.register_user(user_name)

        from tkinter import messagebox
        messagebox.showinfo("登録完了", "ユーザー登録が完了しました")

        self.root.destroy()

        app = MainView()
        app.display()

    def open_registration_info_view(self):
        from boundary.registration_info_view import RegistrationInfoView
        view = RegistrationInfoView()
        view.display()

    def previous_month(self):
        if self.month == 1:
            self.month = 12
            self.year -= 1
        else:
            self.month -= 1

        self.create_calendar()

    def next_month(self):
        if self.month == 12:
            self.month = 1
            self.year += 1
        else:
            self.month += 1

        self.create_calendar()

    def refresh_main_view(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(
            self.root,
            text="食事予定管理システム",
            font=("Yu Gothic", 18)
        ).pack(pady=10)

        self.create_menu_buttons()
        self.calendar_area = tk.Frame(self.root)
        self.calendar_area.pack()
        self.create_calendar()

    def open_group_creation_view(self):
        view = GroupCreationView()
        view.display()

    def open_leave_group_view(self):
        view = LeaveGroupView(self.refresh_main_view)
        view.display()

    def open_add_member_view(self):
        view = AddMemberView()
        view.display()