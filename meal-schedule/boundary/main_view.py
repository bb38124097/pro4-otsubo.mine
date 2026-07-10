import calendar
from datetime import date
from flask import Blueprint, abort, redirect, render_template, request, url_for

# 既存のマネージャー（コントロール層）をインポート
from control.account_manager import AccountManager
from control.group_manager import GroupManager

<<<<<<< HEAD
# FlaskのルーティングをまとめるBlueprint（設計図）を作成
main_view_blueprint = Blueprint("main_view", __name__)

=======
from boundary.group_creation_view import GroupCreationView
from boundary.add_member_view import AddMemberView
from boundary.leave_group_view import LeaveGroupView
from boundary.date_detail_view import DateDetailView
from control.account_manager import AccountManager
from boundary.account_registration_view import AccountRegistrationView
>>>>>>> 58de930f7021947b817eb8445f88473100409681

class MainView:

    def __init__(self):
        self.account_manager = AccountManager()
        self.group_manager = GroupManager()

    def display(self):
        """元のTkinterの表示ロジックをFlaskのメインルーティングにマッピング"""

        # 1. ユーザーが登録されているかチェック
        if not self.account_manager.has_user():
            return render_template("index.html", mode="registration")

        # 2. カレンダーの年月を取得（クエリパラメータがなければ今月）
        try:
            year = int(request.args.get("year", date.today().year))
            month = int(request.args.get("month", date.today().month))
        except ValueError:
            year = date.today().year
            month = date.today().month

        # 前月・翌月の計算（previous_month / next_month メソッドのロジックを統合）
        prev_year, prev_month = (
            (year - 1, 12) if month == 1 else (year, month - 1)
        )
        next_year, next_month = (
            (year + 1, 1) if month == 12 else (year, month + 1)
        )

        # 3. グループ情報の判定（create_menu_buttons のロジック）
        user = self.account_manager.get_current_user()
        has_group = False
        if user is not None:
            has_group = self.group_manager.has_group(user.account_id)

        # 4. カレンダーマトリクスの生成（create_calendar のロジック）
        month_calendar = calendar.monthcalendar(year, month)

        # 5. 選択された日付の詳細（show_date_detail のロジック）
        selected_date = request.args.get("date")

<<<<<<< HEAD
        return render_template(
            "index.html",
            mode="main",
            year=year,
            month=month,
            prev_year=prev_year,
            prev_month=prev_month,
            next_year=next_year,
            next_month=next_month,
            has_group=has_group,
            month_calendar=month_calendar,
            selected_date=selected_date,
        )

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
>>>>>>> 58de930f7021947b817eb8445f88473100409681

    def register_user_from_main(self):
        """ユーザー登録処理"""
        user_name = request.form.get("user_name", "").strip()

        if not self.account_manager.check_user_name_length(user_name):
            # Webではポップアップの代わりに簡易的なエラーメッセージを返す（あるいは400エラー）
            return "エラー: ユーザー名は1～20文字で入力してください", 400

        self.account_manager.register_user(user_name)

        # 登録完了後、トップページへリダイレクト（Tkinterでの再起動に相当）
        return redirect(url_for("main_view.index_route"))


# --- Flaskがアクセスするためのルーティング定義 ---
# インスタンスを生成して各メソッドを呼び出します

main_view_instance = MainView()


@main_view_blueprint.route("/")
def index_route():
    return main_view_instance.display()


<<<<<<< HEAD
@main_view_blueprint.route("/register", methods=["POST"])
def register_route():
    return main_view_instance.register_user_from_main()


# その他のView（画面）への遷移定義（元の open_xxx_view に相当）
@main_view_blueprint.route("/registration-info")
def open_registration_info_view():
    from boundary.registration_info_view import RegistrationInfoView

    view = RegistrationInfoView()
    return view.display()


@main_view_blueprint.route("/group/create")
def open_group_creation_view():
    from boundary.group_creation_view import GroupCreationView

    view = GroupCreationView()
    return view.display()


@main_view_blueprint.route("/group/add-member")
def open_add_member_view():
    from boundary.add_member_view import AddMemberView

    view = AddMemberView()
    return view.display()


@main_view_blueprint.route("/group/leave")
def open_leave_group_view():
    from boundary.leave_group_view import LeaveGroupView

    view = LeaveGroupView()
    return view.display()
=======
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
>>>>>>> 58de930f7021947b817eb8445f88473100409681
