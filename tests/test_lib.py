import pytest

from fast_thumbhash import (
    image_to_thumb_hash,
    rgba_to_thumb_hash,
    thumb_hash_to_approximate_aspect_ratio,
    thumb_hash_to_average_rgba,
    thumb_hash_to_rgba,
)


def solid_rgba(width, height, color):
    return bytes(color) * (width * height)


def test_roundtrip_example(tmp_path, monkeypatch):
    """The usage example from README.md, run against a generated image."""
    Image = pytest.importorskip("PIL.Image")
    monkeypatch.chdir(tmp_path)
    Image.new("RGB", (120, 80), (10, 120, 200)).save("example.jpg")

    # --- README example ---
    thash = image_to_thumb_hash("example.jpg")
    width, height, rgba = thumb_hash_to_rgba(thash)
    restored = Image.frombytes("RGBA", (width, height), rgba)
    restored.save("restored.png")
    # ----------------------

    assert isinstance(thash, bytes)
    assert isinstance(rgba, bytes)
    assert len(rgba) == width * height * 4
    assert restored.size == (width, height)
    assert (tmp_path / "restored.png").exists()
    # solid color input: decoded pixels stay close to it (JPEG + thumbhash are lossy)
    r, g, b, a = restored.getpixel((width // 2, height // 2))
    assert abs(r - 10) < 20 and abs(g - 120) < 20 and abs(b - 200) < 20 and a == 255


def test_average_rgba():
    thash = rgba_to_thumb_hash(60, 40, solid_rgba(60, 40, (51, 153, 204, 255)))

    r, g, b, a = thumb_hash_to_average_rgba(thash)

    # components are floats in 0..1
    assert r == pytest.approx(51 / 255, abs=0.03)
    assert g == pytest.approx(153 / 255, abs=0.03)
    assert b == pytest.approx(204 / 255, abs=0.03)
    assert a == pytest.approx(1.0, abs=0.01)


def test_average_rgba_transparent():
    thash = rgba_to_thumb_hash(32, 32, solid_rgba(32, 32, (255, 0, 0, 0)))

    assert thumb_hash_to_average_rgba(thash)[3] == pytest.approx(0.0, abs=0.01)


@pytest.mark.parametrize(
    ("width", "height"), [(40, 40), (60, 40), (40, 60), (100, 25)]
)
def test_approximate_aspect_ratio(width, height):
    thash = rgba_to_thumb_hash(width, height, solid_rgba(width, height, (90, 90, 90, 255)))

    ratio = thumb_hash_to_approximate_aspect_ratio(thash)

    assert isinstance(ratio, float)
    # the hash only stores a coarse aspect ratio
    assert ratio == pytest.approx(width / height, rel=0.15)


@pytest.mark.parametrize(
    "func", [thumb_hash_to_average_rgba, thumb_hash_to_approximate_aspect_ratio]
)
def test_invalid_hash_raises_value_error(func):
    with pytest.raises(ValueError, match="thumbhash"):
        func(b"\x00")


@pytest.mark.parametrize(("width", "height"), [(101, 10), (10, 101), (200, 200)])
def test_rgba_to_thumb_hash_rejects_too_large_image(width, height):
    with pytest.raises(ValueError, match="at most 100"):
        rgba_to_thumb_hash(width, height, solid_rgba(width, height, (0, 0, 0, 255)))


@pytest.mark.parametrize("length", [0, 5, 4 * 10 * 10 - 1, 4 * 10 * 10 + 1])
def test_rgba_to_thumb_hash_rejects_wrong_rgba_length(length):
    with pytest.raises(ValueError, match="4 = 400 bytes"):
        rgba_to_thumb_hash(10, 10, bytes(length))
