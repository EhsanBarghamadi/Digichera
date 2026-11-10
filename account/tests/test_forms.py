import pytest

from django.core.files.uploadedfile import SimpleUploadedFile
from account.forms import ProfileForm
from user.tests.factories import CustomUserFactory

pytestmark = pytest.mark.django_db


def test_profile_form_valid_data(valid_profile_form_context):
    user, data = valid_profile_form_context

    form = ProfileForm(data=data, instance=user.profile)

    assert form.is_valid() is True


def test_profile_form_requires_postal_code(valid_profile_form_context):
    user, data = valid_profile_form_context
    data.pop("postal_code")

    form = ProfileForm(data=data, instance=user.profile)

    assert form.is_valid() is False
    assert "postal_code" in form.errors


def test_profile_form_allows_optional_fields_to_be_empty(valid_profile_form_context):
    user, data = valid_profile_form_context
    data.pop("location")

    form = ProfileForm(data=data, instance=user.profile)

    assert form.is_valid() is True


@pytest.mark.parametrize(
    "postal_code_value",
    ["161961413", "16196146163", "16196ABCDE", "1111111111"],
    ids=[
        "short_postal_code",
        "long_postal_code",
        "non_numeric_postal_code",
        "invalid_postal_code_format",
    ],
)
def test_profile_form_rejects_invalid_postal_code(postal_code_value):
    user = CustomUserFactory()
    data = {"postal_code": postal_code_value}
    form = ProfileForm(data=data, instance=user.profile)

    assert form.is_valid() is False
    assert "postal_code" in form.errors


def test_profile_form_rejects_non_image_file():
    fake_image = SimpleUploadedFile(
        name="fake.jpg", content=b"This is test text.", content_type="text/plain"
    )
    user = CustomUserFactory()
    data = {"postal_code": "1619614153"}
    file = {"avatar": fake_image}
    form = ProfileForm(data=data, files=file, instance=user.profile)

    assert form.is_valid() is False
    assert "avatar" in form.errors


def test_profile_form_rejects_avatar_over_max_size(image_file_factory):
    image = image_file_factory(min_size_bytes=2 * 1024 * 1024)
    assert image.size > 2 * 1024 * 1024

    user = CustomUserFactory()
    data = {"postal_code": "1619614153"}
    file = {"avatar": image}
    form = ProfileForm(data=data, files=file, instance=user.profile)

    assert form.is_valid() is False
    assert "avatar" in form.errors


def test_profile_form_accepts_avatar_within_max_size(image_file_factory):
    image = image_file_factory(min_size_bytes=1 * 1024 * 1024)
    user = CustomUserFactory()
    data = {"postal_code": "1619614153"}
    file = {"avatar": image}
    form = ProfileForm(data=data, files=file, instance=user.profile)

    assert image.size < 2 * 1024 * 1024
    assert form.is_valid() is True
    assert "avatar" not in form.errors
