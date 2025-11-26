# CROVIA – `trust_bundle.v1`

This note defines the **`trust_bundle.v1`** JSON profile.

A **Trust Bundle** is a compact, hash-addressable evidence pack that ties together:

- the **attribution logs** (`royalty_receipt.v1`),
- the resulting **payouts** (`payouts.v1`),
- optional **trust / priority metrics** per provider,
- **validation and compliance reports** (e.g. EU AI Act),
- and the **hashes** of all these artifacts.

The goal is to produce **one sign-ready JSON object** that an auditor, regulator or partner can verify offline.

---

## 1. Top-level shape

A `trust_bundle.v1` JSON has the following top-level fields (informal example):

    {
      "schema": "trust_bundle.v1",
      "profile_id": "CROVIA_M0_DPI_DEMO_v1",
      "period": "2025-11",
      "model_id": "crovia-dpi-demo-v1",

      "created_at": "2025-11-22T10:00:00Z",
      "engine": {
        "implementation": "crovia-trust-demo",
        "version": "2025-11.dpi.v1"
      },

      "jurisdictions": ["EU", "EU AI Act"],

      "inputs": {
        "royalty_receipts": { /* see §2 */ }
      },

      "artifacts": {
        /* see §3 */
      },

      "stats": {
        /* see §4 */
      },

      "attestations": [
        /* optional digital signatures, see §5 */
      ]
    }

### Required fields

- `schema` MUST be `"trust_bundle.v1"`.
- `profile_id` identifies the policy / profile used for this bundle  
  (e.g. `"CROVIA_M0_DPI_DEMO_v1"`).
- `period` is the accounting period for the payouts (e.g. `"2025-11"`).
- `model_id` identifies the model / engine that produced the outputs.
- `created_at` is an ISO-8601 UTC timestamp for bundle creation.
- `engine` describes the payout engine that produced the artifacts.
- `jurisdictions` is a list of strings (e.g. `"EU AI Act"`).
- `inputs`, `artifacts` and `stats` are required objects.
- `attestations` MAY be an empty list.

---

## 2. `inputs.royalty_receipts`

The `inputs` section points to the attribution logs that drive the whole bundle.

Example:

    "inputs": {
      "royalty_receipts": {
        "path": "data/dpi_royalty_receipts.ndjson",
        "bytes": 123456,
        "sha256": "…",
        "total_outputs": 3718,
        "schema": "royalty_receipt.v1"
      }
    }

### Requirements

- `path` is a path relative to the bundle root (where the bundle is meant to live).
- `bytes` is the exact byte size of the file.
- `sha256` is the SHA-256 digest of the raw file bytes (hex-encoded, lowercase).
- `total_outputs` is the number of rows / events in the receipts NDJSON.
- `schema` MUST be `"royalty_receipt.v1"`.

If multiple input streams exist (e.g. separate logs per region), additional keys MAY be
added under `inputs` (e.g. `royalty_receipts_eu`, `royalty_receipts_us`). Each MUST
follow the same shape.

---

## 3. `artifacts.*`

The `artifacts` object lists all outputs and reports produced for this run.

Every artifact shares a common core shape. Example:

    "artifacts": {
      "payouts_ndjson": {
        "path": "data/dpi_payouts_2025-11.ndjson",
        "bytes": 12345,
        "sha256": "…",
        "schema": "payouts.v1"
      },

      "payouts_csv": {
        "path": "data/dpi_payouts_2025-11.csv",
        "bytes": 23456,
        "sha256": "…",
        "schema": "payouts.v1",
        "providers": 3717,
        "total_amount": 1000000.00,
        "gross_revenue": 1000000.00,
        "currency": "EUR"
      },

      "trust_providers_csv": {
        "path": "data/dpi_trust_providers_2025-11.csv",
        "bytes": 34567,
        "sha256": "…",
        "kind": "trust_providers"
      },

      "trust_summary_md": {
        "path": "docs/DPI_TRUST_2025-11.md",
        "bytes": 4567,
        "sha256": "…",
        "kind": "trust_report"
      },

      "validate_report_md": {
        "path": "docs/DPI_VALIDATE.md",
        "bytes": 5678,
        "sha256": "…",
        "kind": "validation_report"
      },

      "ai_act_summary_md": {
        "path": "docs/DPI_AI_ACT_2025-11.md",
        "bytes": 6789,
        "sha256": "…",
        "kind": "ai_act_summary"
      },

      "ai_act_pack_json": {
        "path": "data/dpi_compliance_pack_2025-11.json",
        "bytes": 7890,
        "sha256": "…",
        "kind": "ai_act_pack"
      },

      "compliance_gaps_csv": {
        "path": "compliance_gaps.csv",
        "bytes": 8901,
        "sha256": "…",
        "kind": "compliance_gaps"
      }
    }

### Core fields

For every artifact entry:

- `path` – path relative to the bundle root.  
- `bytes` – exact byte size of the file.  
- `sha256` – SHA-256 digest of the raw file bytes (hex-encoded, lowercase).  
- `schema` – used for machine-readable objects (e.g. `"payouts.v1"`).  
- `kind` – used for human-oriented reports (e.g. `"trust_report"`, `"validation_report"`).

At least one payouts artifact (CSV or NDJSON) MUST be present with `schema: "payouts.v1"`.

Other entries are OPTIONAL: a given bundle MAY omit, for example, `trust_providers_csv` or
`compliance_gaps_csv` if such artifacts were not produced for that run. The profile is
intentionally flexible: what matters is that every referenced artifact can be located and
verified offline.

### 3.1 Optional Merkle payouts artifact

If payouts are committed via a Merkle tree (see `merkle_payouts.v1` profile), the bundle
MAY include an explicit reference:

    "merkle_payouts_json": {
      "path": "data/dpi_merkle_payouts_2025-11.json",
      "bytes": 12345,
      "sha256": "…",
      "schema": "merkle_payouts.v1"
    }

This links the bundle to a single Merkle root over all provider-level payouts, making it
easy to add per-provider Merkle proofs in a separate `merkle_proof.v1` profile.

---

## 4. `stats`

The `stats` section summarizes the run.

Example:

    "stats": {
      "total_outputs": 3718,
      "providers": 3717,
      "budget_eur": 1000000.00,
      "paid_out_eur": 999999.99
    }

Typical fields:

- `total_outputs` – number of attribution records (rows in `royalty_receipt.v1`).  
- `providers` – distinct `provider_id` that received a payout.  
- `budget_eur` – total EUR budget configured for the period.  
- `paid_out_eur` – sum of all `amount` values in the payout CSV / NDJSON.

Additional fields MAY be added (e.g. `concentration_metrics`, `hhi`, `gini`) as long as
they are numeric or clearly documented.

---

## 5. `attestations`

`attestations` is an extensible list intended for digital signatures and external notaries.

Example:

    "attestations": [
      {
        "type": "pgp-signature.v1",
        "key_id": "…",
        "created_at": "2025-11-22T11:00:00Z",
        "signature": "base64-encoded-signature"
      }
    ]

The `trust_bundle.v1` profile does not mandate a specific signature scheme.  
Examples include:

- PGP / OpenPGP signatures,  
- X.509 / PKI signatures,  
- blockchain-anchored proofs referenced via an external ID.

Each entry SHOULD specify at least `type`, `created_at` and a `signature` or reference.

---

## 6. DPI demo: example instantiation

In the CROVIA DPI demo (period 2025-11), the bundle ties together:

- 3,718 real finetuning datasets from the MIT Data Provenance Initiative,  
- a simulated €1M budget split over those datasets (`payouts.v1`),  
- per-dataset trust / priority bands (optional trust metrics),  
- an EU AI Act–style compliance pack with coverage & gaps,  
- a single `trust_bundle.v1` JSON with SHA-256 hashes for each artifact,  
- and an optional `merkle_payouts.v1` document committing to all payouts.

In that demo:

- the bundle itself lives at  
  `demo_dpi_2025-11/output/dpi_trust_bundle_2025-11.json`
- the receipts live at  
  `demo_dpi_2025-11/data/dpi_royalty_receipts.ndjson`
- the main payouts live at  
  `demo_dpi_2025-11/output/dpi_payouts_2025-11.{csv,ndjson}`
- the AI Act pack lives at  
  `demo_dpi_2025-11/output/dpi_compliance_pack_2025-11.json`
- the Merkle commitment lives at  
  `demo_dpi_2025-11/output/dpi_merkle_payouts_2025-11.json`

This provides a single, sign-ready object that lets any third party recompute and verify:

> “Given these attribution logs and this policy,  
> who was paid what, and which datasets were covered?”
