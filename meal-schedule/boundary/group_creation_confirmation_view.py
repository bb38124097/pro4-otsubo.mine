import tkinter as tk
from tkinter import messagebox


# シーケンス図の :GroupManager（コントロール層）を模したクラス
class DummyGroupManager:

    def create_group(self, user_id: str, group_name: str) -> str:
        if not group_name:
            raise ValueError("グループ名が正しくありません。")
        # 本来はここでDBに登録してIDを発行します
        return "generated_group_id_123"

    def add_group_calendar(self, user_id: str, group_id: str) -> None:
        # 本来はここでユーザーとグループカレンダーを紐づけます
        print(
            f"[Manager] ユーザー:{user_id} のカレンダーに グループ:{group_id} を紐づけました。"
        )


# シーケンス図の :GroupCreationConfirmationView（境界層）を表すクラス
class GroupCreationConfirmationView:

    def __init__(
        self, root: tk.Tk, group_manager: DummyGroupManager, group_name: str
    ):
        self.root = root
        self.group_manager = group_manager
        self.group_name = group_name

        # テスト用の疑似ログインユーザーID
        self.current_user_id = "test_user_01"

        # ウィンドウの設定
        self.root.title("グループ作成確認")
        self.root.geometry("400x250")

        # 画面コンポーネント（要素）の作成
        self.create_widgets()

    def create_widgets(self):
        """
        システムが、ユーザーネームの確認画面を表示し、グループ名を出力する処理
        """
        # 確認メッセージ
        self.label_title = tk.Label(
            self.root,
            text="以下の内容でグループを作成しますか？",
            font=("Arial", 12),
        )
        self.label_title.pack(pady=20)

        # 入力されたグループ名の表示
        self.label_group_name = tk.Label(
            self.root,
            text=f"グループ名: {self.group_name}",
            font=("Arial", 14, "bold"),
            fg="#333333",
        )
        self.label_group_name.pack(pady=15)

        # ボタンを横並びにするためのフレーム
        self.btn_frame = tk.Frame(self.root)
        self.btn_frame.pack(pady=20)

        # 登録するボタン
        self.btn_register = tk.Button(
            self.btn_frame,
            text="登録する",
            command=self.click_register,
            font=("Arial", 11),
            bg="#4CAF50",
            fg="white",
            width=12,
        )
        self.btn_register.pack(side=tk.LEFT, padx=10)  # エラー箇所を修正

        # 戻るボタン（キャンセル用）
        self.btn_cancel = tk.Button(
            self.btn_frame,
            text="戻る",
            command=self.root.destroy,
            font=("Arial", 11),
            bg="#f44336",
            fg="white",
            width=12,
        )
        self.btn_cancel.pack(side=tk.LEFT, padx=10)  # エラー箇所を修正

    def click_register(self):
        """
        登録済ユーザーが確定（登録）を指示したときのイベントハンドラ
        """
        print("[View] 登録するボタンがクリックされました。")

        try:
            # 1. GroupManagerにグループ作成を依頼
            group_id = self.group_manager.create_group(
                self.current_user_id, self.group_name
            )
            print(f"[View] グループが作成されました。ID: {group_id}")

            # 2. GroupManagerにカレンダーの追加を依頼
            self.group_manager.add_group_calendar(
                self.current_user_id, group_id
            )

            # 成功メッセージを表示
            messagebox.showinfo(
                "登録完了",
                f"グループ「{self.group_name}」の登録が完了しました！",
            )

            # 画面を閉じる
            self.root.destroy()

        except Exception as e:
            messagebox.showerror("エラー", f"登録に失敗しました: {e}")


# アプリケーションの起動（単体テスト用）
if __name__ == "__main__":
    manager = DummyGroupManager()
    root = tk.Tk()

    # テスト用に、前の画面から「サンプルグループ」という名前が渡されてきたと仮定して起動
    app = GroupCreationConfirmationView(
        root, manager, group_name="サンプルグループ"
    )

    root.mainloop()