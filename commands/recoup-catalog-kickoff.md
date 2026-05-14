---
name: recoup-catalog-kickoff
description: Set up a music catalog deal workspace and first diligence request list. For full end-to-end runs prefer /recoup-catalog-diligence.
---

# Catalog Kickoff

Use the `recoup-diligence-kickoff` skill.

> **Most users should run `/recoup-catalog-diligence` instead** — that command
> chains kickoff → ingest → analysis → dashboard → memo without
> stopping. This command is kickoff only, for analysts who want to
> scaffold a workspace and stop before ingest.

## Steps

1. Identify workflow type: buy-side, recoup-seller-prep, or financing.
2. Create or locate `deals/{deal-id}/`.
3. Apply templates from `templates/deal-workspace/`.
4. Build the initial missing-file list in
   `findings/missing-files.md` based on the user's described data room.
5. Run `python3 scripts/validate-deal-workspace.py deals/{deal-id}` to
   confirm the scaffold exists. Validator failures here are expected
   until normalized artifacts are created — use the missing requirements
   as the initial worklist.
6. Recommend the next command. The default recommendation is
   `/recoup-catalog-diligence` (it picks up where kickoff stopped). Only
   recommend a single phase command if the user explicitly asked for
   one.

Do not value the catalog during kickoff.

## Final landing card

```text
✅ Workspace scaffolded.

  Deal:        deals/{deal-id}/
  Workflow:    <buy-side | recoup-seller-prep | financing>
  Files in:    <count> seller-supplied files staged in source/

  Initial worklist (from references/diligence-workflow.md):
    - <missing item 1>
    - <missing item 2>

Next:
  /recoup-catalog-diligence    — drive end-to-end (recommended)
  /recoup-catalog-ingest       — ingest only
```
