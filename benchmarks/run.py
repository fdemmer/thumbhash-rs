"""Compare fast_thumbhash with the pure-Python ThumbHash packages.

Run with `just bench`, which builds a release wheel of this package first.
Each implementation runs in its own isolated uv environment, because
`thumbhash` and `thumbhash-python` both install a top-level `thumbhash` package.
"""

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WHEEL_DIR = ROOT / "target" / "bench-wheels"

LABELS = {
    "fast": "fast-thumbhash (this package)",
    "thumbhash": "thumbhash",
    "thumbhash-python": "thumbhash-python",
}
# `thumbhash` only has an encoder.
IMPLEMENTATIONS = {
    "encode": ["fast", "thumbhash", "thumbhash-python"],
    "decode": ["fast", "thumbhash-python"],
}
TITLES = {
    "encode": "rgba_to_thumb_hash, 100x100 RGBA image -> ThumbHash",
    "decode": "thumb_hash_to_rgba, ThumbHash -> 32x32 RGBA image",
}
# The decoders compute in different float precisions, so allow +-1 per channel.
DECODE_TOLERANCE = 1


def newest_wheel():
    wheels = sorted(WHEEL_DIR.glob("fast_thumbhash-*.whl"), key=lambda p: p.stat().st_mtime)
    if not wheels:
        raise SystemExit(f"no wheel in {WHEEL_DIR}, run `just bench`")
    return wheels[-1]


def run_one(impl, op):
    print(f"running {op} / {impl} ...", file=sys.stderr, flush=True)
    requirement = str(newest_wheel()) if impl == "fast" else impl
    cmd = [
        "uv", "run", "--no-project", "--isolated", "--quiet",
        "--with", requirement,
        "python", "benchmarks/bench_one.py", impl, op,
    ]  # fmt: skip
    out = subprocess.run(cmd, cwd=ROOT, check=True, capture_output=True, text=True)
    return json.loads(out.stdout.strip().splitlines()[-1])


def outputs_match(op, results):
    """Return a description of any difference between the implementations' outputs."""
    outputs = {impl: r["output"] for impl, r in results.items()}
    if op == "encode":
        if len({*outputs.values()}) == 1:
            return None
        return "different hashes:\n" + "\n".join(f"  {i}: {o}" for i, o in outputs.items())

    sizes = {tuple(o["size"]) for o in outputs.values()}
    if len(sizes) != 1:
        return f"different image sizes: {sizes}"
    pixels = [bytes.fromhex(o["rgba"]) for o in outputs.values()]
    worst = max(abs(a - b) for a, b in zip(*pixels))
    if len({len(p) for p in pixels}) != 1 or worst > DECODE_TOLERANCE:
        return f"pixels differ by up to {worst}"
    return None


def report(op):
    results = {impl: run_one(impl, op) for impl in IMPLEMENTATIONS[op]}
    fast = results["fast"]

    print(f"\n{TITLES[op]}\n")
    print(f"{'implementation':<32}{'median ms':>11}{'min ms':>10}{'runs':>8}{'speedup':>10}")
    for impl, r in results.items():
        speedup = "" if impl == "fast" else f"{r['median_ms'] / fast['median_ms']:.1f}x"
        print(
            f"{LABELS[impl]:<32}{r['median_ms']:>11.3f}{r['min_ms']:>10.3f}"
            f"{r['runs']:>8}{speedup:>10}"
        )

    problem = outputs_match(op, results)
    if problem:
        print(f"WARNING: {op} outputs differ, the comparison is not valid: {problem}")
        return False
    detail = "" if op == "encode" else f" (within +-{DECODE_TOLERANCE} per channel)"
    print(f"all implementations produced the same output{detail}")
    return True


def main():
    ok = [report(op) for op in IMPLEMENTATIONS]
    print("\nspeedup = how much faster fast-thumbhash is than that implementation (median)")
    sys.exit(0 if all(ok) else 1)


if __name__ == "__main__":
    main()
