import pytest

from auth import authenticate_user


@pytest.mark.parametrize("username,password", [("", "pass"), ("user", ""), ("", "")])
def test_missing_credentials(username, password):
    assert authenticate_user(username, password, {}) == "Missing credentials"


def test_user_not_found():
    assert authenticate_user("user", "pass", {}) == "User not found"


def test_account_locked():
    db = {"user": {"password": "pass", "attempts": 3}}
    assert authenticate_user("user", "pass", db) == "Account locked"
    assert db["user"]["attempts"] == 3


def test_invalid_password():
    db = {"user": {"password": "pass", "attempts": 2}}
    assert authenticate_user("user", "wrong", db) == "Invalid password"
    assert db["user"]["attempts"] == 3
    assert authenticate_user("user", "pass", db) == "Account locked"


def test_implicit_attempt_count():
    db = {"user": {"password": "pass"}}
    assert authenticate_user("user", "wrong", db) == "Invalid password"
    assert db["user"]["attempts"] == 1


def test_success():
    db = {"user": {"password": "pass", "attempts": 1}}
    assert authenticate_user("user", "pass", db) == "Authenticated"
    assert db["user"]["attempts"] == 0
