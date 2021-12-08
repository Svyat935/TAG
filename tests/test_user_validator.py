import pytest

from validators.user_validator import UserValidator


def test_validate_login_positive():
    login = "My.Test-ing_Login123"

    assert UserValidator.validate_login(login)


def test_validate_regex_login_negative():
    login = "MyTestingLogin#$%()Тест"

    with pytest.raises(ValueError) as info:
        UserValidator.validate_login(login)

    assert info.value.args[0] == "Login is invalidated by the validation rule."


def test_validate_login_length_negative():
    login_empty, login_big = "", "A" * 256

    with pytest.raises(ValueError) as info_for_empty:
        UserValidator.validate_login(login_empty)

    with pytest.raises(ValueError) as info_for_big:
        UserValidator.validate_login(login_big)

    assert (
        info_for_empty.value.args[0]
        == info_for_big.value.args[0]
        == "Login doesn't has length less 6 and more 255 symbols."
    )


def test_validate_name_and_surname_positive():
    name = "X_Jack_X"
    surname = "###Daniels###"

    assert UserValidator.validate_name(name) and UserValidator.validate_surname(surname)


def test_validate_name_and_surname_negative():
    name = "Jack" * 64
    surname = ""

    with pytest.raises(ValueError) as info_name:
        UserValidator.validate_name(name)

    with pytest.raises(ValueError) as info_surname:
        UserValidator.validate_surname(surname)

    assert (
        info_name.value.args[0]
        == info_surname.value.args[0]
        == "Value doesn't has length less 1 and more 255 symbols."
    )


def test_validate_email_positive():
    email = "test.test123@mail.com"

    return UserValidator.validate_email(email)


def test_validate_regex_email_negative():
    email = "test-#$%test123@mail.com"

    with pytest.raises(ValueError) as info:
        UserValidator.validate_email(email)

    assert info.value.args[0] == "Email is invalidated by the validation rule."


def test_validate_email_length_negative():
    email_empty, email_big = "", "test" * 10 + "@test.com"

    with pytest.raises(ValueError) as info_for_empty:
        UserValidator.validate_email(email_empty)

    with pytest.raises(ValueError) as info_for_big:
        UserValidator.validate_email(email_big)

    assert (
        info_for_empty.value.args[0]
        == info_for_big.value.args[0]
        == "Email doesn't has length less 6 and more 30 symbols."
    )


def test_validate_password_positive():
    password = "MyVeryGood123987Password##$$@@!!"

    assert UserValidator.validate_password(password)


def test_validate_password_negative():
    password_empty, password_big = "", "a" * 256

    with pytest.raises(ValueError) as info_for_empty:
        UserValidator.validate_password(password_empty)

    with pytest.raises(ValueError) as info_for_big:
        UserValidator.validate_password(password_big)

    assert (
        info_for_empty.value.args[0]
        == info_for_big.value.args[0]
        == "Password doesn't has length less 8 and more 255 symbols."
    )
