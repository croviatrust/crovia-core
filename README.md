# Crovia Core — DPI Demo (M0 Profile + Merkle payouts)

Open, minimal audit pack that turns AI training-data attribution logs into:

- per-provider **payouts**,
- an offline-verifiable **trust bundle**,
- an **EU AI Act–style** compliance summary,
- and a **Merkle root** over all payouts.

No tokens. No blockchain. No SaaS.  
Just NDJSON + CSV + hash-chained JSON you can verify on your own machine.

---

## 1. What this repo contains

This repo is a **frozen demo** of the CROVIA M0 profile, built on top of the  
**MIT Data Provenance Initiative** collection (real finetuning datasets, not synthetic toy examples).

All paths below are relative to this repo.

### 1.1 Inputs (real DPI receipts)

- `demo_dpi_2025-11/data/dpi_royalty_receipts.ndjson`  
  3,718 `royalty_receipt.v1` rows, one per finetuning dataset  
  (`provider_id` ≈ dataset / collection name, with licenses and HF links in `meta`).

These are real datasets (Hugging Face / DPI), mapped into an open, machine-readable attribution log format.

### 1.2 Outputs (payouts, trust, compliance)

The full `.tgz` used in the live demo is served from:

https://croviatrust.com/demo/crovia_dpi_demo_2025-11.tgz


Under `demo_dpi_2025-11/output/` you will find:

- `dpi_payouts_2025-11.csv`  
- `dpi_payouts_2025-11.ndjson`  
  → one **payout per provider** (3,717 providers, €1M total budget).

- `README_PAYOUT_2025-11.md`  
  → human-readable explanation of how the demo split the €1M budget.

- `DPI_VALIDATE.md`  
  → validation report over the receipts (`qa_receipts` + `crovia_validate`).

- `DPI_AI_ACT_2025-11.md`  
  → EU AI Act–style coverage & gap analysis for this exact run.

- `dpi_compliance_pack_2025-11.json`  
  → machine-readable compliance pack (same information as the Markdown, for tools).

- `dpi_trust_bundle_2025-11.json`  
  → the core **`trust_bundle.v1`** object:
    - references all the artifacts above,
    - stores their SHA-256 hashes and sizes,
    - is designed to be **sign-ready** for auditors / regulators.

### 1.3 Merkle root over payouts

New in this repo:

- `dpi_merkle_payouts_2025-11.json`  
  → a **`merkle_payouts.v1`** document that commits to **all provider payouts** via a Merkle tree.

It has the following shape (informal JSON example):

{
  "schema": "merkle_payouts.v1",
  "algo": "merkle_sha256_leaf_ndjson_v1",
  "created_at": "2025-11-24T…Z",
  "target": {
    "path": "demo_dpi_2025-11/output/dpi_payouts_2025-11.ndjson",
    "schema": "payouts.v1",
    "sha256": "…",
    "leaf_encoding": "raw_ndjson_line",
    "leaf_count": 3717
  },
  "root": "02690a2a637a400d28bd90eb9b2b1a55d9e8e6b6be48fb744b7c0bddcf913fdb"
}

This Merkle root is computed over each raw NDJSON line in `dpi_payouts_2025-11.ndjson`,
with the exact file bytes (no pretty-printing, no re-ordering).

---

## 2. Specs

- `spec/trust_bundle.v1.md` – informal spec for the CROVIA `trust_bundle.v1` profile.  
- `spec/merkle_payouts.v1.md` – informal spec for `merkle_payouts.v1` (leaf definition + JSON shape).

---

## 3. Recompute the Merkle root yourself

You can recompute the Merkle root with a single Python script included in this repo.

**Requirements**

- Python 3.11+ (stdlib only)

**Run**

    cd /path/to/crovia-core
    python3 tools/build_merkle_payouts.py

**Expected output**

    [MERKLE] Reading payouts NDJSON: demo_dpi_2025-11/output/dpi_payouts_2025-11.ndjson
    [MERKLE] root=02690a2a637a400d28bd90eb9b2b1a55d9e8e6b6be48fb744b7c0bddcf913fdb  leaves=3717
    [MERKLE] written demo_dpi_2025-11/output/dpi_merkle_payouts_2025-11.json

If you get the same root, you know that:

- Your checkout of `dpi_payouts_2025-11.ndjson` is intact (no tampering).  
- The Merkle algorithm is fully determined by the spec in `spec/merkle_payouts.v1.md`.  
- Anyone else in the world can reproduce the same commitment over all 3,717 provider payouts.

---

## 4. Minimal 10-line example

For workshops / talks / tests, there is a tiny example:

- `examples/simple_10_receipts.ndjson`

This is a hand-written `royalty_receipt.v1` snippet (10 outputs, a few providers).  
You can plug it into your own tooling to prototype a payout policy before touching the full DPI demo.

---

## 5. What is not in this repo (yet)

This repo intentionally does not include the full CROVIA engine code that produced the demo:

- The core payout policy implementation  
- The CLI runner scripts  
- Internal configs used to tune the synthetic €1M budget split  

Right now this is a transparent audit pack + specs + Merkle tool:

- You can see the receipts, payouts, trust bundle, AI Act coverage and Merkle root.  
- You can re-compute hashes and the Merkle root on your own machine.  
- You can use the formats (`royalty_receipt.v1`, `payouts.v1`, `trust_bundle.v1`, `merkle_payouts.v1`)
  in your own pipelines or engines.

**Future work (planned)**

- Open-sourcing a minimal reference engine for the M0 profile.  
- Per-provider Merkle proofs (`merkle_proof.v1`) so creators can verify their individual payout
  with a tiny JSON file instead of the whole bundle.  
- Optional “Crovia Floor” policy profiles (minimum payout per provider).

---

## 6. Story & contact

> If AI is going to eat the world,  
> the people who create the data should be in the payout loop.

This repo is one concrete step:  
3,718 real finetuning datasets → 3,717 providers → €1M simulated budget →  
trust bundle + AI Act pack + Merkle root you can verify offline.

**Feedback, collaborations, real-data pilots**

- X / Twitter: `@croviatrust`  
- Website: https://croviatrust.com  

MIT License – fork, test, break, improve.
