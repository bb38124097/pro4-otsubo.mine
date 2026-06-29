import tkinter as tk
from tkinter import messagebox


# シーケンス図の :AccountManager（コントロール層）を模したクラス
class DummyAccountManager:

    def delete_account(self, user_id: str) -> None:
        """
        アカウント情報をシステム、グループ、カレンダーから完全に削除する
        (シーケンス図の deleteAccount() から後ろの一連の流れに対応)
        """
        print(f"[Manager] ユーザーID: {user_id} の削除処理を開始します。")
        print(f"[Manager] :User エンティティから delete(accountID) を実行。")
        print(f"[Manager] :UserCalender から delete() を実行。")
        print(f"[Manager] :GroupManager へ通知し、:Group からメンバー削除を実行。")
        print(f"[Manager] :GroupCalender から delete() を実行。")
        print(f"[Manager] アカウントの完全削除が完了しました。")


# シーケンス図の :Delete Account Page（境界層）を表すクラス
class DeleteAccountView:

    def __init__(self, root: tk.Tk, account_manager: DummyAccountManager):
        self.root = root
        self.account_manager = account_manager

        # テスト用の疑似ログインユーザーID
        self.current_user_id = "test_user_01"

        # ウィンドウの設定
        self.root.title("アカウント削除")
        self.root.geometry("400x200")

        self.create_widgets()

    def create_widgets(self):
        """
        システムが、削除するか否かの確認画面を表示する処理（シーケンス図の display() に対応）
        """
        # 注意喚起のラベル
        self.label_warning = tk.Label(
            self.root,
            text="アカウントを削除すると、これまでの食事予定や\n所属しているグループのデータがすべて削除されます。\n本当に削除しますか？",
            font=("Arial", 11),
            fg="#f44336",
            justify=tk.CENTER,
        )
        self.label_warning.pack(pady=25)

        # ボタン配置用のフレーム
        self.btn_frame = tk.Frame(self.root)
        self.btn_frame.pack(pady=10)

        # 削除するボタン（シーケンス図の confirm() をトリガーするボタン）
        self.btn_delete = tk.Button(
            self.btn_frame,
            text="削除する",
            command=self.click_delete,
            font=("Arial", 11),
            bg="#f44336",
            fg="white",
            width=12,
        )
        self.btn_delete.pack(side=tk.LEFT, padx=10)

        # 削除しないボタン（代替フロー：メニューやメイン画面に戻る動きに対応）
        self.btn_cancel = tk.Button(
            self.btn_frame,
            text="削除しない",
            command=self.click_cancel,
            font=("Arial", 11),
            bg="#9E9E9E",
            fg="white",
            width=12,
        )
        self.btn_cancel.pack(side=tk.LEFT, padx=10)

    def click_delete(self):
        """
        登録済ユーザーが「削除する」を指示したときのイベントハンドラ
        """
        print("[View] 「削除する」が選択されました。")

        # 二重チェック用の確認ダイアログ
        if messagebox.askyesno(
            "最終確認", "本当にアカウントを削除しますか？この操作は取り消せません。"
        ):
            try:
                # 1. AccountManagerにアカウント削除を依頼（シーケンス図の deleteAccount()）
                self.account_manager.delete_account(self.current_user_id)

                messagebox.showinfo(
                    "削除完了",
                    "アカウントは正常に削除されました。ご利用ありがとうございました。",
                )

                # 2. 削除後はメイン画面ではなく、サインアップ画面（SignUp Page）を表示させて終了する流れを再現
                print(
                    "[View] ログイン画面/サインアップ画面（SignUp Page）へ遷移します。"
                )
                self.root.destroy()

            except Exception as e:
                messagebox.showerror(
                    "エラー", f"アカウントの削除に失敗しました: {e}"
                )

    def click_cancel(self):
        """
        登録済ユーザーが「削除しない」を指示したときのイベントハンドラ（代替フロー 3a に対応）
        """
        print(
            "[View] 「削除しない」が選択されました。メインメニュー画面に戻ります。"
        )
        # 画面を閉じて遷移元（メインページ）へ処理を戻す
        self.root.destroy()


# アプリケーションの起動（単体テスト用）
if __name__ == "__main__":
    manager = DummyAccountManager()
    root = tk.Tk()
    app = DeleteAccountView(root, manager)
    root.mainloop()