import calendar
from datetime import datetime
import tkinter as tk
from tkinter import messagebox


# シーケンス図の :MealScheduleManager（コントロール層）を模したクラス
class DummyMealScheduleManager:

    def get_schedule_for_date(self, user_id: str, target_date: str) -> dict:
        """
        指定された日付の現在の登録状況を取得する処理
        """
        # 2026-06-26 だけダミーデータがある状態を再現
        if target_date == "2026-06-26":
            return {
                "breakfast": "必要 (帰宅 08:00)",
                "lunch": "不要",
                "dinner": "必要 (帰宅 19:00)",
                "message": "今日は夕飯遅くなります！",
            }
        else:
            return {
                "breakfast": "未登録",
                "lunch": "未登録",
                "dinner": "未登録",
                "message": "（伝言はありません）",
            }


# シーケンス図の :DateDetail Page（境界層）を表すクラス
class DateDetailView:

    def __init__(
        self,
        parent_root: tk.Tk,
        schedule_manager: DummyMealScheduleManager,
        selected_date: str,
    ):
        self.window = tk.Toplevel(parent_root)
        self.schedule_manager = schedule_manager
        self.current_user_id = "test_user_01"
        self.selected_date = selected_date

        self.window.title(f"詳細情報 - {self.selected_date}")
        self.window.geometry("450x420")

        self.current_data = self.schedule_manager.get_schedule_for_date(
            self.current_user_id, self.selected_date
        )
        self.create_widgets()

    def create_widgets(self):
        tk.Label(
            self.window,
            text=f"対象日: {self.selected_date}",
            font=("Arial", 14, "bold"),
            fg="#1E88E5",
        ).pack(pady=15)

        self.frame_info = tk.LabelFrame(self.window, text="現在の登録状況")
        self.frame_info.pack(fill="x", padx=20, pady=10)

        tk.Label(
            self.frame_info,
            text=f"朝食: {self.current_data['breakfast']}",
            font=("Arial", 11),
        ).pack(anchor="w", padx=15, pady=4)
        tk.Label(
            self.frame_info,
            text=f"昼食: {self.current_data['lunch']}",
            font=("Arial", 11),
        ).pack(anchor="w", padx=15, pady=4)
        tk.Label(
            self.frame_info,
            text=f"夕食: {self.current_data['dinner']}",
            font=("Arial", 11),
        ).pack(anchor="w", padx=15, pady=4)
        tk.Label(
            self.frame_info,
            text=f"伝言: {self.current_data['message']}",
            font=("Arial", 11, "italic"),
            fg="#555555",
        ).pack(anchor="w", padx=15, pady=8)

        self.btn_frame = tk.Frame(self.window)
        self.btn_frame.pack(pady=15)

        tk.Button(
            self.btn_frame,
            text="食事予定を登録",
            command=lambda: print("[View] 食事登録を開く"),
            font=("Arial", 11),
            bg="#2196F3",
            fg="white",
            width=14,
        ).pack(side=tk.LEFT, padx=10)
        tk.Button(
            self.btn_frame,
            text="伝言メッセージ",
            command=lambda: print("[View] メッセージ登録を開く"),
            font=("Arial", 11),
            bg="#9C27B0",
            fg="white",
            width=14,
        ).pack(side=tk.LEFT, padx=10)

        tk.Button(
            self.window,
            text="閉じる",
            command=self.window.destroy,
            font=("Arial", 10),
            bg="#757575",
            fg="white",
        ).pack(pady=15)


# 【月切り替え機能付き】メイン画面クラス
class MainCalendarView:

    def __init__(self, root: tk.Tk, schedule_manager: DummyMealScheduleManager):
        self.root = root
        self.schedule_manager = schedule_manager

        self.root.title("共有カレンダー")
        self.root.geometry("500x480")

        # 起動時の初期年月を設定（2026年6月）
        self.year = 2026
        self.month = 6

        # 表示エリア用のフレームを先に定義
        self.frame_header = None
        self.frame_weekdays = None
        self.frame_days = None

        # 初期カレンダーの描画
        self.draw_calendar()

    def draw_calendar(self):
        """
        現在の年月(self.year, self.month)に基づいてカレンダー画面を構築・再描画する
        """
        # すでにフレームが存在している場合は、中身をクリアするために古いフレームを破棄する
        if self.frame_header:
            self.frame_header.destroy()
        if self.frame_weekdays:
            self.frame_weekdays.destroy()
        if self.frame_days:
            self.frame_days.destroy()

        # 1. ヘッダーエリア（◀ボタン / 年月表示 / ▶ボタン）
        self.frame_header = tk.Frame(self.root)
        self.frame_header.pack(pady=15)

        # 前月ボタン
        btn_prev = tk.Button(
            self.frame_header,
            text="◀ 前月",
            font=("Arial", 10, "bold"),
            command=self.prev_month,
        )
        btn_prev.pack(side=tk.LEFT, padx=20)

        # 年月表示
        self.label_title = tk.Label(
            self.frame_header,
            text=f"{self.year}年 {self.month}月",
            font=("Arial", 16, "bold"),
            fg="#333333",
            width=12,
        )
        self.label_title.pack(side=tk.LEFT)

        # 次月ボタン
        btn_next = tk.Button(
            self.frame_header,
            text="次月 ▶",
            font=("Arial", 10, "bold"),
            command=self.next_month,
        )
        btn_next.pack(side=tk.LEFT, padx=20)

        # 2. 曜日ヘッダー
        self.frame_weekdays = tk.Frame(self.root)
        self.frame_weekdays.pack()

        weekdays = ["日", "月", "火", "水", "木", "金", "土"]
        colors = [
            "#f44336",
            "#333333",
            "#333333",
            "#333333",
            "#333333",
            "#333333",
            "#2196F3",
        ]

        for i, (day, color) in enumerate(zip(weekdays, colors)):
            lbl = tk.Label(
                self.frame_weekdays,
                text=day,
                font=("Arial", 12, "bold"),
                width=6,
                fg=color,
            )
            lbl.grid(row=0, column=i, padx=4, pady=5)

        # 3. 日付グリッドエリア
        self.frame_days = tk.Frame(self.root)
        self.frame_days.pack()

        cal = calendar.Calendar(firstweekday=6)
        month_days = cal.monthdayscalendar(self.year, self.month)

        for row_idx, week in enumerate(month_days):
            for col_idx, day in enumerate(week):
                if day == 0:
                    lbl = tk.Label(self.frame_days, width=6, height=2)
                    lbl.grid(row=row_idx, column=col_idx, padx=4, pady=4)
                else:
                    if col_idx == 0:
                        fg_color = "#f44336"
                    elif col_idx == 6:
                        fg_color = "#2196F3"
                    else:
                        fg_color = "#333333"

                    # 2026年6月26日の位置だけ背景色を薄黄色に変える
                    bg_color = (
                        "#FFF9C4"
                        if (self.year == 2026 and self.month == 6 and day == 26)
                        else "#F5F5F5"
                    )

                    date_str = f"{self.year}-{self.month:02d}-{day:02d}"
                    btn = tk.Button(
                        self.frame_days,
                        text=str(day),
                        font=("Arial", 11, "bold"),
                        width=6,
                        height=2,
                        fg=fg_color,
                        bg=bg_color,
                        command=lambda d=date_str: self.click_date(d),
                    )
                    btn.grid(row=row_idx, column=col_idx, padx=4, pady=4)

    def prev_month(self):
        """
        前の月へ切り替えるロジック
        """
        if self.month == 1:
            self.month = 12
            self.year -= 1
        else:
            self.month -= 1
        self.draw_calendar()  # 画面を再描画

    def next_month(self):
        """
        次の月へ切り替えるロジック
        """
        if self.month == 12:
            self.month = 1
            self.year += 1
        else:
            self.month += 1
        self.draw_calendar()  # 画面を再描画

    def click_date(self, chosen_date: str):
        print(f"[Main] カレンダーから日付 {chosen_date} が選択されました。")
        DateDetailView(self.root, self.schedule_manager, chosen_date)


if __name__ == "__main__":
    manager = DummyMealScheduleManager()
    root = tk.Tk()
    app = MainCalendarView(root, manager)
    root.mainloop()