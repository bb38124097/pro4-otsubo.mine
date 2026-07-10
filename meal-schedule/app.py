from flask import Flask, render_template, request, redirect
from control.account_manager import AccountManager

app = Flask(__name__)

account_manager = AccountManager()


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
    user = account_manager.get_current_user()
    return render_template("main.html", user=user)


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5001,
        debug=True
    )