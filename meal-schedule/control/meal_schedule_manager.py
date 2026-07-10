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
                meal_type TEXT NOT NULL,
                required INTEGER NOT NULL,
                return_time TEXT,
                message TEXT
            )
        """)

        conn.commit()
        conn.close()

    def set_one_meal_schedule(self, account_id, target_date, meal_type, required, return_time, message):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO meal_schedules (
                account_id, target_date, meal_type, required, return_time, message
            ) VALUES (?, ?, ?, ?, ?, ?)
        """, (
            account_id,
            target_date,
            meal_type,
            int(required),
            return_time,
            message
        ))

        conn.commit()
        conn.close()

    def get_schedule(self, account_id, target_date, meal_type):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT required, return_time, message
            FROM meal_schedules
            WHERE account_id = ? AND target_date = ? AND meal_type = ?
            ORDER BY schedule_id DESC
            LIMIT 1
        """, (account_id, target_date, meal_type))

        row = cursor.fetchone()
        conn.close()

        if row is None:
            return None

        return {
            "required": bool(row[0]),
            "return_time": row[1],
            "message": row[2]
        }
    
    def get_group_schedule(self, group_id, target_date):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                users.user_name,
                meal_schedules.meal_type,
                meal_schedules.required,
                meal_schedules.return_time,
                meal_schedules.message
            FROM meal_schedules
            JOIN users
                ON meal_schedules.account_id = users.account_id
            JOIN group_members
                ON users.account_id = group_members.account_id
            WHERE
                group_members.group_id = ?
                AND meal_schedules.target_date = ?
            ORDER BY
                users.user_name,
                meal_schedules.meal_type
        """, (group_id, target_date))

        schedules = cursor.fetchall()

        conn.close()

        return schedules

