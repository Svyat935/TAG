import re

REGEX_EMAIL = r'\b[A-Za-z0-9.]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
REGEX_LOGIN = r'[\-_A-Za-z0-9.]+'


class UserValidator:
    @staticmethod
    def validate_name(name: str):
        if not 0 < len(name) < 256:
            raise ValueError("Email doesn't has length less 1 and more 255 symbols.")
        return name

    @staticmethod
    def validate_surname(surname: str):
        return UserValidator.validate_name(surname)

    @staticmethod
    def validate_login(login: str):
        if not 5 < len(login) < 256:
            raise ValueError("Email doesn't has length less 6 and more 255 symbols.")
        if not re.fullmatch(REGEX_LOGIN, login):
            raise ValueError("Email is invalidated by the validation rule.")

    @staticmethod
    def validate_email(email: str):
        if not 5 < len(email) < 31:
            raise ValueError("Email doesn't has length less 6 and more 30 symbols.")
        if not re.fullmatch(REGEX_EMAIL, email):
            raise ValueError("Email is invalidated by the validation rule.")
        return email

    @staticmethod
    def validate_password(password: str):
        if not 7 < len(password) < 256:
            raise ValueError("Password doesn't has length less 8 and more 255 symbols.")
