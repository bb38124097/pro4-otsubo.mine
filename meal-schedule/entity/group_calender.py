from datetime import date
from typing import Dict, Optional, List
from entity.user_calendar import UserCalendar
from entity.meal_schedule import MealSchedule

class GroupCalendar:
    def __init__(self, group_id: str, group_name: str):
        self.group_id = group_id
        self.group_name = group_name
        # ユーザーID (str) をキー、その人のUserCalendarオブジェクトを値とする辞書
        # 例: { "user_father": UserCalendarオブジェクト, "user_mother": UserCalendarオブジェクト }
        self.user_calendars: Dict[str, UserCalendar] = {}

    def add_user_calendar(self, user_calendar: UserCalendar):
        """グループにメンバーの個人カレンダーを紐付ける"""
        self.user_calendars[user_calendar.user_id] = user_calendar

    def get_member_schedule_by_date(self, user_id: str, target_date: date) -> Optional[MealSchedule]:
        """特定のメンバーの、特定の日付のスケジュールを取得する"""
        user_cal = self.user_calendars.get(user_id)
        if user_cal:
            return user_cal.get_schedule_by_date(target_date)
        return None

    def get_group_schedules_by_date(self, target_date: date) -> Dict[str, Optional[MealSchedule]]:
        """特定の日付の、家族全員のスケジュールをまとめて取得する（一覧表示用）"""
        group_status = {}
        for user_id, user_cal in self.user_calendars.items():
            group_status[user_id] = user_cal.get_schedule_by_date(target_date)
        return group_status


# ==========================================
# 動作確認用のテストコード
# ==========================================
if __name__ == "__main__":
    print("--- GroupCalendarクラスのテスト ---")
    
    # 1. グループカレンダーの作成
    my_group_cal = GroupCalendar(group_id="g_001", group_name="大坪・三根家")
    
    # 2. お父さんのカレンダーを作って登録
    father_cal = UserCalendar(user_id="father")
    sch_father = MealSchedule(schedule_id="s_01", user_id="father", target_date=date(2026, 7, 5))
    sch_father.update_meal_status(needs_meal=True)
    sch_father.update_return_time(return_time="19:00")
    father_cal.add_or_update_schedule(sch_father)
    
    my_group_cal.add_user_calendar(father_cal)
    
    # 3. 妹のカレンダーを作って登録
    sister_cal = UserCalendar(user_id="sister")
    sch_sister = MealSchedule(schedule_id="s_02", user_id="sister", target_date=date(2026, 7, 5))
    sch_sister.update_meal_status(needs_meal=False) # ご飯いらない
    sch_sister.update_return_time(return_time="21:30")
    sister_cal.add_or_update_schedule(sch_sister)
    
    my_group_cal.add_user_calendar(sister_cal)
    
    # 4. 7月5日の家族全員の予定を一覧で取得して確認
    print(f"\n【{my_group_cal.group_name}】2026年7月5日の晩御飯状況：")
    all_schedules = my_group_cal.get_group_schedules_by_date(date(2026, 7, 5))
    
    for user, sch in all_schedules.items():
        if sch:
            status = "必要" if sch.needs_meal else "不要"
            print(f"・{user} -> ご飯: {status}, 帰宅予定: {sch.return_time}")
        else:
            print(f"・{user} -> 未入力")