from datetime import date
from typing import Dict, Optional
from entity.meal_schedule import MealSchedule

class UserCalendar:
    def __init__(self, user_id: str):
        self.user_id = user_id
        # 日付 (date型) をキー、MealScheduleオブジェクトを値とする辞書
        # 例: { date(2026, 7, 5): MealScheduleオブジェクト }
        self.schedules: Dict[date, MealSchedule] = {}

    def add_or_update_schedule(self, schedule: MealSchedule):
        """カレンダーにスケジュールを追加または更新する"""
        if schedule.user_id != self.user_id:
            raise ValueError("このスケジュールは別のユーザーのものです。")
        
        self.schedules[schedule.target_date] = schedule

    def get_schedule_by_date(self, target_date: date) -> Optional[MealSchedule]:
        """指定された日付のスケジュールを取得する（なければNone）"""
        return self.schedules.get(target_date)

    def delete_schedule_by_date(self, target_date: date):
        """指定された日付のスケジュールを削除する"""
        if target_date in self.schedules:
            del self.schedules[target_date]


# ==========================================
# 動作確認用のテストコード
# ==========================================
if __name__ == "__main__":
    print("--- UserCalendarクラスのテスト ---")
    
    # 1. カレンダーの作成（お父さん用）
    father_calendar = UserCalendar(user_id="user_father")
    
    # 2. 7月5日の予定を作ってカレンダーに登録してみる
    day1 = date(2026, 7, 5)
    sch1 = MealSchedule(schedule_id="sch_001", user_id="user_father", target_date=day1)
    sch1.update_meal_status(needs_meal=True)
    sch1.update_return_time(return_time="19:00")
    
    father_calendar.add_or_update_schedule(sch1)
    
    # 3. 7月6日の予定（ご飯いらない日）も登録してみる
    day2 = date(2026, 7, 6)
    sch2 = MealSchedule(schedule_id="sch_002", user_id="user_father", target_date=day2)
    sch2.update_meal_status(needs_meal=False)
    
    father_calendar.add_or_update_schedule(sch2)
    
    # 4. カレンダーからデータを取り出して確認
    print(f"【登録された予定の数】: {len(father_calendar.schedules)}件")
    
    saved_sch1 = father_calendar.get_schedule_by_date(day1)
    if saved_sch1:
        print(f"7月5日の予定 -> 食事: {saved_sch1.needs_meal}, 帰宅: {saved_sch1.return_time}")
        
    saved_sch2 = father_calendar.get_schedule_by_date(day2)
    if saved_sch2:
        print(f"7月6日の予定 -> 食事: {saved_sch2.needs_meal}, 帰宅: {saved_sch2.return_time}")