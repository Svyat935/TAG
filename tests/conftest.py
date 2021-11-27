import pytest as pytest


@pytest.fixture
def new_user():
    user = {
        "login": "JoshBush23_|",
        "password": "Test123_123"
    }
    return user


@pytest.fixture
def user_credentials():
    user = {
        "login": "Test123",
        "password": "Test123"
    }
    return user


@pytest.fixture
def user_pass_settings():
    user_settings = {
        "url": "https://ksu.edu.ru/",
        "html_tags": ["div", "head"],
        "css_tags": ["footer"],
        "js_tags": ["name", "body"]
    }
    return user_settings


@pytest.fixture
def user_fail_settings():
    user_settings = {
        "url": "https://www.asdfghjkl.com/",
        "html_tags": ["spider_man"],
        "css_tags": ["69Abobus"],
        "js_tags": ["1488Polish"]
    }
    return user_settings


@pytest.fixture
def site_data():
    data = {
        "url": "https://www.asdfghjkl.com/",
        "tree": [["head", "", [["meta", 'charset="UTF-8"', []]], ["title", 'MYSITE', []]], ["body", "", [["div", "", [["h1", "MYSITE GOOD", []]]]]]],
        "multimedia_content": [["audio", "controls", [["source", 'src="myAudio.mp3" type="audio/mpeg"', []]]]],
        "scripts": [['script', 'alert("HI");', []]]
    }
    return data
