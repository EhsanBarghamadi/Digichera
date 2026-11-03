import io

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
    ):
        image = Image.new(mode, (width, height))
        buffer = io.BytesIO()
        image.save(buffer, format=image_format)

        extension = "jpg" if image_format == "JPEG" else "png"

        return SimpleUploadedFile(
            f"photo.{extension}",
            buffer.getvalue(),
            content_type=f"image/{extension}",
        )

    return create_image
