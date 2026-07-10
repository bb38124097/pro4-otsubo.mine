from flask import Flask, render_template, request, redirect
from control.account_manager import AccountManager
from control.meal_schedule_manager import MealScheduleManager
from control.group_manager import GroupManager
import calendar
from datetime import date

account_manager = AccountManager()
group_manager = GroupManager()
meal_manager = MealScheduleManager()

app = Flask(__name__)



@app.route("/")
def index():
    if account_manager.has_user():
        return redirect("/main")
    return render_template("index.html")


@app.route("/register")
def register():
    return render_template("register.html")


@app.route("/register", methods=["POST"])
def register_post():
    user_name = request.form["user_name"]

    if not account_manager.check_user_name_length(user_name):
        return render_template(
            "register.html",
            error="ユーザー名は1～20文字で入力してください"
        )

    account_manager.register_user(user_name)

    return redirect("/main")


@app.route("/main")
def main():

    year = request.args.get("year", type=int)
    month = request.args.get("month", type=int)

    if year is None or month is None:
        today = date.today()
        year = today.year
        month = today.month

    month_calendar = calendar.monthcalendar(year, month)

    prev_year = year
    prev_month = month - 1
    if prev_month == 0:
        prev_month = 12
        prev_year -= 1

    next_year = year
    next_month = month + 1
    if next_month == 13:
        next_month = 1
        next_year += 1

    return render_template(
        "main.html",
        year=year,
        month=month,
        month_calendar=month_calendar,
        prev_year=prev_year,
        prev_month=prev_month,
        next_year=next_year,
        next_month=next_month
    )


@app.route("/meal/<target_date>")
def meal(target_date):

    user = account_manager.get_current_user()

    group_id = group_manager.get_user_group_id(
        user.account_id
    )

    schedules = []

    if group_id is not None:
        schedules = meal_manager.get_group_schedule(
            group_id,
            target_date
        )

    return render_template(
        "meal.html",
        target_date=target_date,
        schedules=schedules
    )

@app.route(
    "/meal_detail/<target_date>/<meal_type>",
    methods=["GET", "POST"]
)
def meal_detail(target_date, meal_type):

    if request.method == "POST":

        return_time = request.form["return_time"]
        message = request.form["message"]

        user = account_manager.get_current_user()

        account_id = user.account_id
        
        meal_manager.set_one_meal_schedule(
            account_id,
            target_date,
            meal_type,
            True,
            return_time,
            message
        )

        return redirect("/main")

    return render_template(
        "meal_detail.html",
        target_date=target_date,
        meal_type=meal_type
    )

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5001,
        debug=True
    )
