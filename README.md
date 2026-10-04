# thumbhash-rs
[![Release](https://github.com/fdemmer/thumbhash-rs/actions/workflows/release.yml/badge.svg?branch=main)](https://github.com/fdemmer/thumbhash-rs/actions/workflows/release.yml)

> [!WARNING]
> This package is not related to [VectorPrivacy/fast-thumbhash](https://github.com/VectorPrivacy/fast-thumbhash), which is a different project. Don't confuse the two.

A fast Python package for [ThumbHash](https://evanw.github.io/thumbhash/) image encoding/decoding using Rust bindings (PyO3, maturin) to the official `thumbhash` crate.

## Benchmark
Compared with the pure-Python packages [`thumbhash`](https://github.com/justinforlenza/thumbhash-py) (encoding only) and [`thumbhash-python`](https://github.com/Astropilot/thumbhash-python). Run it yourself with `just bench` (see `benchmarks/`). Output on an AMD Ryzen 7 5700X, Python 3.14, release build:

```
rgba_to_thumb_hash, 100x100 RGBA image -> ThumbHash

implementation                    median ms    min ms    runs   speedup
thumbhash-rs (this package)           1.124     1.120     887          
thumbhash                            29.452    28.929      34     26.2x
thumbhash-python                     29.764    29.182      33     26.5x
all implementations produced the same output

thumb_hash_to_rgba, ThumbHash -> 32x32 RGBA image

implementation                    median ms    min ms    runs   speedup
thumbhash-rs (this package)           0.049     0.048   20328          
thumbhash-python                      5.543     5.519     179    113.8x
all implementations produced the same output (within +-1 per channel)

speedup = how much faster thumbhash-rs is than that implementation (median)
```

## Features
- Exposes `rgba_to_thumb_hash`, `thumb_hash_to_rgba`, `thumb_hash_to_average_rgba`, `thumb_hash_to_approximate_aspect_ratio`.
- Works on raw RGBA bytes with no dependencies.
- `image_to_thumb_hash` wrapper: opens an image file with Pillow (as a `PIL.Image`, converted to RGBA, resized and EXIF-rotated) and encodes it. Pillow is optional, install it with the `[pillow]` extra.

## Installation

```sh
pip install thumbhash-rs
```

With Pillow support (for `image_to_thumb_hash`):

```sh
pip install "thumbhash-rs[pillow]"
```

## Usage Example
`image_to_thumb_hash` needs the `[pillow]` extra (see Installation).

```python
from PIL import Image
from thumbhash import image_to_thumb_hash, thumb_hash_to_rgba

thash = image_to_thumb_hash("example.jpg")
width, height, rgba = thumb_hash_to_rgba(thash)
restored = Image.frombytes("RGBA", (width, height), rgba)
restored.save("restored.png")
```

## API
Each function has a docstring (`help(thumbhash.rgba_to_thumb_hash)`), also available as editor hints through the bundled type stubs.

- `rgba_to_thumb_hash(width, height, rgba)`: encode raw RGBA pixels (at most 100x100) to a ThumbHash (`bytes`).
- `thumb_hash_to_rgba(hash)`: decode a ThumbHash to `(width, height, rgba)`.
- `thumb_hash_to_average_rgba(hash)`: the average color as `(r, g, b, a)`, each from 0 to 1.
- `thumb_hash_to_approximate_aspect_ratio(hash)`: the approximate width / height of the original image.
- `image_to_thumb_hash(fp)`: open an image file with Pillow and encode it (requires the `[pillow]` extra).

## Other Python packages
Pure-Python implementations of ThumbHash:
- [`thumbhash`](https://github.com/justinforlenza/thumbhash-py) ([PyPI](https://pypi.org/project/thumbhash/))
- [`thumbhash-python`](https://github.com/Astropilot/thumbhash-python) ([PyPI](https://pypi.org/project/thumbhash-python/))

## License
MIT
