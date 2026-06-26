import tkinter as tk
from tkinter import messagebox


# シーケンス図の :GroupManager（コントロール層）を模したクラス
class DummyGroupManager:

    def check_name_length(self, group_name: str) -> bool:
        """
        グループ名の文字数制限をチェックする（20文字以内）
        """
        if len(group_name) > 20:  # 20文字制限を追加
            return False
        return True

    def create_group(self, user_id: str, group_name: str) -> str:
        if not group_name:
            raise ValueError("グループ名を入力してください。")
        return "generated_group_id_123"

    def add_group_calendar(self, user_id: str, group_id: str) -> None:
        print(
            f"[Manager] ユーザー:{user_id} のカレンダーに グループ:{group_id} を紐づけました。"
        )


# シーケンス図の :GroupCreationView（境界層）を表すクラス
class GroupCreationView:

    def __init__(self, root: tk.Tk, group_manager: DummyGroupManager):
        self.root = root
        self.group_manager = group_manager
        self.current_user_id = "test_user_01"

        self.root.title("グループ作成")
        self.root.geometry("400x200")
        self.create_widgets()

    def create_widgets(self):
        self.label = tk.Label(
            self.root, text="グループ名を入力してください\n（20文字以内）", font=("Arial", 11)
        )
        self.label.pack(pady=15)

        self.entry_group_name = tk.Entry(self.root, font=("Arial", 12), width=30)
        self.entry_group_name.pack(pady=10)

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
        group_name = self.entry_group_name.get().strip()
        print(
            f"[View] 確定ボタンがクリックされました。グループ名: {group_name}"
        )

        # 1. 20文字制限のバリデーションを呼び出す
        if not self.group_manager.check_name_length(group_name):
            messagebox.showwarning(
                "入力エラー",
                "グループ名は20文字以内で入力してください。",
            )
            return

        try:
            group_id = self.group_manager.create_group(
                self.current_user_id, group_name
            )
            self.group_manager.add_group_calendar(
                self.current_user_id, group_id
            )

            messagebox.showinfo(
                "成功", f"グループ「{group_name}」を作成しました。"
            )
            self.root.destroy()

        except ValueError as ve:
            messagebox.showwarning("入力エラー", str(ve))
        except Exception as e:
            messagebox.showerror("エラー", f"予期せぬエラーが発生しました: {e}")


if __name__ == "__main__":
    manager = DummyGroupManager()
    root = tk.Tk()
    app = GroupCreationView(root, manager)
    root.mainloop()