from models import User


def test_user_password_hashing_behaves_correctly():
    user = User(username="test_user")
    password = "SecurePassword123!"

    user.set_password(password)

    assert user.password_hash != password
    assert user.check_password(password) is True
    assert user.check_password("WrongPassword") is False