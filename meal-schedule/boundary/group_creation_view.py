import tkinter as tk
from tkinter import messagebox


# シーケンス図の :GroupManager（コントロール層）を模したクラス
class DummyGroupManager:

    def create_group(self, user_id: str, group_name: str) -> str:
        if not group_name:
            raise ValueError("グループ名を入力してください。")
        # 本来はここでDBに登録してIDを発行します
        return "generated_group_id_123"

    def add_group_calendar(self, user_id: str, group_id: str) -> None:
        # 本来はここでユーザーとグループカレンダーを紐づけます
        print(
            f"[Manager] ユーザー:{user_id} のカレンダーに グループ:{group_id} を紐づけました。"
        )


# シーケンス図の :GroupCreationView（境界層）を表すクラス
class GroupCreationView:

    def __init__(self, root: tk.Tk, group_manager: DummyGroupManager):
        self.root = root
        self.group_manager = group_manager

        # テスト用の疑似ログインユーザーID
        self.current_user_id = "test_user_01"

        # ウィンドウの設定
        self.root.title("グループ作成")
        self.root.geometry("400x200")

        # 画面コンポーネント（要素）の作成
        self.create_widgets()

    def create_widgets(self):
        """
        システムが、グループの情報登録画面を表示する処理（シーケンス図のdisplay()に対応）
        """
        # ラベル
        self.label = tk.Label(
            self.root, text="グループ名を入力してください", font=("Arial", 12)
        )
        self.label.pack(pady=20)

        # グループ名入力欄（シーケンス図のsubmit(groupName)で送られる値になります）
        self.entry_group_name = tk.Entry(self.root, font=("Arial", 12), width=30)
        self.entry_group_name.pack(pady=10)

        # 確定ボタン（シーケンス図のconfirm()イベントを発生させるトリガー）
        self.btn_confirm = tk.Button(
            self.root,
            text="確定",
            command=self.click_confirm,
            font=("Arial", 12),
            bg="#4CAF50",
            fg="white",
        )
        self.btn_confirm.pack(pady=15)

    def click_confirm(self):
        """
        登録済ユーザーが確定を指示したときのイベントハンドラ（シーケンス図のconfirm()に対応）
        """
        # 入力されたグループ名を取得
        group_name = self.entry_group_name.get().strip()

        print(
            f"[View] 確定ボタンがクリックされました。グループ名: {group_name}"
        )

        try:
            # 1. GroupManagerにグループ作成を依頼 (シーケンス図の create_group)
            group_id = self.group_manager.create_group(
                self.current_user_id, group_name
            )

            # 2. GroupManagerにカレンダーの追加を依頼 (シーケンス図の add_group_calendar)
            self.group_manager.add_group_calendar(
                self.current_user_id, group_id
            )

            # 成功メッセージを表示
            messagebox.showinfo(
                "成功", f"グループ「{group_name}」を作成し、カレンダーを切り替えました。"
            )

            # 次の画面に進むか、画面を閉じる処理（今回はウィンドウを閉じます）
            self.root.destroy()

        except ValueError as ve:
            # 入力エラー（文字数制限や未入力など）の場合のアラート
            messagebox.showwarning("入力エラー", str(ve))
        except Exception as e:
            messagebox.showerror("エラー", f"予期せぬエラーが発生しました: {e}")


# アプリケーションの起動
if __name__ == "__main__":
    # ロジック層のインスタンス化
    manager = DummyGroupManager()

    # tkinter本体の初期化
    root = tk.Tk()

    # 画面の表示
    app = GroupCreationView(root, manager)

    # イベントループ（画面を閉じられるまで待機する状態）を開始
    root.mainloop()