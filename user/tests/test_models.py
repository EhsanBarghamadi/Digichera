import pytest
from django.core.exceptions import ValidationError

from user.models import phone_validator


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
