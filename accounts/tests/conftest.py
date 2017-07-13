import pytest


@pytest.fixture
def signup_data():
    """
    Return valid signup data
    """
    return {
        'name': 'User',
        'email': 'user@mail.com',
        'password': 'userpass',
        'password_confirm': 'userpass',
    }
