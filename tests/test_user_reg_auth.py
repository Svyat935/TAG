from datetime import timedelta, datetime

from auth.user_reg_auth import UserRegAuth
from models.user import User


def test_registration_user(setup, new_user):
    db_connection = setup
    user_reg_auth = UserRegAuth(db_connection)
    user_reg_auth.registration(new_user)
    with db_connection.create_connection() as conn:
        user = conn.query(User).filter(User.login == new_user.login).first()

    assert user


def test_authorization_user(setup, new_user):
    db_connection = setup
    login, password = new_user.login, new_user.password
    user_reg_auth = UserRegAuth(db_connection)
    user_reg_auth.registration(new_user)
    token = user_reg_auth.authorization(login, password)

    assert token


def test_parse_token_positive(setup, new_user):
    db_connection = setup
    login, password = new_user.login, new_user.password
    user_reg_auth = UserRegAuth(db_connection)
    user_reg_auth.registration(new_user)
    token = user_reg_auth.authorization(login, password)
    result = user_reg_auth.parse_token(token)

    assert result["user_id"] == 1


def test_parse_token_negative_expire_time(setup, new_user):
    db_connection = setup
    login, password = new_user.login, new_user.password
    user_reg_auth = UserRegAuth(
        db_connection, jwt_expire=datetime.utcnow() - timedelta(days=10)
    )
    user_reg_auth.registration(new_user)
    token = user_reg_auth.authorization(login, password)
    result = user_reg_auth.parse_token(token)
    assert result is None


def test_parse_token_negative_invalid_token():
    user_reg_auth = UserRegAuth(None)
    result = user_reg_auth.parse_token("token")
    assert result is None
