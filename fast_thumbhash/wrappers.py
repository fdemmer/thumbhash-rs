from __future__ import annotations

from pathlib import Path

from .fast_thumbhash import rgba_to_thumb_hash


def image_to_thumb_hash(fp: str | bytes | Path) -> bytes:
    """Opens an image file with Pillow and encodes it to a ThumbHash.

    The image is converted to RGBA, shrunk to fit within 100x100 pixels (the
    maximum size ThumbHash supports) and rotated according to its EXIF
    orientation before encoding.

    Requires Pillow, install it with the ``pillow`` extra:
    ``pip install "fast-thumbhash[pillow]"``.

    :param fp: The path of the image file, or any argument accepted by
        :func:`PIL.Image.open`.
    :returns: The ThumbHash.
    :raises ImportError: If Pillow is not installed.
    """
    try:
        from PIL import Image, ImageOps
    except ImportError:
        raise ImportError(
            "Pillow not installed, please re-install with the [pillow] extra"
        ) from None

    img = Image.open(fp)
    img = img.convert("RGBA")
    img.thumbnail((100, 100))
    img = ImageOps.exif_transpose(img)

    return rgba_to_thumb_hash(img.width, img.height, img.tobytes())