# CLAUDE.md

`thumbhash-rs` is a Python package (imported as `thumbhash`) with a Rust (PyO3) extension, built with maturin. It wraps the `thumbhash` crate.

## Layout
- `src/lib.rs`: PyO3 module with four functions: `rgba_to_thumb_hash`, `thumb_hash_to_rgba`, `thumb_hash_to_average_rgba` and `thumb_hash_to_approximate_aspect_ratio`. They take and return `bytes`. `rgba_to_thumb_hash` validates its input and raises `ValueError`.
- `thumbhash/__init__.py`: re-exports the compiled module (`._thumbhash`) and `.wrappers`.
- `thumbhash/wrappers.py`: `image_to_thumb_hash(fp)`, pure Python, needs the optional Pillow extra (imported lazily).
- `thumbhash/_thumbhash.pyi` and `py.typed`: hand-written type stub for the compiled module, and the PEP 561 marker.
- `tests/test_lib.py`: pytest tests for the extension and the README example.
- `pyproject.toml`: maturin build backend with `python-source = "."`, the cibuildwheel config (cp39–cp314, no musllinux; wheels are tested with pytest) and the pyright config.
- `.python-version`: Python 3.14, the newest version supported by the pinned `pyo3 0.29`.
- `.pre-commit-config.yaml`: `cargo fmt` hook, run with `prek`.
- `LICENSE` and `THIRD_PARTY_LICENSES.md`: MIT, plus the notices for the statically linked Rust crates. Both ship in wheels.
- `.github/workflows/test.yml`: on pull requests, pushes to `main` and as a reusable workflow: pytest on Linux/macOS/Windows with Python 3.9–3.14, plus `cargo fmt --check` and pyright.
- `.github/workflows/release.yml`: on a release, runs `test.yml` first, then builds wheels (cibuildwheel) and an sdist, then publishes to PyPI. Actions are pinned to commit SHAs.

## Commands (see `Justfile`)
- `just setup`: recreate `.venv/` with uv and install maturin, pytest, pillow and pyright.
- `just build` / `just build-release`: `maturin develop` into the venv.
- `just shell`: rebuild, then open a Python shell with the package installed from source.
- `just test`: rebuild, then run pytest.
- `just bench`: build a release wheel and benchmark encoding (vs `thumbhash`, `thumbhash-python`) and decoding (vs `thumbhash-python`) in `benchmarks/`, each in its own uv environment because both packages import as `thumbhash`.
- `just check`: `cargo check` and clippy. Clippy currently fails on the redundant `use thumbhash;` in `src/lib.rs`.
- `just typecheck`: pyright on `thumbhash/`.
- `just gha-update` / `just gha-check`: update and SHA-pin the GitHub Actions versions (`gha-update`), lint the workflows with zizmor.
- `just wheel` / `just sdist`: build distributable artifacts into `dist/`.

## Conventions
- Docstrings are reStructuredText (`:param:`, `:returns:`, `:raises:`). The Rust `///` comments (exposed as `__doc__`, shown by `help()`) and the `.pyi` docstrings (shown by editors) must say the same thing. Update both together.
- When a function's signature or return type changes in `src/lib.rs`, update the `.pyi` stub as well.
- Commit messages are plain imperative sentences ("Add intial tests"), not Conventional Commits prefixes.

## Notes
- `cargo test` is not used. The `extension-module` feature breaks linking of Rust test binaries.
- The Rust crate version (`Cargo.toml`) and the Python version (`pyproject.toml`) are tracked separately.
- Ignored by git: `.venv/`, `target/`, the built `.so` in `thumbhash/`, `uv.lock`, and image files in the repo root (`example.jpg`, `restored.png`).
