# CROVIA – `merkle_payouts.v1`

This note defines the **`merkle_payouts.v1`** JSON profile.

A `merkle_payouts.v1` document describes a **Merkle root** computed over
a `payouts.v1` NDJSON file (one JSON per provider-level payout).

---

## 1. Canonical leaf definition

For this profile, each **leaf** of the Merkle tree is:

- the **SHA-256 hash** of one **raw NDJSON line** from a `payouts.v1` file,
- with bytes taken **exactly as stored** in the file (no reformatting).

Formally, for a payouts file `F`:

- Iterate over each non-empty line `L` in `F` (in file order),
- Strip trailing `\r` and `\n`,
- Compute `leaf_hash = SHA256(L_bytes)`,
- Append `leaf_hash` to the leaf list.

The **ordering** of leaves is the file order of `F`.

If the number of leaves is odd at any Merkle level, the last leaf is **duplicated**
(`[h0, h1, h2] → [H(h0‖h1), H(h2‖h2)]`).

The Merkle root is the single hash obtained at the top level, as a hex string.

---

## 2. `merkle_payouts.v1` JSON shape

Example:

{
  "schema": "merkle_payouts.v1",
  "algo": "merkle_sha256_leaf_ndjson_v1",
  "created_at": "2025-11-24T19:30:00Z",
  "target": {
    "path": "demo_dpi_2025-11/output/dpi_payouts_2025-11.ndjson",
    "schema": "payouts.v1",
    "sha256": "…",
    "leaf_encoding": "raw_ndjson_line",
    "leaf_count": 3717
  },
  "root": "…"
}

---

Future extensions (v1.1+) may add:

- per-provider proof files (`merkle_proof.v1`)
- additional algorithms (algo variants)
- compression hints

`merkle_payouts.v1` is designed to be:

- small (a few hundred bytes)
- stable (fully determined by the payouts file)
- offline-verifiable with ~100 lines of code in any language.

