import json
from datetime import datetime, timedelta

from flask import Flask, request, render_template, redirect, url_for

from auth.user_reg_auth import UserRegAuth
from models.site_settings import SiteSettings
from models.user import User
from settings.controller_site_settings import ControllerSiteSettings
from validators.settings_validator import SettingsValidator
from validators.user_validator import UserValidator

app = Flask(__name__)

user_reg_auth = UserRegAuth()
controller_site_settings = ControllerSiteSettings()
user_validator = UserValidator()


@app.route("/")
@app.route("/auth", methods=["GET", "POST"])
def authorization():
    if request.method == "GET":
        return render_template("auth.html")

    login = user_validator.validate_login(request.form["login"])
    password = user_validator.validate_password(request.form["password"])
    token = user_reg_auth.authorization(login, password)
    if token:
        response = redirect("/main_page")
        response.set_cookie("JWT", token)
        return response
    return {"status": "authentication is failed."}, 400


@app.route("/reg", methods=["GET", "POST"])
def registration():
    if request.method == "GET":
        return render_template("reg.html")

    login, password = request.form["login"], request.form["password"]
    user = User(
        name=request.form["name"],
        surname=request.form["surname"],
        email=request.form["email"],
        login=login,
        password=password,
    )
    try:
        user_reg_auth.registration(user)
    except ValueError as info:
        return {"status": "error", "message": str(info)}, 400

    token = user_reg_auth.authorization(login, password)

    response = redirect("/main_page")
    response.set_cookie("JWT", token)
    return response


@app.route("/main_page", methods=["GET"])
def main_page():
    if not request.cookies.get("JWT"):
        return redirect("/")
    return render_template("main_page.html")


@app.route("/settings/create/site_settings", methods=["GET", "POST"])
def page_site_settings():
    if request.method == "GET":
        token = request.cookies.get("JWT")
        if not token:
            return {"status": "error", "message": "JWT isn't existed"}, 400
        user_id = user_reg_auth.parse_token(token)["user_id"]
        if not user_id:
            return {"status": "error", "message": "JWT is invalid."}, 400
        user = user_reg_auth.get_user(user_id)
        settings = controller_site_settings.get_user_site_settings(user)
        # IF
        settings = settings.search_settings
        settings = json.loads(settings)
        settings["html_tags"] = " ".join(settings["html_tags"])
        settings["css_tags"] = " ".join(settings["css_tags"])
        return render_template("site_settings.html", settings=settings)

    try:
        token = request.cookies["JWT"]
    except KeyError:
        return {"status": "error", "message": "JWT isn't existed."}, 400
    user_id = user_reg_auth.parse_token(token)["user_id"]
    if not user_id:
        return {"status": "error", "message": "JWT is invalid."}, 400
    user = user_reg_auth.get_user(user_id)

    settings = request.json
    if settings is None:
        return {"status": "error", "message": "JSON is empty"}, 400

    try:
        SettingsValidator.validate_site_settings(settings)
    except ValueError as info:
        return {"status": "error", "message": str(info)}, 400

    interval = settings["interval"]
    if interval == "1 day":
        interval = timedelta(days=1)
    elif interval == "1 hour":
        interval = timedelta(hours=1)
    else:
        interval = timedelta(minutes=1)

    site_settings = SiteSettings(
        user_id=user.id,
        url=settings["url"],
        search_settings=json.dumps(settings),
        search_interval=interval,
        current_date=datetime.now(),
    )
    controller_site_settings.create_site_settings(site_settings)
    return {"status": "ok"}


@app.route("/settings/update/user", methods=["POST"])
def create_user_settings():
    pass
