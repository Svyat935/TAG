import json
from datetime import datetime, timedelta

from flask import Flask, request

from auth.user_reg_auth import UserRegAuth
from models.site_settings import SiteSettings
from models.user import User
from settings.controller_site_settings import ControllerSiteSettings
from validators.settings_validator import SettingsValidator

app = Flask(__name__)

user_reg_auth = UserRegAuth()
controller_site_settings = ControllerSiteSettings()


@app.route("/version")
def version():
    return "Version 1.0.0"


@app.route("/user/reg", methods=["POST"])
def create_user():
    user = User(
        name=request.form["name"],
        surname=request.form["surname"],
        email=request.form["email"],
        login=request.form["login"],
        password=request.form["password"],
    )
    try:
        user_reg_auth.registration(user)

    except ValueError as info:
        return {"status": "error", "message": str(info)}, 400
    return {"status": "ok"}, 200


@app.route("/user/auth", methods=["POST"])
def check_user():
    token = user_reg_auth.authorization(request.form["login"], request.form["password"])
    if token:
        return {"status": "ok", "token": token}, 200
    return {"status": "authentication is failed."}, 400


@app.route("/settings/create/site", methods=["POST"])
def create_site_settings():
    try:
        token = request.headers["JWT"]
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
        start_date=datetime.now(),
    )
    controller_site_settings.create_site_settings(site_settings)
    return {"status": "ok"}


@app.route("/settings/update/site", methods=["POST"])
def update_site_settings():
    pass


@app.route("/settings/update/user", methods=["POST"])
def update_user_settings():
    pass
