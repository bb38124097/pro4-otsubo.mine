import tkinter as tk
from tkinter import messagebox
from control.meal_schedule_manager import MealScheduleManager


class MealInputView:
    def __init__(self, target_date, meal_type):
        self.manager = MealScheduleManager()
        self.target_date = target_date
        self.meal_type = meal_type

    def display(self):
        self.window = tk.Toplevel()
        self.window.title("予定入力")
        self.window.geometry("400x340")

        meal_name = {
            "breakfast": "朝食",
            "lunch": "昼食",
            "dinner": "夕食"
        }[self.meal_type]

        tk.Label(
            self.window,
            text=f"{self.target_date} の {meal_name}",
            font=("Yu Gothic", 16)
        ).pack(pady=15)

        self.required_var = tk.BooleanVar(value=True)

        tk.Radiobutton(
            self.window,
            text="必要",
            variable=self.required_var,
            value=True,
            command=self.toggle_input_fields
        ).pack()

        tk.Radiobutton(
            self.window,
            text="不要",
            variable=self.required_var,
            value=False,
            command=self.toggle_input_fields
        ).pack()

        self.detail_frame = tk.Frame(self.window)
        self.detail_frame.pack(pady=10)

        tk.Label(self.detail_frame, text="帰宅時間").pack()
        self.return_time_entry = tk.Entry(self.detail_frame, width=30)
        self.return_time_entry.pack()

        tk.Label(self.detail_frame, text="メッセージ").pack(pady=5)
        self.message_entry = tk.Entry(self.detail_frame, width=30)
        self.message_entry.pack()

        tk.Button(
            self.window,
            text="登録",
            command=self.register_schedule
        ).pack(pady=15)

        self.toggle_input_fields()

    def toggle_input_fields(self):
        if self.required_var.get():
            self.detail_frame.pack(pady=10)
        else:
            self.detail_frame.pack_forget()

    def register_schedule(self):
        if self.required_var.get():
            return_time = self.return_time_entry.get().strip()
            message = self.message_entry.get().strip()
        else:
            return_time = ""
            message = ""

        self.manager.set_one_meal_schedule(
            account_id=1,
            target_date=self.target_date,
            meal_type=self.meal_type,
            required=self.required_var.get(),
            return_time=return_time,
            message=message
        )

        messagebox.showinfo("登録完了", "予定を登録しました")
        self.window.destroy()
