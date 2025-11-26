# Crovia Core – DPI demo (November 2025)

This folder contains a **public, reproducible demo** of Crovia
run on the MIT Data Provenance Initiative (DPI) finetuning collection.

What you get here:

- `demo_dpi_2025-11/data/dpi_royalty_receipts.ndjson`  
  NDJSON `royalty_receipt.v1` logs for 3,718 DPI datasets.

- `demo_dpi_2025-11/output/dpi_payouts_2025-11.{csv,ndjson}`  
  Provider-level payouts for a simulated EUR 1,000,000 budget.

- `demo_dpi_2025-11/output/dpi_trust_bundle_2025-11.json`  
  A single `trust_bundle.v1` JSON that ties together receipts, payouts
  and compliance artifacts, with SHA-256 hashes for offline verification.

- `demo_dpi_2025-11/output/DPI_AI_ACT_2025-11.md`  
  AI Act–style training data summary for this run.

- `examples/simple_10_receipts.ndjson`  
  Tiny 10-line example you can inspect or feed into your own tools.

The full `.tgz` used in the live demo is served from:

https://croviatrust.com/demo/crovia_dpi_demo_2025-11.tgz

This repo skeleton is meant to be the public, minimal core for Crovia
— no secrets, no internal configs, just verifiable artifacts.
