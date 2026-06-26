import tkinter as tk
from tkinter import messagebox


# シーケンス図の :GroupManager（コントロール層）を模したクラス
class DummyGroupManager:

    def remove_account(self, group_id: str, account_id: str) -> None:
        """
        Group からアカウントIDを削除し、User からグループIDを削除する
        """
        print(f"[Manager] グループ:{group_id} から ユーザー:{account_id} を削除します。")
        print(f"[Manager] :Group からアカウントIDの削除を完了しました。")
        print(f"[Manager] :User からグループIDの削除を完了しました。")

    def unlink_calendar(self, group_id: str, account_id: str) -> None:
        """
        UserCalender と GroupCalender のリンクを解除（unlinked）する
        """
        print(
            f"[Manager] ユーザー:{account_id} と グループ:{group_id} のカレンダー連携を解除しました。"
        )
        print(f"[Manager] :UserCalender 側で unlinked() が実行されました。")


# シーケンス図の :LeaveGroupView（境界層）を表すクラス
class LeaveGroupView:

    def __init__(self, root: tk.Tk, group_manager: DummyGroupManager):
        self.root = root
        self.group_manager = group_manager

        # テスト用の疑似ログインデータ
        self.current_user_id = "test_user_01"
        self.current_group_id = "generated_group_id_123"
        self.current_group_name = "サンプルグループ"

        # ウィンドウの設定
        self.root.title("グループ退出")
        self.root.geometry("400x200")

        # 画面コンポーネント（要素）の作成
        self.create_widgets()

    def create_widgets(self):
        """
        システムが、グループ退出画面を表示する処理（シーケンス図の display() に対応）
        """
        # 確認ラベル
        self.label = tk.Label(
            self.root,
            text=f"「{self.current_group_name}」から退出しますか？\n※退出すると共有カレンダーが見られなくなります。",
            font=("Arial", 11),
            justify=tk.CENTER,
        )
        self.label.pack(pady=25)

        # ボタン配置用のフレーム
        self.btn_frame = tk.Frame(self.root)
        self.btn_frame.pack(pady=10)

        # 退出ボタン（シーケンス図の confirm() イベントを発生させるトリガー）
        self.btn_leave = tk.Button(
            self.btn_frame,
            text="退出する",
            command=self.click_leave,
            font=("Arial", 11),
            bg="#f44336",
            fg="white",
            width=12,
        )
        self.btn_leave.pack(side=tk.LEFT, padx=10)

        # キャンセルボタン
        self.btn_cancel = tk.Button(
            self.btn_frame,
            text="キャンセル",
            command=self.root.destroy,
            font=("Arial", 11),
            bg="#9E9E9E",
            fg="white",
            width=12,
        )
        self.btn_cancel.pack(side=tk.LEFT, padx=10)

    def click_leave(self):
        """
        ユーザーが確定（退出）を指示したときのイベントハンドラ（シーケンス図の confirm() に対応）
        """
        print(f"[View] 退出するボタンがクリックされました。")

        try:
            # 1. GroupManagerにメンバー削除を依頼（シーケンス図の remove(accountID) / remove(groupID) のトリガー）
            self.group_manager.remove_account(
                self.current_group_id, self.current_user_id
            )

            # 2. GroupManagerにカレンダーの連携解除を依頼（シーケンス図の unlinked() のトリガー）
            self.group_manager.unlink_calendar(
                self.current_group_id, self.current_user_id
            )

            # 成功メッセージを表示
            messagebox.showinfo(
                "退出完了",
                f"グループ「{self.current_group_name}」から退出しました。",
            )

            # 画面を閉じる
            self.root.destroy()

        except Exception as e:
            messagebox.showerror("エラー", f"退出処理に失敗しました: {e}")


# アプリケーションの起動（単体テスト用）
if __name__ == "__main__":
    manager = DummyGroupManager()
    root = tk.Tk()
    app = LeaveGroupView(root, manager)
    root.mainloop()