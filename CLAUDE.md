# CLAUDE.md

`fast_thumbhash` is a Python package with a Rust (PyO3) extension, built with maturin. It wraps the `thumbhash` crate.

## Layout
- `src/lib.rs`: PyO3 module with four functions: `rgba_to_thumb_hash`, `thumb_hash_to_rgba`, `thumb_hash_to_average_rgba` and `thumb_hash_to_approximate_aspect_ratio`.
- `fast_thumbhash/__init__.py`: re-exports the compiled module (`.fast_thumbhash`) and `.wrappers`.
- `fast_thumbhash/wrappers.py`: `image_to_thumb_hash(fp)`, pure Python, needs the optional Pillow extra.
- `pyproject.toml`: maturin build backend with `python-source = "."` and the cibuildwheel config (cp310–cp312, no musllinux).
- `.github/workflows/release.yml`: builds wheels and an sdist, then publishes to PyPI on a release. There is no CI for push or pull requests.

## Commands (see `Justfile`)
- `just setup`: create `.venv/` (via uv) and install maturin, pytest and pillow.
- `just build` / `just build-release`: `maturin develop` into the venv.
- `just test`: rebuild, then run pytest. The repo has no tests yet.
- `just check`: `cargo check` and clippy.
- `just wheel` / `just sdist`: build distributable artifacts into `dist/`.

## Notes
- `cargo test` is not used. The `extension-module` feature breaks linking of Rust test binaries.
- The Rust crate version (`Cargo.toml`) and the Python version (`pyproject.toml`) are tracked separately.
