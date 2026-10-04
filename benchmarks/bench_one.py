"""Benchmark one implementation's encoder or decoder and print a JSON line.

Usage: bench_one.py {fast-thumbhash-rs,thumbhash-rs,thumbhash,thumbhash-python} [encode|decode]

`thumbhash` has no decoder.

`fast-thumbhash-rs`, `thumbhash-rs`, `thumbhash` and `thumbhash-python` all import as `thumbhash`, so each
implementation must run in its own environment (see run.py).
"""

import json
import random
import statistics
import sys
import time

WIDTH = HEIGHT = 100  # the maximum size ThumbHash supports
TARGET_SECONDS = 1.0
MIN_RUNS = 5


def make_rgba(width, height):
    """Deterministic, opaque, noisy gradient, so the image isn't trivial."""
    rng = random.Random(0)
    pixels = bytearray()
    for y in range(height):
        for x in range(width):
            pixels += bytes(
                (
                    (x * 255 // width + rng.randrange(40)) % 256,
                    (y * 255 // height + rng.randrange(40)) % 256,
                    ((x + y) * 255 // (width + height) + rng.randrange(40)) % 256,
                    255,
                )
            )
    return bytes(pixels)


def load(impl):
    """Return (encode, decode or None, rgba input in the form the library expects)."""
    rgba = make_rgba(WIDTH, HEIGHT)
    if impl in ("fast-thumbhash-rs", "thumbhash-rs"):
        from thumbhash import rgba_to_thumb_hash, thumb_hash_to_rgba

        return rgba_to_thumb_hash, thumb_hash_to_rgba, rgba
    if impl == "thumbhash":
        from thumbhash import rgba_to_thumb_hash

        return rgba_to_thumb_hash, None, list(rgba)
    if impl == "thumbhash-python":
        from thumbhash.decode import thumbhash_to_rgba
        from thumbhash.encode import rgba_to_thumbhash

        return rgba_to_thumbhash, thumbhash_to_rgba, list(rgba)
    raise SystemExit(f"unknown implementation: {impl}")


def measure(call):
    """Time `call()`: returns (median ms, min ms, runs)."""
    call()  # warm-up
    start = time.perf_counter()
    call()
    estimate = time.perf_counter() - start
    runs = max(MIN_RUNS, int(TARGET_SECONDS / max(estimate, 1e-9)))

    timings = []
    for _ in range(runs):
        start = time.perf_counter()
        call()
        timings.append((time.perf_counter() - start) * 1000)
    return statistics.median(timings), min(timings), runs


def main(impl, op):
    encode, decode, rgba = load(impl)
    thash = bytes(encode(WIDTH, HEIGHT, rgba))

    if op == "encode":
        call = lambda: encode(WIDTH, HEIGHT, rgba)  # noqa: E731
        output = thash.hex()
    elif decode is None:
        raise SystemExit(f"{impl} has no decoder")
    else:
        call = lambda: decode(thash)  # noqa: E731
        width, height, pixels = decode(thash)
        output = {"size": [width, height], "rgba": bytes(pixels).hex()}

    median, minimum, runs = measure(call)
    print(
        json.dumps(
            {
                "impl": impl,
                "op": op,
                "runs": runs,
                "median_ms": median,
                "min_ms": minimum,
                "output": output,
            }
        )
    )


if __name__ == "__main__":
    if len(sys.argv) not in (2, 3):
        raise SystemExit(__doc__)
    main(sys.argv[1], sys.argv[2] if len(sys.argv) == 3 else "encode")
