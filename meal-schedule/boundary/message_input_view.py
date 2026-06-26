import tkinter as tk
from tkinter import messagebox


# シーケンス図の :MealScheduleManager（コントロール層）を模したクラス
class DummyMealScheduleManager:

    def check_length(self, message: str) -> bool:
        """
        メッセージの文字数制限をチェックする (30文字以内)
        """
        if len(message) > 30:  # 30文字に変更
            return False
        return True

    def set_message(
        self, user_id: str, target_date: str, time_slot: str, message: str
    ) -> None:
        """
        メッセージをカレンダーに登録し、グループに同期する
        """
        print(f"[Manager] メッセージを登録します。対象日: {target_date} ({time_slot})")
        print(f"[Manager] 内容: {message}")
        print(f"[Manager] :UserCalender への set(message) が完了しました。")
        print(f"[Manager] :GroupCalender への syncSchedule() を実行しました。")


# シーケンス図の :Message Page（境界層）を表すクラス
class MessageInputView:

    def __init__(self, root: tk.Tk, schedule_manager: DummyMealScheduleManager):
        self.root = root
        self.schedule_manager = schedule_manager

        # 前の画面から引き継いだ想定のデータ
        self.current_user_id = "test_user_01"
        self.selected_date = "2026-06-26"
        self.selected_time_slot = "dinner"

        # ウィンドウの設定
        self.root.title("メッセージ入力")
        self.root.geometry("400x250")

        self.create_widgets()

    def create_widgets(self):
        """
        システムが、メッセージ入力画面を表示する処理
        """
        # 案内ラベルの表示を30文字に変更
        self.label_hint = tk.Label(
            self.root,
            text="伝言・メッセージを入力してください\n（30文字以内）",
            font=("Arial", 11),
        )
        self.label_hint.pack(pady=15)

        # メッセージ入力欄
        self.entry_message = tk.Entry(self.root, font=("Arial", 12), width=30)
        self.entry_message.pack(pady=10)
        self.entry_message.insert(0, "")

        # ボタン配置用のフレーム
        self.btn_frame = tk.Frame(self.root)
        self.btn_frame.pack(pady=15)

        # 登録ボタン
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
        ユーザーがメッセージを送信したときのイベントハンドラ
        """
        message = self.entry_message.get().strip()

        print(f"[View] メッセージが送信されました。内容: {message}")

        # 1. マネージャーに文字数チェックを依頼 (30文字チェック)
        is_valid = self.schedule_manager.check_length(message)

        if not is_valid:
            # エラーメッセージの表示を30文字に変更
            messagebox.showwarning(
                "入力エラー",
                "メッセージは30文字以内で入力してください。",
            )
            return

        try:
            # 2. 登録と同期を実行
            self.schedule_manager.set_message(
                self.current_user_id,
                self.selected_date,
                self.selected_time_slot,
                message,
            )

            messagebox.showinfo("登録完了", "メッセージを登録・同期しました。")
            self.root.destroy()

        except Exception as e:
            messagebox.showerror("エラー", f"登録に失敗しました: {e}")


if __name__ == "__main__":
    manager = DummyMealScheduleManager()
    root = tk.Tk()
    app = MessageInputView(root, manager)
    root.mainloop()