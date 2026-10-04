# CLAUDE.md

`fast_thumbhash` is a Python package with a Rust (PyO3) extension, built with maturin. It wraps the `thumbhash` crate.

## Layout
- `src/lib.rs`: PyO3 module with four functions: `rgba_to_thumb_hash`, `thumb_hash_to_rgba`, `thumb_hash_to_average_rgba` and `thumb_hash_to_approximate_aspect_ratio`. They take and return `bytes`. `rgba_to_thumb_hash` validates its input and raises `ValueError`.
- `fast_thumbhash/__init__.py`: re-exports the compiled module (`.fast_thumbhash`) and `.wrappers`.
- `fast_thumbhash/wrappers.py`: `image_to_thumb_hash(fp)`, pure Python, needs the optional Pillow extra (imported lazily).
- `fast_thumbhash/fast_thumbhash.pyi` and `py.typed`: hand-written type stub for the compiled module, and the PEP 561 marker.
- `tests/test_lib.py`: pytest tests for the extension and the README example.
- `pyproject.toml`: maturin build backend with `python-source = "."`, the cibuildwheel config (cp38–cp314, no musllinux) and the pyright config.
- `.python-version`: Python 3.14, the newest version supported by the pinned `pyo3 0.29`.
- `.pre-commit-config.yaml`: `cargo fmt` hook, run with `prek`.
- `LICENSE` and `THIRD_PARTY_LICENSES.md`: MIT, plus the notices for the statically linked Rust crates. Both ship in wheels.
- `.github/workflows/release.yml`: builds wheels and an sdist, then publishes to PyPI on a release. There is no CI for push or pull requests.

## Commands (see `Justfile`)
- `just setup`: recreate `.venv/` with uv and install maturin, pytest, pillow and pyright.
- `just build` / `just build-release`: `maturin develop` into the venv.
- `just shell`: rebuild, then open a Python shell with the package installed from source.
- `just test`: rebuild, then run pytest.
- `just bench`: build a release wheel and benchmark encoding (vs `thumbhash`, `thumbhash-python`) and decoding (vs `thumbhash-python`) in `benchmarks/`, each in its own uv environment because both packages import as `thumbhash`.
- `just check`: `cargo check` and clippy. Clippy currently fails on the redundant `use thumbhash;` in `src/lib.rs`.
- `just typecheck`: pyright on `fast_thumbhash/`.
- `just wheel` / `just sdist`: build distributable artifacts into `dist/`.

## Conventions
- Docstrings are reStructuredText (`:param:`, `:returns:`, `:raises:`). The Rust `///` comments (exposed as `__doc__`, shown by `help()`) and the `.pyi` docstrings (shown by editors) must say the same thing. Update both together.
- When a function's signature or return type changes in `src/lib.rs`, update the `.pyi` stub as well.
- Commit messages are plain imperative sentences ("Add intial tests"), not Conventional Commits prefixes.

## Notes
- `cargo test` is not used. The `extension-module` feature breaks linking of Rust test binaries.
- The Rust crate version (`Cargo.toml`) and the Python version (`pyproject.toml`) are tracked separately.
- Ignored by git: `.venv/`, `target/`, the built `.so` in `fast_thumbhash/`, `uv.lock`, and image files in the repo root (`example.jpg`, `restored.png`).
