import io
import os

import pytest
from PIL import Image
from django.core.files.uploadedfile import SimpleUploadedFile


@pytest.fixture
def image_file_factory():
    def create_image(
        width=100,
        height=100,
        image_format="PNG",
        mode="RGB",
        min_size_bytes=None,
    ):
        if min_size_bytes is None:
            image = Image.new(mode, (width, height))
            buffer = io.BytesIO()
            image.save(buffer, format=image_format)

        else:
            channels = len(mode)

            while True:
                image = Image.frombytes(
                    mode,
                    (width, height),
                    os.urandom(width * height * channels),
                )

                buffer = io.BytesIO()
                image.save(buffer, format=image_format)

                if buffer.tell() > min_size_bytes:
                    break

                width = int(width * 1.5)
                height = int(height * 1.5)

        extension = "jpg" if image_format == "JPEG" else "png"
        content_type = (
            "image/jpeg" if image_format == "JPEG" else "image/png"
        )

        return SimpleUploadedFile(
            f"photo.{extension}",
            buffer.getvalue(),
            content_type=content_type,
        )

    return create_image