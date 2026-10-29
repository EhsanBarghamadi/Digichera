import pytest

from user.forms import CustomUserCreateForm
from user.tests.factories import CustomUserFactory

pytestmark = pytest.mark.django_db


def test_valid_registration_data_is_accepted(valid_registration_data):
    form = CustomUserCreateForm(data=valid_registration_data)

    assert form.is_valid() is True
    assert form.cleaned_data["phone"] == valid_registration_data["phone"]
    assert form.cleaned_data["first_name"] == valid_registration_data["first_name"]
    assert form.cleaned_data["last_name"] == valid_registration_data["last_name"]
    assert form.cleaned_data["role"] == valid_registration_data["role"]


@pytest.mark.parametrize("allowed_role", ["customer", "seller"])
def test_registration_accepts_allowed_roles(valid_registration_data, allowed_role):
    data = valid_registration_data.copy()
    data["role"] = allowed_role
    form = CustomUserCreateForm(data=data)

    assert form.is_valid() is True
    assert form.cleaned_data["role"] == allowed_role


@pytest.mark.parametrize("disallowed_role", ["staff", "admin"])
def test_registration_rejects_disallowed_roles(
    valid_registration_data, disallowed_role
):
    data = valid_registration_data.copy()
    data["role"] = disallowed_role
    form = CustomUserCreateForm(data=data)

    assert form.is_valid() is False
    assert "role" in form.errors


@pytest.mark.parametrize(
    "field",
    ["first_name", "last_name", "phone", "password", "confirm_password", "role"],
)
def test_registration_requires_all_fields(valid_registration_data, field):
    data = valid_registration_data.copy()
    data.pop(field)

    form = CustomUserCreateForm(data=data)

    assert form.is_valid() is False
    assert field in form.errors


def test_registration_rejects_mismatched_passwords(valid_registration_data):
    data = valid_registration_data.copy()
    data["confirm_password"] = data["password"] + "Hi"

    form = CustomUserCreateForm(data=data)

    assert form.is_valid() is False
    assert form.non_field_errors()
    assert "مطابقت ندارد" in form.non_field_errors()[0]


def test_registration_rejects_weak_password(valid_registration_data):
    data = valid_registration_data.copy()
    data["password"] = "123"
    data["confirm_password"] = data["password"]

    form = CustomUserCreateForm(data=data)

    assert form.is_valid() is False
    assert form.non_field_errors()


def test_registration_rejects_duplicate_phone(valid_registration_data):
    user = CustomUserFactory()
    data = valid_registration_data.copy()
    data["phone"] = user.phone

    form = CustomUserCreateForm(data=data)

    assert form.is_valid() is False
    assert "phone" in form.errors


@pytest.mark.parametrize(
    ("attribute", "attribute_value", "password"),
    [
        ("first_name", "Ehsan", "EhsanU47"),
        ("last_name", "Barghamadi", "BarghamadiUn47"),
    ],
)
def test_registration_rejects_password_similar_to_user_attributes(
    valid_registration_data, attribute, attribute_value, password
):
    data = valid_registration_data.copy()
    data[attribute] = attribute_value
    data["password"] = password
    data["confirm_password"] = data["password"]

    form = CustomUserCreateForm(data=data)

    assert form.is_valid() is False
    assert form.non_field_errors()
