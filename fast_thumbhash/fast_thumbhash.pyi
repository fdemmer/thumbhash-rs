def rgba_to_thumb_hash(width: int, height: int, rgba: bytes) -> bytes:
    """Encodes an RGBA image to a ThumbHash. RGB should not be premultiplied by A.

    :param width: The width of the input image. Must be at most 100 pixels.
    :param height: The height of the input image. Must be at most 100 pixels.
    :param rgba: The pixels of the input image, row by row, with 4 bytes (R, G, B, A)
        per pixel. Must be exactly ``width * height * 4`` bytes long.
    :returns: The ThumbHash.
    :raises ValueError: If ``width`` or ``height`` is larger than 100, or ``rgba``
        has the wrong length.
    """


def thumb_hash_to_rgba(hash: bytes) -> tuple[int, int, bytes]:
    """Decodes a ThumbHash to an RGBA image. RGB is not premultiplied by A.

    :param hash: The bytes of the ThumbHash.
    :returns: The width, height, and pixels of the rendered placeholder image, as
        ``(width, height, rgba)``. The pixels are row by row, with 4 bytes
        (R, G, B, A) per pixel.
    :raises ValueError: If the hash is invalid or malformed.
    """


def thumb_hash_to_average_rgba(hash: bytes) -> tuple[float, float, float, float]:
    """Extracts the average color from a ThumbHash. RGB is not premultiplied by A.

    :param hash: The bytes of the ThumbHash.
    :returns: The average color as ``(r, g, b, a)``. Each value ranges from 0 to 1.
    :raises ValueError: If the hash is invalid or malformed.
    """


def thumb_hash_to_approximate_aspect_ratio(hash: bytes) -> float:
    """Extracts the approximate aspect ratio of the original image.

    :param hash: The bytes of the ThumbHash.
    :returns: The approximate aspect ratio (i.e. width / height).
    :raises ValueError: If the hash is invalid or malformed.
    """
