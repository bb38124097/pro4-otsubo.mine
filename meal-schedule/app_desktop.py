from datetime import date
import tkinter as tk
from tkinter import messagebox, ttk

# あなたが作った「Control(司令塔)」をインポート
from control.meal_schedule_manager import MealScheduleManager


class MealScheduleApp:

    def __init__(self, root):
        self.root = root
        self.root.title("おうちのご飯管理アプリ")
        self.root.geometry("450x400")  # ウィンドウのサイズ設定

        # マネージャー（Control）の初期化
        self.manager = MealScheduleManager()

        # --- 画面のパーツ（UI）の作成 ---
        # 1. ユーザー選択のラベルとコンボボックス
        tk.Label(root, text="あなたのお名前は？", font=("MS Gothic", 12)).pack(
            pady=10
        )
        self.user_combo = ttk.Combobox(
            root, values=["user_father", "user_sister"], state="readonly"
        )
        self.user_combo.set("user_father")  # 初期値
        self.user_combo.pack()

        # 2. 夕飯の要・不要（ラジオボタン）
        tk.Label(root, text="今日の夕飯は？", font=("MS Gothic", 12)).pack(
            pady=10
        )
        self.meal_var = tk.StringVar(value="必要")
        tk.Radiobutton(
            root, text="必要", variable=self.meal_var, value="必要"
        ).pack()
        tk.Radiobutton(
            root, text="不要", variable=self.meal_var, value="不要"
        ).pack()

        # 3. 帰宅時間の入力欄
        tk.Label(root, text="帰宅予定時間 (例: 19:00)", font=("MS Gothic", 10)).pack(
            pady=5
        )
        self.time_entry = tk.Entry(root)
        self.time_entry.insert(0, "19:00")  # 初期値
        self.time_entry.pack()

        # 4. 伝言メッセージの入力欄
        tk.Label(root, text="伝言メッセージ (30文字以内)", font=("MS Gothic", 10)).pack(
            pady=5
        )
        self.msg_entry = tk.Entry(root, width=40)
        self.msg_entry.insert(0, "遅くなります！")
        self.msg_entry.pack()

        # 5. 登録ボタン（押すと register_schedule メソッドが動く）
        st_button = tk.Button(
            root,
            text="カレンダーに登録する",
            command=self.register_schedule,
            bg="#4CAF50",
            fg="white",
        )
        st_button.pack(pady=20)

    def register_schedule(self):
        """ボタンが押されたときに実行される、仕様書通りのバトンリレー処理"""
        user_id = self.user_combo.get()
        needs_meal = self.meal_var.get()
        return_time = self.time_entry.get()
        message = self.msg_entry.get()
        date_str = str(date.today())  # 今日のお日付

        try:
            # --- Control (Manager) へのバトンリレー ---
            if needs_meal == "不要":
                if hasattr(self.manager, "set_meal_no_need"):
                    self.manager.set_meal_no_need(
                        user_id=user_id, target_date=date_str, time_slot="dinner"
                    )
                elif hasattr(self.manager, "set_schedule"):
                    self.manager.set_schedule(
                        account_id=user_id,
                        target_date=date_str,
                        breakfast_required=0,
                        lunch_required=0,
                        dinner_required=0,
                        return_time=None,
                        message=message,
                    )
            else:
                if hasattr(self.manager, "set_return_time"):
                    self.manager.set_return_time(
                        user_id=user_id,
                        target_date=date_str,
                        time_slot="dinner",
                        return_time=return_time,
                    )
                elif hasattr(self.manager, "set_schedule"):
                    self.manager.set_schedule(
                        account_id=user_id,
                        target_date=date_str,
                        breakfast_required=0,
                        lunch_required=0,
                        dinner_required=1,
                        return_time=return_time,
                        message=message,
                    )

            # メッセージの追加登録（文字数チェックが裏で動く）
            if message and hasattr(self.manager, "set_message"):
                self.manager.set_message(
                    user_id=user_id,
                    target_date=date_str,
                    time_slot="dinner",
                    message=message,
                )

            # 成功したらポップアップでお知らせ
            messagebox.showinfo(
                "成功", f"{user_id} さんの予定をDBに保存・同期しました！"
            )

        except ValueError as e:
            # 安全装置に引っかかったら警告ポップアップを出す
            messagebox.showerror("バリデーションエラー", str(e))


# アプリケーションの起動処理
if __name__ == "__main__":
    main_window = tk.Tk()
    app = MealScheduleApp(main_window)
    main_window.mainloop()  # 画面を閉じないように維持する魔法のループ