import pytest
from django.core.exceptions import ValidationError

from user.models import phone_validator, CustomUser

@pytest.mark.parametrize(
    "phone",
    [
        "09123456789",
        "09351234567",
        "09901234567",
    ],
)
def test_phone_validator_accepts_valid_numbers(phone):
    phone_validator(phone)


@pytest.mark.parametrize(
    "phone",
    [
        "0912345678",
        "091234567890",
        "9123456789",
        "0912abc6789",
        "",
        " 09123456789",
        "09123456789 ",
        "+989123456789",
        "۰۹۱۲۳۴۵۶۷۸۹",
        "09۱۲۳۴۵۶۷۸۹",
        "09123456789\n",
    ],
)
def test_phone_validator_rejects_invalid_numbers(phone):
    with pytest.raises(ValidationError, match="شماره تماس باید با فرمت صحیح وارد شود"):
        phone_validator(phone)


@pytest.mark.django_db
def test_create_user_creates_user_with_expected_fields():
    data = {
        "phone": "09123456789",
        "password": "Password123!",
        "first_name": "John",
        "last_name": "Doe",
    }

    user = CustomUser.objects.create_user(**data)

    assert user.phone == data["phone"]
    assert user.first_name == data["first_name"]
    assert user.last_name == data["last_name"]
    assert user.password != data["password"]
    assert user.check_password(data["password"])


@pytest.mark.django_db
def test_create_user_uses_default_values():
    data = {
        "phone": "09123456789",
        "password": "Password123!",
        "first_name": "John",
        "last_name": "Doe",
    }

    user = CustomUser.objects.create_user(**data)

    assert user.is_active is True
    assert user.is_staff is False
    assert user.is_superuser is False
    assert user.role == CustomUser.Roles.CUSTOMER


@pytest.mark.django_db
def test_create_user_allows_overriding_default_values():
    data = {
        "phone": "09123456789",
        "password": "Password123!",
        "first_name": "John",
        "last_name": "Doe",
        "is_staff": True,
        "is_active": False,
    }

    user = CustomUser.objects.create_user(**data)

    assert user.is_active is False
    assert user.is_staff is True


def test_create_user_raises_error_when_phone_is_empty():
    data = {
        "phone": "",
        "password": "Password123!",
        "first_name": "John",
        "last_name": "Doe",
    }

    with pytest.raises(ValueError, match="The number can not empty!"):
        CustomUser.objects.create_user(**data)


def test_create_user_raises_validation_error_for_invalid_phone():
    data = {
        "phone": "123",
        "password": "Password123!",
        "first_name": "John",
        "last_name": "Doe",
    }

    with pytest.raises(ValidationError):
        CustomUser.objects.create_user(**data)


@pytest.mark.django_db
def test_create_superuser_creates_superuser_with_required_flags():
    data = {
        "phone": "09123456789",
        "password": "Password123!",
        "first_name": "John",
        "last_name": "Doe",
    }

    user = CustomUser.objects.create_superuser(**data)

    assert user.is_active is True
    assert user.is_staff is True
    assert user.is_superuser is True
    assert user.check_password(data["password"])


@pytest.mark.parametrize(
    "key, value, message",
    [
        ("is_active", False, "Superuser must have is_active=True"),
        ("is_staff", False, "Superuser must have is_staff=True"),
        ("is_superuser", False, "Superuser must have is_superuser=True"),
    ],
)
def test_create_superuser_raises_error_when_required_flag_is_false(key, value, message):
    data = {
        "phone": "09123456789",
        "password": "Password123!",
        "first_name": "John",
        "last_name": "Doe",
        key: value,
    }

    with pytest.raises(ValueError, match=message):
        CustomUser.objects.create_superuser(**data)
