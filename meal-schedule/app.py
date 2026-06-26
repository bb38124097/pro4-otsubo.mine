from flask import Flask

app = Flask(__name__)

@app.route("/")
def index():
    return "食事予定管理システム"

if __name__ == "__main__":
    app.run(debug=True, port=5001)