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
    