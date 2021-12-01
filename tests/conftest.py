from pathlib import Path

import pytest as pytest

from db.db_connection import DBConnection
from models.user import User


@pytest.fixture
def setup():
    path = "test.db"
    url = f"sqlite:///{path}"
    yield DBConnection(url)
    db_path = Path(path)
    db_path.unlink(missing_ok=True)


@pytest.fixture
def row_html():
    with open("tests/template.html", "r") as file:
        return file.read()


@pytest.fixture
def row_css():
    with open("tests/template.css", "r") as file:
        return file.read()


@pytest.fixture
def new_user():
    user = User(
        login="JoshBush23",
        password="Test123_123",
        email="test@mail.ru"
    )
    return user

#
# @pytest.fixture
# def user_credentials():
#     user = {
#         "login": "Test123",
#         "password": "Test123"
#     }
#     return user
#
#
# @pytest.fixture
# def user_pass_settings():
#     user_settings = {
#         "url": "https://ksu.edu.ru/",
#         "html_tags": ["div", "head"],
#         "css_tags": ["footer"],
#         "js_tags": ["name", "body"]
#     }
#     return user_settings
#
#
# @pytest.fixture
# def user_fail_settings():
#     user_settings = {
#         "url": "https://www.asdfghjkl.com/",
#         "html_tags": ["spider_man"],
#         "css_tags": ["69Abobus"],
#         "js_tags": ["1488Polish"]
#     }
#     return user_settings
