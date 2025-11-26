#!/usr/bin/env python3
import hashlib
import json
from datetime import datetime
from pathlib import Path

PAYOUTS_PATH = Path("demo_dpi_2025-11/output/dpi_payouts_2025-11.ndjson")
OUT_PATH = Path("demo_dpi_2025-11/output/dpi_merkle_payouts_2025-11.json")

def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            if not chunk:
                break
            h.update(chunk)
    return h.hexdigest()

def compute_merkle_root_from_ndjson(path: Path) -> tuple[str, int]:
    leaves = []

    with path.open("rb") as f:
        for raw in f:
            # skip empty lines
            if raw.strip() == b"":
                continue
            line = raw.rstrip(b"\r\n")
            leaf_hash = hashlib.sha256(line).digest()
            leaves.append(leaf_hash)

    if not leaves:
        raise ValueError("No non-empty lines found in payouts NDJSON")

    leaf_count = len(leaves)

    level = 0
    while len(leaves) > 1:
        next_level = []
        it = iter(leaves)
        for left in it:
            try:
                right = next(it)
            except StopIteration:
                # duplicate last if odd
                right = left
            h = hashlib.sha256(left + right).digest()
            next_level.append(h)
        leaves = next_level
        level += 1

    root_hex = leaves[0].hex()
    return root_hex, leaf_count

def main():
    if not PAYOUTS_PATH.exists():
        raise SystemExit(f"Missing payouts file: {PAYOUTS_PATH}")

    print(f"[MERKLE] Reading payouts NDJSON: {PAYOUTS_PATH}")
    file_hash = sha256_file(PAYOUTS_PATH)
    root_hex, leaf_count = compute_merkle_root_from_ndjson(PAYOUTS_PATH)

    out = {
        "schema": "merkle_payouts.v1",
        "algo": "merkle_sha256_leaf_ndjson_v1",
        "created_at": datetime.utcnow().isoformat() + "Z",
        "target": {
            "path": str(PAYOUTS_PATH),
            "schema": "payouts.v1",
            "sha256": file_hash,
            "leaf_encoding": "raw_ndjson_line",
            "leaf_count": leaf_count,
        },
        "root": root_hex,
    }

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(json.dumps(out, indent=2))
    print(f"[MERKLE] root={root_hex}  leaves={leaf_count}")
    print(f"[MERKLE] written {OUT_PATH}")

if __name__ == "__main__":
    main()
