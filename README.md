# fast_thumbhash
[![Release](https://github.com/sitatec/fast_python_thumbhash/actions/workflows/release.yml/badge.svg?branch=main)](https://github.com/sitatec/fast_python_thumbhash/actions/workflows/release.yml)

> [!WARNING]
> This package is not related to [VectorPrivacy/fast-thumbhash](https://github.com/VectorPrivacy/fast-thumbhash), which is a different project. Don't confuse the two.

A fast Python package for [ThumbHash](https://evanw.github.io/thumbhash/) image encoding/decoding using Rust bindings (PyO3, maturin) to the official `thumbhash` crate.

fast_thumbhash is 60.5x faster than the pure Python implementations I tested:

```
28.13854099076707 ms (thumbhash)
0.46491601096931845 ms (fast-thumbhash - this package)
```

[`thumbhash-python`](https://github.com/Astropilot/thumbhash-python) was also taking the same time range as [`thumbhash`](https://github.com/justinforlenza/thumbhash-py) (27 - 35 ms).

## Features
- Exposes `rgba_to_thumb_hash`, `thumb_hash_to_rgba`, `thumb_hash_to_average_rgba`, `thumb_hash_to_approximate_aspect_ratio`.
- Works on raw RGBA bytes with no dependencies.
- `image_to_thumb_hash` wrapper: opens an image file with Pillow (as a `PIL.Image`, converted to RGBA, resized and EXIF-rotated) and encodes it. Pillow is optional, install it with the `[pillow]` extra.

## Installation

```sh
pip install fast-thumbhash
```

With Pillow support (for `image_to_thumb_hash`):

```sh
pip install "fast-thumbhash[pillow]"
```

## Usage Example
`image_to_thumb_hash` needs the `[pillow]` extra (see Installation).

```python
from PIL import Image
from fast_thumbhash import image_to_thumb_hash, thumb_hash_to_rgba

thash = image_to_thumb_hash("example.jpg")
width, height, rgba = thumb_hash_to_rgba(thash)
restored = Image.frombytes("RGBA", (width, height), rgba)
restored.save("restored.png")
```

## Other Python packages
Pure-Python implementations of ThumbHash:
- [`thumbhash`](https://github.com/justinforlenza/thumbhash-py) ([PyPI](https://pypi.org/project/thumbhash/))
- [`thumbhash-python`](https://github.com/Astropilot/thumbhash-python) ([PyPI](https://pypi.org/project/thumbhash-python/))

## License
MIT
