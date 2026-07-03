import tkinter as tk
from boundary.meal_input_view import MealInputView
from control.meal_schedule_manager import MealScheduleManager


class DateDetailView:
    def __init__(self, parent, target_date):
        self.parent = parent
        self.target_date = target_date
        self.manager = MealScheduleManager()
        self.account_id = 1

    def display(self):
        tk.Label(
            self.parent,
            text=f"{self.target_date} の予定",
            font=("Yu Gothic", 14)
        ).pack(pady=10)

        self.create_meal_row("breakfast", "朝食")
        self.create_meal_row("lunch", "昼食")
        self.create_meal_row("dinner", "夕食")

    def create_meal_row(self, meal_type, meal_name):
        schedule = self.manager.get_schedule(
            self.account_id,
            self.target_date,
            meal_type
        )

        if schedule is None:
            status_text = "未登録"
        else:
            required_text = "必要" if schedule["required"] else "不要"
            return_time = schedule["return_time"] or "-"
            message = schedule["message"] or "-"
            status_text = f"{required_text} / 帰宅時間: {return_time} / メッセージ: {message}"

        frame = tk.Frame(self.parent)
        frame.pack(pady=5)

        tk.Button(
            frame,
            text=meal_name,
            width=10,
            command=lambda: self.open_meal_input_view(meal_type)
        ).pack(side=tk.LEFT, padx=5)

        tk.Label(
            frame,
            text=status_text,
            width=45,
            anchor="w"
        ).pack(side=tk.LEFT)

    def open_meal_input_view(self, meal_type):
        view = MealInputView(self.target_date, meal_type)
        view.display()