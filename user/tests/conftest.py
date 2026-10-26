import pytest


@pytest.fixture
def valid_registration_data():
    return {
        "phone": "09123456789",
        "password": "StrongPassword!",
        "confirm_password": "StrongPassword!",
        "first_name": "John",
        "last_name": "Doe",
        "role": "customer",
    }
