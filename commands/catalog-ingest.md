---
name: catalog-ingest
description: Normalize a catalog data room into auditable catalog, royalty, rights, and evidence artifacts.
---

# Catalog Ingest

Use the `catalog-ingest` skill.

Steps:

1. Confirm raw files are under `deals/{deal-id}/source/`.
2. Build or update the file manifest with
   `python3 scripts/build-file-manifest.py deals/{deal-id}/source`.
3. Normalize catalog, royalty, rights, and source-lineage artifacts into
   `normalized/`.
4. Write cleanup and missing-file notes into `findings/`.
5. Run `python3 scripts/validate-normalized-ledger.py deals/{deal-id}/normalized/royalty-ledger.csv`
   after creating the ledger.
6. Run `python3 scripts/validate-deal-workspace.py deals/{deal-id}` before
   moving to analysis.

Do not edit source files. Do not produce a valuation unless ingest artifacts
exist and the user explicitly asks to continue.
