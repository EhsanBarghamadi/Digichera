import pytest

from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from account.validators import validate_file_size


def test_validate_file_size_accepts_file_at_limit():
    file = SimpleUploadedFile(
        name="test.txt",
        content=b"x" * (2 * 1024 * 1024),
    )
    result = validate_file_size(file)

    assert result is None


def test_validate_file_size_rejects_file_over_limit():
    file = SimpleUploadedFile(
        name="test.txt",
        content=b"x" * (2 * 1024 * 1024 + 1),
    )

    with pytest.raises(ValidationError):
        validate_file_size(file)


def test_validate_file_size_accepts_small_file():
    file = SimpleUploadedFile(
        name="test.txt",
        content=b"x",
    )
    result = validate_file_size(file)

    assert result is None
