# Music Catalog Diligence Plugin

Agent plugin for music catalog acquisition, seller preparation, financing
underwriting, royalty normalization, rights checks, and valuation analysis.

The plugin helps catalog teams turn a messy seller data room into a
source-cited deal package: normalized royalty data, rights exceptions,
valuation workpapers, and buyer/seller/lender-ready memos.

## Skills

| Skill | What it does |
| ----- | ------------ |
| `diligence-kickoff` | Set up a deal workspace, classify workflow type, and create the first missing-file list. |
| `catalog-ingest` | Ingest and normalize music catalog data rooms, royalty statements, metadata, and rights files into auditable hand-off artifacts. |
| `catalog-analysis` | Analyze normalized catalog royalties, risk, and cash flows to project catalog value for acquisitions, financing, or sale processes. |
| `rights-diligence` | Review ownership support, chain of title, splits, restrictions, and transferability. |
| `royalty-audit` | Audit statements, normalized ledgers, PRO/MLC issues, and gross-to-net support. |
| `seller-prep` | Create cleanup worklists that reduce avoidable valuation discounts before going to market. |
| `financing-underwrite` | Build lender-ready collateral and cash-flow diligence for royalty-backed financing. |
| `ic-memo-package` | Assemble IC memos, seller cleanup reports, financing packs, and final deal outputs. |
| `post-close-admin` | Turn diligence data into transfer, registration, and income-monitoring worklists. |

## Commands

| Command | Purpose |
| ------- | ------- |
| `catalog-diligence` | Run the end-to-end workflow from setup through package readiness. |
| `catalog-kickoff` | Start a deal workspace and route the work. |
| `catalog-ingest` | Normalize a data room into source-cited artifacts. |
| `catalog-analyze` | Run catalog analysis, workpapers, and specialist review. |
| `catalog-qc` | Check evidence, assumptions, findings, and memo readiness. |
| `catalog-package` | Assemble a buyer, seller, lender, or post-close package. |

## Deal workspace

Use one workspace per opportunity:

```text
deals/{deal-id}/
├── source/
├── normalized/
├── workpapers/
├── findings/
├── memos/
├── assumptions.yaml
└── evidence-ledger.json
```

Source files are immutable. Work from normalized data, workpapers, findings,
and memos.

## Structure

```text
music-catalog-diligence/
├── .claude-plugin/
│   └── plugin.json
├── .codex-plugin/
│   └── plugin.json
├── .cursor-plugin/
│   └── plugin.json
├── agents/
├── commands/
├── evals/
├── references/
├── scripts/
├── skills/
├── templates/
└── README.md
```

Claude Code and Cursor load the full plugin surface, including skills,
commands, and agents. Codex loads the bundled skills through
`.codex-plugin/plugin.json`.

## Development

Keep each skill focused and self-contained. Use `references/` for detailed
domain material so each `SKILL.md` stays easy to scan. Use `scripts/` for
deterministic checks that should not depend on prose reasoning.

Current scripts include validators, readiness dashboard generation,
concentration/bridge calculators, and `normalize-royalty-statement.py` for
first-pass ASCAP, BMI, MLC, distributor, publisher admin, SoundExchange, direct
sync, YouTube Content ID, and Curve-style CSV normalization.

Golden fixtures live under `fixtures/golden/`. Run these checks before release:

```bash
python3 scripts/test-normalize-royalty-statement.py
python3 scripts/test-golden-fixtures.py
python3 scripts/test-validate-deal-workspace.py
python3 scripts/test-diligence-readiness.py
```

Use `python3 scripts/run-diligence-checks.py deals/{deal-id}` to validate a
workspace and `python3 scripts/build-diligence-dashboard.py deals/{deal-id}` to
generate a shareable readiness summary.

## About

[Recoupable](https://recoupable.com) builds AI-powered infrastructure for music
operators.
