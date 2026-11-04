import pytest
import os

from PIL import Image
from user.tests.factories import CustomUserFactory
from account.models import Profile


@pytest.mark.django_db
def test_profile_avatar_resizes_large_image(image_file_factory):
    file = image_file_factory(width=1000, height=800)
    user = CustomUserFactory()
    profile = user.profile
    profile.avatar = file
    profile.save()

    image = Image.open(profile.avatar.path)

    assert image.width <= 300 and image.height <= 300


@pytest.mark.django_db
def test_profile_avatar_is_saved_as_jpeg(image_file_factory):
    file = image_file_factory(width=1000, height=800, image_format="PNG")
    user = CustomUserFactory()
    profile = user.profile
    profile.avatar = file
    profile.save()

    image = Image.open(profile.avatar.path)

    assert image.format == "JPEG"


@pytest.mark.django_db
def test_profile_avatar_converts_rgba_to_rgb(image_file_factory):
    file = image_file_factory(width=1000, height=800, image_format="PNG", mode="RGBA")
    user = CustomUserFactory()
    profile = user.profile
    profile.avatar = file
    profile.save()

    image = Image.open(profile.avatar.path)

    assert image.mode == "RGB"


@pytest.mark.django_db
def test_profile_avatar_does_not_enlarge_small_image(image_file_factory):
    file = image_file_factory(width=100, height=100)
    user = CustomUserFactory()
    profile = user.profile
    profile.avatar = file
    profile.save()

    image = Image.open(profile.avatar.path)

    assert image.width == 100
    assert image.height == 100


@pytest.mark.django_db
def test_profile_save_does_not_reprocess_unchanged_avatar(image_file_factory):
    file = image_file_factory(width=100, height=100)
    user = CustomUserFactory()
    profile = user.profile
    profile.avatar = file
    profile.save()
    image_name = profile.avatar.name

    profile.location = "This is test for location."
    profile.save()

    assert profile.avatar.name == image_name


@pytest.mark.django_db
def test_profile_save_reprocesses_replaced_avatar(image_file_factory):
    file_1 = image_file_factory(width=100, height=100)
    user = CustomUserFactory()
    profile = user.profile
    profile.avatar = file_1
    profile.save()

    old_name = profile.avatar.name

    file = image_file_factory(width=300, height=300)
    profile.avatar = file
    profile.save()

    image_2 = Image.open(profile.avatar.path)

    assert profile.avatar.name != old_name
    assert image_2.format == "JPEG"


@pytest.mark.django_db
def test_profile_save_without_avatar():
    user = CustomUserFactory()
    profile = user.profile
    profile.save()

    assert not profile.avatar

@pytest.mark.django_db
def test_profile_avatar_preserves_original_extension(image_file_factory):
    file = image_file_factory(width=100, height=100, image_format="PNG")
    user = CustomUserFactory()
    profile = user.profile
    profile.avatar = file
    profile.save()
    image_name = profile.avatar.name
    image = Image.open(profile.avatar.path)

    assert os.path.splitext(profile.avatar.name)[1] == ".png"
    assert image.format == "JPEG"