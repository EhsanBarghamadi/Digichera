import pytest

from django.core.files.uploadedfile import SimpleUploadedFile
from account.forms import ProfileForm
from user.tests.factories import CustomUserFactory


@pytest.mark.django_db
def test_profile_form_valid_data():
    user = CustomUserFactory()
    data = {
        "postal_code": "1619614153",
        "location": "تهران، خیابان پاسداران، کوچه شهید یزدانی، پلاک ۱۲، طبقه سوم",
    }
    form = ProfileForm(data=data, instance=user.profile)

    assert form.is_valid() is True


@pytest.mark.django_db
def test_profile_form_requires_postal_code():
    user = CustomUserFactory()
    data = {"location": "تهران، خیابان پاسداران، کوچه شهید یزدانی، پلاک ۱۲، طبقه سوم"}
    form = ProfileForm(data=data, instance=user.profile)

    assert form.is_valid() is False
    assert "postal_code" in form.errors


@pytest.mark.django_db
def test_profile_form_allows_optional_fields_to_be_empty():
    user = CustomUserFactory()
    data = {"postal_code": "1619614153"}
    form = ProfileForm(data=data, instance=user.profile)

    assert form.is_valid() is True


@pytest.mark.django_db
def test_profile_form_rejects_short_postal_code():
    user = CustomUserFactory()
    data = {"postal_code": "161961413"}
    form = ProfileForm(data=data, instance=user.profile)

    assert form.is_valid() is False
    assert "postal_code" in form.errors


@pytest.mark.django_db
def test_profile_form_rejects_long_postal_code():
    user = CustomUserFactory()
    data = {"postal_code": "16196146163"}
    form = ProfileForm(data=data, instance=user.profile)

    assert form.is_valid() is False
    assert "postal_code" in form.errors


@pytest.mark.django_db
def test_profile_form_rejects_non_numeric_postal_code():
    user = CustomUserFactory()
    data = {"postal_code": "16196ABCDE"}
    form = ProfileForm(data=data, instance=user.profile)

    assert form.is_valid() is False
    assert "postal_code" in form.errors


@pytest.mark.django_db
def test_profile_form_rejects_invalid_postal_code_format():
    user = CustomUserFactory()
    data = {"postal_code": "1111111111"}
    form = ProfileForm(data=data, instance=user.profile)

    assert form.is_valid() is False
    assert "postal_code" in form.errors


@pytest.mark.django_db
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


@pytest.mark.django_db
def test_profile_form_rejects_avatar_over_max_size(image_file_factory):
    image = image_file_factory(min_size_bytes=2 * 1024 * 1024)
    user = CustomUserFactory()
    data = {"postal_code": "1619614153"}
    file = {"avatar": image}
    form = ProfileForm(data=data, files=file, instance=user.profile)

    assert form.is_valid() is False
    assert "avatar" in form.errors


@pytest.mark.django_db
def test_profile_form_accepts_avatar_within_max_size(image_file_factory):
    image = image_file_factory(min_size_bytes=1 * 1024 * 1024)
    user = CustomUserFactory()
    data = {"postal_code": "1619614153"}
    file = {"avatar": image}
    form = ProfileForm(data=data, files=file, instance=user.profile)

    assert image.size < 2 * 1024 * 1024
    assert form.is_valid() is True
    assert "avatar" not in form.errors
