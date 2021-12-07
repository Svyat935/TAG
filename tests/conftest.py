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
    user = User(login="JoshBush23", password="Test123_123", email="test@mail.ru")
    return user


@pytest.fixture
def site_settings():
    settings = {
        "url": ["https://www.futuretimeline.net/index.htm#timeline"],
        "html_tags": ["meta", "link"],
        "css_tags": ["button"],
        "interval": "1 day",
    }
    return settings
