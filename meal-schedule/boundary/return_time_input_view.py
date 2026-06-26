import tkinter as tk
from tkinter import messagebox
import re


# シーケンス図の :MealScheduleManager（コントロール層）を模したクラス
class DummyMealScheduleManager:

    def set_return_time(
        self, user_id: str, target_date: str, time_slot: str, return_time: str
    ) -> None:
        """
        帰宅時間を確定し、UserCalenderに登録、GroupCalenderへ同期する
        (シーケンス図の confirm(..., returnTime) および syncSchedule() の流れに対応)
        """
        print(f"[Manager] 帰宅時間を登録します。対象日: {target_date} ({time_slot})")
        print(f"[Manager] 帰宅予定時間: {return_time}")
        print(f"[Manager] :UserCalender への登録が完了しました。")
        print(f"[Manager] :GroupCalender への syncSchedule() を実行しました。")


# シーケンス図の :ReturnTimePage（境界層）を表すクラス
class ReturnTimeInputView:

    def __init__(self, root: tk.Tk, schedule_manager: DummyMealScheduleManager):
        self.root = root
        self.schedule_manager = schedule_manager

        # 前の画面（MealRequirementPageなど）から引き継いだ想定のデータ
        self.current_user_id = "test_user_01"
        self.selected_date = "2026-06-26"
        self.selected_time_slot = "dinner"  # 朝食/昼食/夕食

        # ウィンドウの設定
        self.root.title("帰宅時間入力")
        self.root.geometry("400x220")

        self.create_widgets()

    def create_widgets(self):
        """
        システムが、帰宅予定時間の入力画面を表示する処理（シーケンス図の display() に対応）
        """
        # 案内ラベル
        self.label_hint = tk.Label(
            self.root,
            text="帰宅予定時間を入力してください\n(例: 19:30, 21:00)",
            font=("Arial", 11),
        )
        self.label_hint.pack(pady=15)

        # 時間入力欄（シーケンス図の submit(returnTime) で送られる要素）
        self.entry_return_time = tk.Entry(self.root, font=("Arial", 12), width=20)
        self.entry_return_time.pack(pady=10)
        self.entry_return_time.insert(0, "19:00")  # デフォルト値

        # ボタン配置用のフレーム
        self.btn_frame = tk.Frame(self.root)
        self.btn_frame.pack(pady=15)

        # 登録ボタン（シーケンス図の submit(returnTime) をトリガーするボタン）
        self.btn_submit = tk.Button(
            self.btn_frame,
            text="登録する",
            command=self.click_submit,
            font=("Arial", 11),
            bg="#4CAF50",
            fg="white",
            width=10,
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
            width=10,
        )
        self.btn_cancel.pack(side=tk.LEFT, padx=10)

    def click_submit(self):
        """
        ユーザーが帰宅時間を送信（確定）したときのイベントハンドラ
        """
        return_time = self.entry_return_time.get().strip()

        print(f"[View] 帰宅時間が入力されました。時間: {return_time}")

        # 簡易的な時間フォーマットバリデーション (HH:MM 形式チェック)
        if not re.match(r"^\d{1,2}:\d{2}$", return_time):
            messagebox.showwarning(
                "入力エラー",
                "時間の形式が正しくありません。「19:30」のように入力してください。",
            )
            return

        try:
            # 1. マネージャーに帰宅時間の登録と同期を依頼
            # (シーケンス図の confirm(targetTime, mealRequirement, returnTime) から後ろの流れに対応)
            self.schedule_manager.set_return_time(
                self.current_user_id,
                self.selected_date,
                self.selected_time_slot,
                return_time,
            )

            # 成功メッセージを表示して画面を閉じる
            messagebox.showinfo("登録完了", "帰宅予定時間を登録・同期しました。")
            self.root.destroy()

        except Exception as e:
            messagebox.showerror("エラー", f"登録に失敗しました: {e}")


# アプリケーションの起動（単体テスト用）
if __name__ == "__main__":
    manager = DummyMealScheduleManager()
    root = tk.Tk()
    app = ReturnTimeInputView(root, manager)
    root.mainloop()