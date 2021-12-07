from flask import Flask

app = Flask(__name__)


@app.route("/version")
def version():
    return "Version 1.0.0"


@app.route("/user/reg")
def create_user():
    pass


@app.route("/user/auth")
def check_user():
    pass
