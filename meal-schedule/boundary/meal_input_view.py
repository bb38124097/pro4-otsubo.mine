import tkinter as tk
from tkinter import messagebox
from control.meal_schedule_manager import MealScheduleManager


class MealInputView:
    def __init__(self):
        self.manager = MealScheduleManager()

    def display(self):
        self.window = tk.Toplevel()
        self.window.title("食事予定入力")
        self.window.geometry("420x360")

        tk.Label(self.window, text="食事予定入力", font=("Yu Gothic", 16)).pack(pady=15)

        tk.Label(self.window, text="日付").pack()
        self.date_entry = tk.Entry(self.window, width=30)
        self.date_entry.insert(0, "2026-06-26")
        self.date_entry.pack(pady=5)

        self.breakfast_var = tk.BooleanVar()
        self.lunch_var = tk.BooleanVar()
        self.dinner_var = tk.BooleanVar()

        tk.Checkbutton(self.window, text="朝食が必要", variable=self.breakfast_var).pack()
        tk.Checkbutton(self.window, text="昼食が必要", variable=self.lunch_var).pack()
        tk.Checkbutton(self.window, text="夕食が必要", variable=self.dinner_var).pack()

        tk.Label(self.window, text="帰宅時間").pack()
        self.return_time_entry = tk.Entry(self.window, width=30)
        self.return_time_entry.pack(pady=5)

        tk.Label(self.window, text="メッセージ").pack()
        self.message_entry = tk.Entry(self.window, width=30)
        self.message_entry.pack(pady=5)

        tk.Button(
            self.window,
            text="登録",
            command=self.register_schedule
        ).pack(pady=15)

    def register_schedule(self):
        target_date = self.date_entry.get().strip()
        return_time = self.return_time_entry.get().strip()
        message = self.message_entry.get().strip()

        if not target_date:
            messagebox.showerror("エラー", "日付を入力してください")
            return

        self.manager.set_schedule(
            account_id=1,
            target_date=target_date,
            breakfast_required=self.breakfast_var.get(),
            lunch_required=self.lunch_var.get(),
            dinner_required=self.dinner_var.get(),
            return_time=return_time,
            message=message
        )

        messagebox.showinfo("登録完了", "食事予定を登録しました")
        self.window.destroy()