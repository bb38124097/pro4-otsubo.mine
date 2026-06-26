import tkinter as tk
from tkinter import messagebox


# シーケンス図の :GroupManager（コントロール層）を模したクラス
class DummyGroupManager:

    def check_member_availability(self, group_id: str, account_id: str) -> bool:
        """
        ユーザーが他のグループに所属していないか確認する
        """
        if not account_id:
            raise ValueError("アカウントIDを入力してください。")
        # テスト用に「already」という文字が入っていたら参加不可（登録済み）とする模擬ロジック
        if "already" in account_id:
            return False
        return True

    def add_member_to_group(self, group_id: str, account_id: str) -> None:
        """
        グループにメンバーを追加し、各種Entityの登録・カレンダー連携を指示する
        """
        print(
            f"[Manager] グループ:{group_id} に ユーザー:{account_id} を追加しました。"
        )
        print(f"[Manager] :User へのグループID登録を完了しました。")
        print(f"[Manager] :Group へのアカウントID登録を完了しました。")
        print(f"[Manager] :GroupCalender へのリンク処理を完了しました。")


# シーケンス図の :AddMemberView（境界層）を表すクラス
class AddMemberView:

    def __init__(self, root: tk.Tk, group_manager: DummyGroupManager):
        self.root = root
        self.group_manager = group_manager

        # テスト用の現在のグループID
        self.current_group_id = "generated_group_id_123"

        # ウィンドウの設定
        self.root.title("メンバー追加")
        self.root.geometry("400x200")

        # 画面コンポーネント（要素）の作成
        self.create_widgets()

    def create_widgets(self):
        """
        システムが、メンバー追加画面を表示する処理（シーケンス図の display() に対応）
        """
        # ラベル
        self.label = tk.Label(
            self.root,
            text="追加するメンバーのアカウントIDを入力してください",
            font=("Arial", 11),
        )
        self.label.pack(pady=20)

        # アカウントID入力欄（シーケンス図の submit(accountID) で送られる値）
        self.entry_account_id = tk.Entry(self.root, font=("Arial", 12), width=30)
        self.entry_account_id.pack(pady=5)

        # ボタン配置用のフレーム
        self.btn_frame = tk.Frame(self.root)
        self.btn_frame.pack(pady=15)

        # 追加ボタン（シーケンス図の confirm() イベントを発生させるトリガー）
        self.btn_add = tk.Button(
            self.btn_frame,
            text="追加",
            command=self.click_add,
            font=("Arial", 11),
            bg="#4CAF50",
            fg="white",
            width=10,
        )
        self.btn_add.pack(side=tk.LEFT, padx=10)

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

    def click_add(self):
        """
        ユーザーが確定（追加）を指示したときのイベントハンドラ（シーケンス図の confirm() に対応）
        """
        account_id = self.entry_account_id.get().strip()

        print(f"[View] 追加ボタンがクリックされました。対象ID: {account_id}")

        try:
            # 1. メンバーが追加可能かチェックを依頼 (シーケンス図の checkMemberAvailability)
            is_available = self.group_manager.check_member_availability(
                self.current_group_id, account_id
            )

            if not is_available:
                # すでに別のグループに所属している場合の代替フロー/エラーハンドリング
                messagebox.showwarning(
                    "追加不可",
                    "指定されたユーザーは既に別のグループに所属しています。",
                )
                return

            # 2. 利用可能な場合、グループへの追加処理を依頼 (シーケンス図の addMemberToGroup)
            self.group_manager.add_member_to_group(
                self.current_group_id, account_id
            )

            # 成功メッセージを表示
            messagebox.showinfo(
                "追加完了", f"ユーザー「{account_id}」をグループに追加しました。"
            )

            # 画面を閉じる
            self.root.destroy()

        except ValueError as ve:
            messagebox.showwarning("入力エラー", str(ve))
        except Exception as e:
            messagebox.showerror("エラー", f"予期せぬエラーが発生しました: {e}")


# アプリケーションの起動（単体テスト用）
if __name__ == "__main__":
    manager = DummyGroupManager()
    root = tk.Tk()
    app = AddMemberView(root, manager)
    root.mainloop()