"""Fast ThumbHash encoding and decoding, implemented in Rust.

See https://evanw.github.io/thumbhash/ for details on the ThumbHash format.
"""

from .wrappers import image_to_thumb_hash

from ._thumbhash import (
    rgba_to_thumb_hash,
    thumb_hash_to_rgba,
    thumb_hash_to_average_rgba,
    thumb_hash_to_approximate_aspect_ratio,
)

__all__ = [
    "image_to_thumb_hash",
    "rgba_to_thumb_hash",
    "thumb_hash_to_rgba",
    "thumb_hash_to_average_rgba",
    "thumb_hash_to_approximate_aspect_ratio",
]