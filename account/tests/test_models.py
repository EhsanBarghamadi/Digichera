import os

import pytest
from PIL import Image

pytestmark = pytest.mark.django_db


def test_profile_avatar_resizes_large_image(image_file_factory, profile):
    file = image_file_factory(width=1000, height=800)
    profile.avatar = file
    profile.save()

    with Image.open(profile.avatar.path) as image:
        assert image.width == 300
        assert image.height == 240


def test_profile_avatar_is_saved_as_jpeg(image_file_factory, profile):
    file = image_file_factory(width=1000, height=800, image_format="PNG")
    profile.avatar = file
    profile.save()

    with Image.open(profile.avatar.path) as image:
        assert image.format == "JPEG"


def test_profile_avatar_converts_rgba_to_rgb(image_file_factory, profile):
    file = image_file_factory(width=1000, height=800, image_format="PNG", mode="RGBA")
    profile.avatar = file
    profile.save()

    with Image.open(profile.avatar.path) as image:
        assert image.mode == "RGB"


def test_profile_avatar_does_not_enlarge_small_image(image_file_factory, profile):
    file = image_file_factory(width=100, height=100)
    profile.avatar = file
    profile.save()

    with Image.open(profile.avatar.path) as image:
        assert image.width == 100
        assert image.height == 100


def test_profile_save_does_not_reprocess_unchanged_avatar(image_file_factory, profile):
    file = image_file_factory(width=100, height=100)
    profile.avatar = file
    profile.save()
    image_name = profile.avatar.name

    profile.location = "This is test for location."
    profile.save()

    assert profile.avatar.name == image_name


def test_profile_save_reprocesses_replaced_avatar(image_file_factory, profile):
    file_1 = image_file_factory(width=100, height=100)
    profile.avatar = file_1
    profile.save()

    old_name = profile.avatar.name

    file = image_file_factory(width=300, height=300)
    profile.avatar = file
    profile.save()

    with Image.open(profile.avatar.path) as image:
        assert profile.avatar.name != old_name
        assert image.format == "JPEG"


def test_profile_save_without_avatar(profile):
    profile.save()

    assert not profile.avatar


@pytest.mark.xfail(strict=True, reason="JPEG image content must have .jpg extension")
def test_profile_avatar_extension_matches_jpeg_content(image_file_factory, profile):
    file = image_file_factory(width=100, height=100, image_format="PNG")
    profile.avatar = file
    profile.save()

    assert os.path.splitext(profile.avatar.name)[1] == ".jpg"
