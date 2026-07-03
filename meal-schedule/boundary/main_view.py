from datetime import date
import calendar
import tkinter as tk

from boundary.add_member_view import AddMemberView
from boundary.date_detail_view import DateDetailView
from boundary.group_creation_view import GroupCreationView
from boundary.leave_group_view import LeaveGroupView
from control.account_manager import AccountManager
from control.group_manager import GroupManager


class MainView:

    def display(self):
        self.root = tk.Tk()
        self.root.title("食事予定管理システム")
        self.root.geometry("520x720")

        # 司令塔（Control）の初期化
        self.account_manager = AccountManager()
        self.group_manager = GroupManager()

        self.year = date.today().year
        self.month = date.today().month

        tk.Label(
            self.root, text="食事予定管理システム", font=("Yu Gothic", 18)
        ).pack(pady=10)

        # ➔ ユーザー自体が未登録なら登録フォーム、登録済みならメニューとカレンダーを表示
        if not self.account_manager.has_user():
            self.create_registration_form()
        else:
            self.create_menu_buttons()
            self.create_calendar()

        self.root.mainloop()

    def create_menu_buttons(self):
        """ユーザーのグループ所属状態に合わせてボタンを綺麗に出し分ける（配置修正版）"""
        frame = tk.Frame(self.root)
        frame.pack(pady=5)

        # 現在のユーザー情報を取得
        user = self.account_manager.get_current_user()

        # 現在グループに属しているかIDをチェック
        group_id = (
            self.group_manager.get_user_group_id(user.account_id)
            if user
            else None
        )

        if group_id is None:
            # 【未所属】グループ作成ボタンだけを表示
            tk.Button(
                frame,
                text="グループ作成",
                width=14,
                command=self.open_group_creation_view,
            ).grid(row=0, column=0, padx=5, pady=5)
        else:
            # 【所属済み】メンバー追加 と グループ退出 をきれいに横並びで表示
            tk.Button(
                frame,
                text="メンバー追加",
                width=14,
                command=self.open_add_member_view,
            ).grid(row=0, column=0, padx=5, pady=5)

            tk.Button(
                frame,
                text="グループ退出",
                width=14,
                command=self.open_leave_group_view,
            ).grid(row=0, column=1, padx=5, pady=5)

        # 登録情報確認ボタン（常に下の行 row=1 に固定表示）
        tk.Button(
            frame,
            text="登録情報",
            width=14,
            command=self.open_registration_info_view,
        ).grid(row=1, column=0, padx=5, pady=5)

    def create_calendar(self):
        """カレンダー画面の描画"""
        tk.Label(
            self.root,
            text=f"{self.year}年 {self.month}月",
            font=("Yu Gothic", 16),
        ).pack(pady=10)

        calendar_frame = tk.Frame(self.root)
        calendar_frame.pack()

        days = ["月", "火", "水", "木", "金", "土", "日"]

        for col, day_name in enumerate(days):
            tk.Label(
                calendar_frame,
                text=day_name,
                width=6,
                font=("Yu Gothic", 10, "bold"),
            ).grid(row=0, column=col, padx=2, pady=2)

        month_calendar = calendar.monthcalendar(self.year, self.month)

        for row, week in enumerate(month_calendar, start=1):
            for col, day in enumerate(week):
                if day == 0:
                    tk.Label(calendar_frame, text="", width=6).grid(
                        row=row, column=col
                    )
                else:
                    target_date = f"{self.year}-{self.month:02d}-{day:02d}"

                    tk.Button(
                        calendar_frame,
                        text=str(day),
                        width=6,
                        command=lambda d=target_date: self.show_date_detail(
                            d
                        ),
                    ).grid(row=row, column=col, padx=2, pady=2)

        self.detail_frame = tk.Frame(self.root)
        self.detail_frame.pack(pady=20)

    def show_date_detail(self, target_date):
        """日付が押されたときに詳細画面（登録状況）を下に描画する"""
        for widget in self.detail_frame.winfo_children():
            widget.destroy()

        detail_view = DateDetailView(self.detail_frame, target_date)
        detail_view.display()

    def create_registration_form(self):
        """初期起動時のユーザー登録画面"""
        tk.Label(
            self.root, text="ユーザー登録", font=("Yu Gothic", 16)
        ).pack(pady=20)

        tk.Label(self.root, text="ユーザー名").pack()

        self.user_name_entry = tk.Entry(self.root, width=30)
        self.user_name_entry.pack(pady=5)

        tk.Button(
            self.root, text="登録", command=self.register_user_from_main
        ).pack(pady=10)

    def register_user_from_main(self):
        """メイン画面の登録ボタンからAccountManagerを呼び出す処理"""
        user_name = self.user_name_entry.get().strip()

        if not self.account_manager.check_user_name_length(user_name):
            from tkinter import messagebox

            messagebox.showerror(
                "エラー", "ユーザー名は1～20文字で入力してください"
            )
            return

        self.account_manager.register_user(user_name)

        from tkinter import messagebox

        messagebox.showinfo("登録完了", "ユーザー登録が完了しました")

        # 画面を一度破棄し、カレンダーモードで再起動
        self.root.destroy()
        app = MainView()
        app.display()

    # --- 各サブ画面（View）の呼び出し関数群 ---
    def open_group_creation_view(self):
        view = GroupCreationView()
        view.display()

    def open_add_member_view(self):
        view = AddMemberView()
        view.display()

    def open_leave_group_view(self):
        view = LeaveGroupView()
        view.display()

    def open_registration_info_view(self):
        from boundary.registration_info_view import RegistrationInfoView

        view = RegistrationInfoView()
        view.display()