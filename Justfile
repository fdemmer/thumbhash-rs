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

# Run Python tests (rebuilds first)
test *args: build
    uv run --no-project pytest {{args}}

# Type-check the Python package
typecheck:
    uv run --no-project pyright fast_thumbhash

# Rust checks
check:
    cargo check
    cargo clippy -- -D warnings

clean:
    cargo clean
    rm -rf dist build
