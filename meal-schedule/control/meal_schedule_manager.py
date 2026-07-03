import re


# シーケンス図・クラス図の :UserCalender / :GroupCalender を模した簡易データベース（メモリ保持用）
# 本来はSQLiteや外部DBに保存する部分を、確認用に辞書型で表現しています
MOCK_DATABASE = {
    "user_schedules": {
        # "ユーザーID_日付": {各時間帯のデータ}
        "test_user_01_2026-06-26": {
            "breakfast": "必要 (帰宅 08:00)",
            "lunch": "不要",
            "dinner": "必要 (帰宅 19:00)",
            "message": "今日は夕飯遅くなります！",
        }
    },
    "group_schedules": {
        # グループカレンダーに同期されたデータ
        "test_user_01_2026-06-26": {
            "breakfast": "必要 (帰宅 08:00)",
            "lunch": "不要",
            "dinner": "必要 (帰宅 19:00)",
            "message": "今日は夕飯遅くなります！",
        }
    },
}


class MealScheduleManager:

    def __init__(self):
        # クラス図の仕様に準拠した属性定数
        self.max_message_length = 30

    def get_schedule_for_date(self, user_id: str, target_date: str) -> dict:
        """
        指定された日付の現在の登録状況を :UserCalender から取得する
        """
        key = f"{user_id}_{target_date}"
        print(f"[Manager] :UserCalender から予定を読み込みます。キー: {key}")

        # 該当日のデータがなければ初期状態を返す
        if key not in MOCK_DATABASE["user_schedules"]:
            return {
                "breakfast": "未登録",
                "lunch": "未登録",
                "dinner": "未登録",
                "message": "（伝言はありません）",
            }
        return MOCK_DATABASE["user_schedules"][key]

    def has_next_step(self, requirement: str) -> bool:
        """
        meal_input_viewでの判定用。理不尽な重複を防ぐため、「必要」ならTrueを返す
        """
        return requirement == "need"

    def check_length(self, message: str) -> bool:
        """
        メッセージの文字数制限をチェックする (シーケンス図の checkLength(message) に対応)
        仕様: maxMessageLength = 30文字
        """
        return len(message) <= self.max_message_length

    def sync_schedule(self, user_id: str, target_date: str, schedule_data: dict):
        """
        変更されたデータを :GroupCalender へ同期する
        (シーケンス図の syncSchedule() に対応)
        """
        key = f"{user_id}_{target_date}"
        MOCK_DATABASE["group_schedules"][key] = schedule_data
        print(f"[Manager] ➔ :GroupCalender への syncSchedule() が成功しました。")

    def set_meal_no_need(self, user_id: str, target_date: str, time_slot: str):
        """
        食事「不要」な場合、即座にUserCalenderに登録し、GroupCalenderへ同期する
        """
        key = f"{user_id}_{target_date}"

        # 既存データを取得、なければ初期化
        current_data = self.get_schedule_for_date(user_id, target_date)
        if current_data["breakfast"] == "未登録":
            current_data = {
                "breakfast": "未登録",
                "lunch": "未登録",
                "dinner": "未登録",
                "message": "（伝言はありません）",
            }

        # 該当の時間帯を「不要」に更新
        current_data[time_slot] = "不要"

        # 1. :UserCalender への保存
        MOCK_DATABASE["user_schedules"][key] = current_data
        print(
            f"[Manager] :UserCalender への登録が完了しました。[{time_slot}: 不要]"
        )

        # 2. :GroupCalender への同期
        self.sync_schedule(user_id, target_date, current_data)

    def set_return_time(
        self, user_id: str, target_date: str, time_slot: str, return_time: str
    ):
        """
        帰宅時間を確定し、UserCalenderに登録、GroupCalenderへ同期する
        (シーケンス図の confirm(..., returnTime) に対応)
        """
        key = f"{user_id}_{target_date}"

        current_data = self.get_schedule_for_date(user_id, target_date)
        if current_data["breakfast"] == "未登録":
            current_data = {
                "breakfast": "未登録",
                "lunch": "未登録",
                "dinner": "未登録",
                "message": "（伝言はありません）",
            }

        # 該当の時間帯を「必要 (帰宅 HH:MM)」に更新
        current_data[time_slot] = f"必要 (帰宅 {return_time})"

        # 1. :UserCalender への登録
        MOCK_DATABASE["user_schedules"][key] = current_data
        print(
            f"[Manager] :UserCalender への登録が完了しました。[{time_slot}: 必要(帰宅 {return_time})]"
        )

        # 2. :GroupCalender への同期
        self.sync_schedule(user_id, target_date, current_data)

    def set_message(
        self, user_id: str, target_date: str, time_slot: str, message: str
    ):
        """
        メッセージをカレンダーに登録し、グループに同期する
        (シーケンス図の set(message) に対応)
        """
        # 事前ガード（文字数制限チェック）
        if not self.check_length(message):
            raise ValueError(
                f"メッセージは{self.max_message_length}文字以内で入力してください。"
            )

        key = f"{user_id}_{target_date}"
        current_data = self.get_schedule_for_date(user_id, target_date)
        if current_data["breakfast"] == "未登録":
            current_data = {
                "breakfast": "未登録",
                "lunch": "未登録",
                "dinner": "未登録",
                "message": "（伝言はありません）",
            }

        # メッセージを更新
        current_data["message"] = message

        # 1. :UserCalender への set(message)
        MOCK_DATABASE["user_schedules"][key] = current_data
        print(f"[Manager] :UserCalender への set(message) が完了しました。")

        # 2. :GroupCalender への syncSchedule()
        self.sync_schedule(user_id, target_date, current_data)


# 簡易動作テスト
if __name__ == "__main__":
    manager = MealScheduleManager()
    print("--- 初期状態の確認 ---")
    print(manager.get_schedule_for_date("test_user_01", "2026-06-26"))

    print("\n--- メッセージ登録のテスト ---")
    manager.set_message(
        "test_user_01", "2026-06-26", "dinner", "遅くなります！"
    )

    print("\n--- 変更後のDB確認 ---")
    print(MOCK_DATABASE["group_schedules"]["test_user_01_2026-06-26"])

import sqlite3


class MealScheduleManager:
    def __init__(self):
        self.db_name = "meal_schedule.db"
        self.create_table()

    def create_table(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS meal_schedules (
                schedule_id INTEGER PRIMARY KEY AUTOINCREMENT,
                account_id INTEGER NOT NULL,
                target_date TEXT NOT NULL,
                breakfast_required INTEGER NOT NULL,
                lunch_required INTEGER NOT NULL,
                dinner_required INTEGER NOT NULL,
                return_time TEXT,
                message TEXT
            )
        """)

        conn.commit()
        conn.close()

    def set_schedule(self, account_id, target_date, breakfast_required,
                     lunch_required, dinner_required, return_time, message):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO meal_schedules (
                account_id,
                target_date,
                breakfast_required,
                lunch_required,
                dinner_required,
                return_time,
                message
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            account_id,
            target_date,
            int(breakfast_required),
            int(lunch_required),
            int(dinner_required),
            return_time,
            message
        ))

        conn.commit()
        conn.close()
    
#222963e99a83bc7aa24f080a3c41135e648b6097
