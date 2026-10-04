set shell := ["bash", "-euo", "pipefail", "-c"]

default:
    @just --list

# Create venv and install dev tools
setup:
    uv venv --clear
    uv pip install maturin pytest pillow pyright

# Build the extension and install it into the venv (debug)
build:
    uv run --no-project maturin develop --uv

# Optimized build
build-release:
    uv run --no-project maturin develop --uv --release

# Build release wheel(s) into dist/
wheel:
    uv run --no-project maturin build --release --out dist

# Build sdist into dist/
sdist:
    uv run --no-project maturin sdist --out dist

# Python shell with the package built from source and installed
shell: build
    uv run --no-project python

# Run Python tests (rebuilds first)
test *args: build
    uv run --no-project pytest {{args}}

# Type-check the Python package
typecheck:
    uv run --no-project pyright thumbhash

# Benchmark encode and decode of the PyPI releases of fast-thumbhash-rs, thumbhash-rs, thumbhash and thumbhash-python
bench:
    uv run --no-project python benchmarks/run.py

# Rust checks
check:
    cargo check
    cargo clippy -- -D warnings

# Update and pin GitHub Actions versions in .github/workflows
gha-update:
    uvx gha-update

# Lint GitHub Actions workflows with zizmor
gha-check args="":
    uvx zizmor {{args}} .

clean:
    cargo clean
    rm -rf dist build
