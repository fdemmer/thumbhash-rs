# fast-thumbhash-rs

[![Test](https://github.com/fdemmer/thumbhash-rs/actions/workflows/test.yml/badge.svg?branch=main)](https://github.com/fdemmer/thumbhash-rs/actions/workflows/test.yml)
[![PyPI](https://img.shields.io/pypi/v/fast-thumbhash-rs.svg)](https://pypi.org/project/fast-thumbhash-rs/)

A fast Python package for [ThumbHash](https://evanw.github.io/thumbhash/) image encoding/decoding using Rust bindings (PyO3, maturin) to the [`fast-thumbhash`](https://github.com/VectorPrivacy/fast-thumbhash) crate.

> [!NOTE]
> `fast-thumbhash` output is perceptually identical to the reference ThumbHash implementation, but not guaranteed to be bit-identical: the hash bytes may differ slightly from those of other implementations.

> [!NOTE]
> This is a fork of [sitatec/fast_python_thumbhash](https://github.com/sitatec/fast_python_thumbhash) (originally named `fast_thumbhash`), renamed to `fast-thumbhash-rs` and imported as `thumbhash`.

> [!WARNING]
> `fast-thumbhash-rs` provides the same `thumbhash` module and API as `thumbhash-rs`, so it is a drop-in replacement. The two packages install into the same directory and cannot be installed side by side: `pip uninstall thumbhash-rs` before installing this one.

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

## Installation

```sh
pip install fast-thumbhash-rs
```

With Pillow support (for `image_to_thumb_hash`):

```sh
pip install "fast-thumbhash-rs[pillow]"
```

## API

Each function has a docstring (`help(thumbhash.rgba_to_thumb_hash)`), also available as editor hints through the bundled type stubs.

- `rgba_to_thumb_hash(width, height, rgba)`: encode raw RGBA pixels (at most 100x100) to a ThumbHash (`bytes`).
- `thumb_hash_to_rgba(hash)`: decode a ThumbHash to `(width, height, rgba)`.
- `thumb_hash_to_average_rgba(hash)`: the average color as `(r, g, b, a)`, each from 0 to 1.
- `thumb_hash_to_approximate_aspect_ratio(hash)`: the approximate width / height of the original image.
- `image_to_thumb_hash(fp)`: open an image file with Pillow and encode it (requires the `[pillow]` extra).

## Benchmark

Compared with [`thumbhash-rs`](https://pypi.org/project/thumbhash-rs/) (the original Rust bindings) and the pure-Python packages [`thumbhash`](https://github.com/justinforlenza/thumbhash-py) (encoding only) and [`thumbhash-python`](https://github.com/Astropilot/thumbhash-python). All packages are the releases from PyPI. Run it yourself with `just bench` (see `benchmarks/`). Output on an AMD Ryzen 7 5700X, Python 3.14, release build:

```
rgba_to_thumb_hash, 100x100 RGBA image -> ThumbHash

implementation                    median ms    min ms    runs   speedup
fast-thumbhash-rs                     0.034     0.034   28404          
thumbhash-rs                          1.121     1.119     888     32.5x
thumbhash                            28.888    28.259      33    837.9x
thumbhash-python                     29.758    29.440      33    863.2x
all implementations produced the same output

thumb_hash_to_rgba, ThumbHash -> 32x32 RGBA image

implementation                    median ms    min ms    runs   speedup
fast-thumbhash-rs                     0.006     0.005  166057          
thumbhash-rs                          0.048     0.047   20798      8.6x
thumbhash-python                      5.555     5.512     180   1006.2x
all implementations produced the same output (within +-1 per channel)

speedup = how much faster fast-thumbhash-rs is than that implementation (median)
```

## Other Python packages

Pure-Python implementations of ThumbHash:
- [`thumbhash`](https://github.com/justinforlenza/thumbhash-py) ([PyPI](https://pypi.org/project/thumbhash/))
- [`thumbhash-python`](https://github.com/Astropilot/thumbhash-python) ([PyPI](https://pypi.org/project/thumbhash-python/))

## License

MIT
