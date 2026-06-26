import tkinter as tk
from tkinter import messagebox


# シーケンス図の :MealScheduleManager（コントロール層）を模したクラス
class DummyMealScheduleManager:

    def has_next_step(self, requirement: str) -> bool:
        """
        理不尽な重複を防ぐため、食事が「必要」な場合のみ次の時間入力画面へ進む判定を行う
        """
        return requirement == "need"

    def set_meal_no_need(self, user_id: str, target_date: str, time_slot: str):
        """
        食事が「不要」な場合は、帰宅時間の入力なしでここで確定・同期する
        """
        print(f"[Manager] 日付: {target_date} ({time_slot}) は食事「不要」で登録します。")
        print(f"[Manager] :UserCalender への set() が完了しました。")
        print(f"[Manager] :GroupCalender への syncSchedule() を実行しました。")


# シーケンス図の :MealRequirementPage（境界層）を表すクラス
class MealInputView:

    def __init__(self, root: tk.Tk, schedule_manager: DummyMealScheduleManager):
        self.root = root
        self.schedule_manager = schedule_manager

        # テスト用の疑似データ
        self.current_user_id = "test_user_01"
        self.selected_date = "2026-06-26"

        self.root.title("食事予定入力")
        self.root.geometry("400x260")

        self.create_widgets()

    def create_widgets(self):
        """
        システムが、食事の要不要の選択画面を表示する処理（シーケンス図の display() に対応）
        """
        # 日付表示ラベル
        self.label_date = tk.Label(
            self.root,
            text=f"対象日: {self.selected_date}",
            font=("Arial", 12, "bold"),
        )
        self.label_date.pack(pady=15)

        # 1. 食事タイミングの選択（朝・昼・夜）
        self.frame_time = tk.LabelFrame(self.root, text="食事のタイミング")
        self.frame_time.pack(fill="x", padx=20, pady=5)

        self.var_time_slot = tk.StringVar(value="dinner")
        tk.Radiobutton(
            self.frame_time, text="朝食", variable=self.var_time_slot, value="breakfast"
        ).pack(side=tk.LEFT, padx=15, pady=5)
        tk.Radiobutton(
            self.frame_time, text="昼食", variable=self.var_time_slot, value="lunch"
        ).pack(side=tk.LEFT, padx=15, pady=5)
        tk.Radiobutton(
            self.frame_time, text="夕食", variable=self.var_time_slot, value="dinner"
        ).pack(side=tk.LEFT, padx=15, pady=5)

        # 2. 食事の要・不要の選択
        self.frame_req = tk.LabelFrame(self.root, text="食事の必要性")
        self.frame_req.pack(fill="x", padx=20, pady=5)

        self.var_requirement = tk.StringVar(value="need")
        tk.Radiobutton(
            self.frame_req, text="必要", variable=self.var_requirement, value="need"
        ).pack(side=tk.LEFT, padx=15, pady=5)
        tk.Radiobutton(
            self.frame_req, text="不要", variable=self.var_requirement, value="no_need"
        ).pack(side=tk.LEFT, padx=15, pady=5)

        # ボタン配置用のフレーム
        self.btn_frame = tk.Frame(self.root)
        self.btn_frame.pack(pady=20)

        # 次へボタン（または登録ボタン）
        self.btn_submit = tk.Button(
            self.btn_frame,
            text="次へ進む",
            command=self.click_next,
            font=("Arial", 11),
            bg="#4CAF50",
            fg="white",
            width=12,
        )
        self.btn_submit.pack(side=tk.LEFT, padx=10)

        # キャンセルボタン
        self.btn_cancel = tk.Button(
            self.btn_frame,
            text="キャンセル",
            command=self.root.destroy,
            font=("Arial", 11),
            bg="#f44336",
            fg="white",
            width=12,
        )
        self.btn_cancel.pack(side=tk.LEFT, padx=10)

    def click_next(self):
        """
        ユーザーが決定を指示したときのイベントハンドラ
        """
        time_slot = self.var_time_slot.get()
        requirement = self.var_requirement.get()

        print(f"[View] 選択されました。タイミング: {time_slot} | 必要性: {requirement}")

        # マネージャーに次のステップ（帰宅時間入力）が必要か確認
        if self.schedule_manager.has_next_step(requirement):
            # 食事「必要」なら、この画面を閉じて次の「帰宅時間入力画面」に進む
            print("[View] 食事が必要なため、帰宅時間入力画面（ReturnTimeInputView）へ遷移します。")
            messagebox.showinfo("案内", "次の画面で帰宅予定時間を入力してください。")
            
            # 本来はここで return_time_input_view のクラスを呼び出しますが、
            # 今回は単体確認のため、遷移のログを残して画面を閉じます
            self.root.destroy()
        else:
            # 食事「不要」なら、その場で登録処理を完結させる（[isMealRequired] の偽ルートに相当）
            self.schedule_manager.set_meal_no_need(
                self.current_user_id, self.selected_date, time_slot
            )
            messagebox.showinfo("登録完了", "食事「不要」で予定を登録・共有しました。")
            self.root.destroy()


if __name__ == "__main__":
    manager = DummyMealScheduleManager()
    root = tk.Tk()
    app = MealInputView(root, manager)
    root.mainloop()