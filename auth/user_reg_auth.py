from datetime import datetime, timedelta
from typing import Optional, Dict

import jwt
import bcrypt

from db.db_connection import DBConnection
from models.user import User
from validators.user_validator import UserValidator

JWT_KEY_DEFAULT = "Lw8cIjl5oKXV2EUdCq7uyznfhmQJeNp1"
JWT_EXPIRE_DEFAULT = datetime.utcnow() + timedelta(days=10)


class UserRegAuth:
    def __init__(
        self,
        db_connection: DBConnection = DBConnection(),
        jwt_key: str = JWT_KEY_DEFAULT,
        jwt_expire: datetime = JWT_EXPIRE_DEFAULT,
    ):
        self._db = db_connection
        self._jwt_key = jwt_key
        self._jwt_expire = jwt_expire

    def authorization(self, login: str, password: str) -> Optional[str]:
        with self._db.create_connection() as conn:
            user_found: User = conn.query(User).filter(User.login == login).first()
            if bcrypt.checkpw(password.encode(), user_found.password.encode()):
                token = jwt.encode(
                    payload={"exp": self._jwt_expire, "user_id": user_found.id},
                    key=self._jwt_key,
                )
                return token
        return None

    def registration(self, user: User) -> User:
        UserValidator.validate_email(user.email)
        UserValidator.validate_login(user.login)
        UserValidator.validate_password(user.password)
        if user.name is not None:
            UserValidator.validate_name(user.name)
        if user.surname is not None:
            UserValidator.validate_surname(user.surname)

        with self._db.create_connection() as conn:
            user_found: User = conn.query(User).filter(User.login == user.login).first()
            if user_found:
                raise ValueError("User already exists.")

            user.password = bcrypt.hashpw(
                password=user.password.encode(), salt=bcrypt.gensalt()
            ).decode()
            conn.add(user)
            conn.commit()

        return user

    def parse_token(self, token: str) -> Optional[Dict[str, str]]:
        try:
            payload = jwt.decode(token, self._jwt_key, algorithms="HS256")
        except jwt.exceptions.ExpiredSignatureError:
            return None
        except jwt.DecodeError:
            return None
        return payload

    def get_user(self, user_id) -> Optional[User]:
        with self._db.create_connection() as conn:
            user = conn.query(User).filter(User.id == user_id).first()
            return user
