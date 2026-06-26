import tkinter as tk
from tkinter import messagebox
from tkinter import ttk


# シーケンス図の :MealScheduleManager（コントロール層）を模したクラス
class DummyMealScheduleManager:

    def set_meal_schedule(
        self,
        user_id: str,
        target_date: str,
        time_slot: str,
        requirement: str,
        return_time: str,
    ) -> None:
        """
        食事予定の情報を精査し、UserCalenderへの登録とGroupCalenderへの同期(syncSchedule)を行う
        """
        print(f"[Manager] 以下の予定を処理します。日付: {target_date}")
        print(
            f"[Manager] 区分: {time_slot} | 必要: {requirement} | 帰宅時間: {return_time}"
        )
        print(f"[Manager] :UserCalender への set() が完了しました。")
        print(f"[Manager] :GroupCalender への syncSchedule() を実行しました。")


# シーケンス図の :MealInputView（境界層）を表すクラス
class MealInputView:

    def __init__(self, root: tk.Tk, schedule_manager: DummyMealScheduleManager):
        self.root = root
        self.schedule_manager = schedule_manager

        # テスト用の疑似データ（本来はカレンダーで選択された日付などが入ります）
        self.current_user_id = "test_user_01"
        self.selected_date = "2026-06-26"

        # ウィンドウの設定
        self.root.title("食事予定入力")
        self.root.geometry("450x350")

        # 画面コンポーネント（要素）の作成
        self.create_widgets()

    def create_widgets(self):
        """
        システムが、食事情報の登録画面を表示する処理（シーケンス図の display() に対応）
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
            self.frame_req,
            text="必要",
            variable=self.var_requirement,
            value="need",
            command=self.toggle_time_entry,
        ).pack(side=tk.LEFT, padx=15, pady=5)
        tk.Radiobutton(
            self.frame_req,
            text="不要",
            variable=self.var_requirement,
            value="no_need",
            command=self.toggle_time_entry,
        ).pack(side=tk.LEFT, padx=15, pady=5)

        # 3. 帰宅予定時間の入力欄
        self.frame_return = tk.LabelFrame(self.root, text="帰宅予定時間")
        self.frame_return.pack(fill="x", padx=20, pady=5)

        self.label_hint = tk.Label(self.frame_return, text="時間 (例: 19:30):")
        self.label_hint.pack(side=tk.LEFT, padx=10, pady=5)

        self.entry_return_time = tk.Entry(self.frame_return, width=15)
        self.entry_return_time.pack(side=tk.LEFT, padx=10, pady=5)
        self.entry_return_time.insert(0, "19:00")  # デフォルト値

        # ボタン配置用のフレーム
        self.btn_frame = tk.Frame(self.root)
        self.btn_frame.pack(pady=20)

        # 登録ボタン
        self.btn_submit = tk.Button(
            self.btn_frame,
            text="登録する",
            command=self.click_submit,
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

    def toggle_time_entry(self):
        """
        食事「不要」が選ばれたときは、帰宅時間の入力を無効化する処理
        （シーケンス図の [isMealRequired] 分岐に近い画面制御ロジック）
        """
        if self.var_requirement.get() == "no_need":
            self.entry_return_time.config(state=tk.DISABLED)
        else:
            self.entry_return_time.config(state=tk.NORMAL)

    def click_submit(self):
        """
        ユーザーが登録を指示したときのイベントハンドラ
        """
        time_slot = self.var_time_slot.get()
        requirement = self.var_requirement.get()
        return_time = (
            self.entry_return_time.get().strip()
            if requirement == "need"
            else "N/A"
        )

        print(f"[View] 登録ボタンがクリックされました。")

        try:
            # 帰宅時間の簡易バリデーション（必要な場合のみ）
            if requirement == "need" and not return_time:
                raise ValueError("帰宅予定時間を入力してください。")

            # 1. MealScheduleManagerに予定のセットと同期を依頼する
            # (シーケンス図の submitTargetTime / confirm / set / syncSchedule の一連の流れに対応)
            self.schedule_manager.set_meal_schedule(
                self.current_user_id,
                self.selected_date,
                time_slot,
                requirement,
                return_time,
            )

            # 成功メッセージの表示
            messagebox.showinfo("登録完了", "食事予定を登録・共有しました。")

            # 画面を閉じる
            self.root.destroy()

        except ValueError as ve:
            messagebox.showwarning("入力エラー", str(ve))
        except Exception as e:
            messagebox.showerror("エラー", f"登録に失敗しました: {e}")


# アプリケーションの起動（単体テスト用）
if __name__ == "__main__":
    manager = DummyMealScheduleManager()
    root = tk.Tk()
    app = MealInputView(root, manager)
    root.mainloop()