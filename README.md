# Recoup Catalog Diligence

Agent plugin for music catalog acquisition, seller preparation, financing
underwriting, royalty normalization, rights checks, and valuation
analysis. Built by [Recoup](https://recoupable.com).

The plugin turns a messy seller data room into a source-cited deal
package: normalized royalty data, rights exceptions, valuation
workpapers, an **agent-authored HTML dashboard**, and buyer/seller/lender
memos. The whole thing is driven by a single command —
`/recoup-catalog-diligence`.

## Install

### Claude Desktop (non-technical users)

Not a developer? Step-by-step guide with screenshots:
**[docs/install-claude-desktop.md](docs/install-claude-desktop.md)**.
It takes about 5 minutes — no Terminal needed.

### Claude Code (CLI)

```bash
claude plugin install https://github.com/recoupable/recoup-catalog-diligence
```

Then **restart your Claude Code session** so `hooks/hooks.json` loads.

### Claude Cowork

1. Open the plugin marketplace (puzzle-piece icon in the sidebar).
2. Click **Add custom plugin** and paste:
   `https://github.com/recoupable/recoup-catalog-diligence`
3. Approve the requested tool permissions (`Read`, `Write`, `Bash` —
   needed to run the validator scripts).
4. **Restart the Cowork session** so the PreToolUse and Stop hooks
   load.
5. Confirm install: type `/plugin` and check that
   `recoup-catalog-diligence` is listed.

### Cursor

1. Cursor → Settings → Plugins → **Add custom plugin**.
2. Paste the GitHub URL above.
3. Restart Cursor so `.cursor-plugin/plugin.json` loads commands,
   skills, and agents.

### Optional dependencies

Core scripts run on the Python standard library alone. PDF and XLSX
extraction need two extra packages:

```bash
pip3 install -r requirements.txt   # pdfplumber, openpyxl
```

You can skip this if your data room is CSV/TSV only.

## Getting started

After installing, open a new chat in Claude and try:

> **Let's analyze a catalog with /recoup-catalog-diligence**

Claude will ask what kind of deal this is (buy-side, seller-prep, or
financing) and what to call it. Drag your seller's files into the
chat — royalty statements, contracts, metadata exports, even messy
ones. Claude runs the full workflow end-to-end: scaffolds the
workspace, normalizes the royalties, flags rights issues, builds an
interactive dashboard, and drafts an IC memo.

When it finishes, open:

```text
deals/{deal-id}/DASHBOARD.html
```

The dashboard is **authored by the agent** for your specific
catalog — layout, charts, and narrative shaped by the deal's story.
A concentration-driven catalog reads differently than a recoupment-
cliff catalog. Agents in May 2026 build remarkable dashboards when
given good direction; the `skills/recoup-catalog-dashboard/SKILL.md`
file is that direction.

When you're ready to share the deal with a buyer, IC, or lender:

```text
/recoup-catalog-report
```

That exports a single PDF you can attach to an email.

### No catalog handy? Try the demo

To see what the plugin produces before pointing it at a real deal — or
to show a teammate — run `/recoup-catalog-demo`. It runs the full
workflow against a bundled synthetic catalog.

## Commands

| Command | When to use it |
| ------- | -------------- |
| `/recoup-catalog-diligence` | **Default.** End-to-end run from kickoff to dashboard and IC memo, no stops between phases. |
| `/recoup-catalog-demo` | Optional: runs the full workflow on a bundled synthetic catalog. Useful for showing a teammate what the plugin produces. |
| `/recoup-catalog-kickoff` | Power-user: scaffold the workspace and stop. |
| `/recoup-catalog-ingest` | Power-user: re-normalize after dropping new files into `source/`. Auto-recovers when seller headers don't match a provider profile. |
| `/recoup-catalog-analyze` | Power-user: refresh analysis workpapers (NPS/NLS bridge, valuation summary). |
| `/recoup-catalog-dashboard` | Power-user: refresh `DASHBOARD.html` after editing workpapers, findings, or recommendations. |
| `/recoup-catalog-qc` | Power-user: re-run QC after editing findings or memos. |
| `/recoup-catalog-package` | Power-user: refine the IC memo / financing pack / seller cleanup report. |
| `/recoup-catalog-report` | Export the validated dashboard + memo as a single shareable PDF you can email (`deals/{deal-id}/REPORT.pdf`). |

If you're new to the plugin, ignore the power-user commands and start
with `/recoup-catalog-diligence`. Try `/recoup-catalog-demo` only if
you want to see the output before pointing it at a real deal.

## Skills

Loaded automatically by description-matching when the agent recognizes
the task:

| Skill | What it does |
| ----- | ------------ |
| `recoup-diligence-kickoff` | Scaffolds a deal workspace and produces the first missing-file list. |
| `recoup-catalog-ingest` | Normalizes data rooms, royalty statements, metadata, and rights files into auditable hand-off artifacts. |
| `recoup-catalog-analysis` | Analyzes normalized cash flows and projects value. |
| `recoup-catalog-dashboard` | Authors the customer-facing HTML dashboard. The agent picks layout, charts, narrative, and depth — guided by a strong skill spec and a post-hoc validator. |
| `recoup-catalog-report` | Packages the validated dashboard + memo + workpapers as a single shareable PDF (`deals/{deal-id}/REPORT.pdf`). Agent picks the conversion path (headless Chrome, Playwright, WeasyPrint, or ReportLab). |
| `recoup-rights-diligence` | Reviews ownership support, chain of title, splits, restrictions, transferability. |
| `recoup-royalty-audit` | Audits statements, normalized ledgers, PRO/MLC issues, gross-to-net support. |
| `recoup-seller-prep` | Creates cleanup worklists that reduce avoidable valuation discounts before going to market. |
| `recoup-financing-underwrite` | Builds lender-ready collateral and cash-flow diligence. |
| `recoup-ic-memo-package` | Assembles IC memos, seller cleanup reports, financing packs, and final outputs. |
| `recoup-post-close-admin` | Turns diligence data into transfer, registration, and income-monitoring worklists. |

## What you get when `/recoup-catalog-diligence` finishes

```text
deals/{deal-id}/
├── DASHBOARD.html              ← open this first (agent-authored)
├── REPORT.pdf                  ← optional shareable export (run /recoup-catalog-report)
├── source/                     ← raw seller files (immutable)
├── normalized/
│   ├── royalty-ledger.csv
│   ├── canonical-catalog.csv
│   └── rights-map.csv
├── workpapers/
│   ├── file-manifest.json
│   ├── ingest-coverage.json
│   ├── concentration-analysis.json
│   ├── valuation-summary.json
│   ├── nps-bridge.json
│   ├── nls-bridge.json
│   ├── recommendations.json
│   └── readiness-check.md       ← internal-only QC view
├── findings/
│   ├── findings.json
│   ├── missing-files.md
│   └── manual-review-queue.md
├── memos/
│   └── ic-memo.md
├── assumptions.yaml
└── evidence-ledger.json
```

`DASHBOARD.html` is the customer-facing artifact. Everything else is
provenance, evidence, and internal QC. `source/` is treated as
immutable evidence — writes into it are denied by the PreToolUse hook
so the agent cannot accidentally mutate the data room.

## How the agent stays honest

The trust model has two complementary layers:

### Deterministic source files

Royalty ledgers, valuation summaries, NPS/NLS bridges, concentration
analyses, findings, and the evidence ledger are all structured JSON
or CSV. They go through validators
(`scripts/run-diligence-checks.py`) that confirm shape, evidence
references, cross-artifact consistency, and findings-to-evidence
traceability. These are the source of truth.

### Post-hoc dashboard verification

The dashboard itself is built by the agent — full creative freedom on
layout, chart types (Chart.js, D3, Plotly), tabs, scenario sliders,
narrative structure, depth. After the agent writes
`DASHBOARD.html`, `scripts/validate-dashboard.py` runs and enforces:

1. File exists, parses as HTML, between 5 KB and 5 MB.
2. Required structural markers present (status, KPIs, findings,
   recommendations, evidence trail).
3. External `<script src>` tags only from a CDN allowlist
   (`cdn.jsdelivr.net`, `cdnjs.cloudflare.com`, `unpkg.com`).
4. No `<iframe>`, `<object>`, `<embed>`, `eval(`, `Function(`,
   `document.write(`.
5. Every `$`-claim in the rendered text either matches a workpaper
   value within 5%, or carries a `data-evidence`, `data-source`, or
   `data-derived` attribute (or any ancestor does). Unverified
   numerical claims fail the validator.

### Two hooks defined in `hooks/hooks.json`

- **PreToolUse `protect-source-files.sh`** — denies any
  `Write`/`Edit`/`MultiEdit` whose path matches `*/deals/*/source/*`.

- **Stop hook (prompt-based, two gates)**.
  - Gate A (completion claims) — when the agent claims a package is
    "ready", the hook verifies that `run-diligence-checks.py` ran
    cleanly, the readiness check isn't `blocked`, `assumptions.yaml`
    and `evidence-ledger.json` exist, findings aren't silently
    dropped, and memo claims trace to evidence.
  - Gate B (mid-workflow progress) — when the user launched
    `/recoup-catalog-diligence` or `/recoup-catalog-demo`, the hook blocks the
    agent from stopping until `DASHBOARD.html` exists **and**
    `validate-dashboard.py` returned `status: ok`. This is what
    prevents the agent from quitting after Phase 2 with "want me to
    continue?"

Restart your session after editing `hooks/hooks.json`.

## Development

Keep each skill focused and self-contained. Use `references/` for
detailed domain material so each `SKILL.md` stays easy to scan. Use
`scripts/` for deterministic checks and the dashboard validator —
**not** for rendering customer-facing HTML. The dashboard is the
agent's deliverable; presentation is its job.

Current scripts include validators, the dashboard validator,
normalization, auto-column-mapping recovery, and concentration / NPS-NLS
bridge calculators. The auto column mapper
(`scripts/auto-column-map.py`) is the recovery path when a seller's
CSV uses non-canonical headers — the agent runs it automatically when
normalization returns `status: "partial"`.

Golden fixtures live under `fixtures/golden/` (per-provider canonical
input/expected output pairs). The synthetic demo catalog lives under
`fixtures/demo-data-room/` — that's what `/recoup-catalog-demo` copies in.

Run all tests before release:

```bash
python3 scripts/test-normalize-royalty-statement.py
python3 scripts/test-golden-fixtures.py
python3 scripts/test-validate-deal-workspace.py
python3 scripts/test-validate-findings-evidence.py
python3 scripts/test-validate-workspace-consistency.py
python3 scripts/test-build-manual-review-queue.py
python3 scripts/test-calculate-concentration.py
python3 scripts/test-dataroom-hygiene-scan.py
python3 scripts/test-diligence-readiness.py
python3 scripts/test-helpers.py
python3 scripts/test-validate-dashboard.py
python3 scripts/test-auto-column-map.py
```

Operate a real deal workspace with:

```bash
python3 scripts/run-diligence-checks.py deals/{deal-id}
python3 scripts/build-diligence-dashboard.py deals/{deal-id}      # internal readiness
python3 scripts/validate-dashboard.py deals/{deal-id}             # check agent's DASHBOARD.html
```

## Structure

```text
recoup-catalog-diligence/
├── .claude-plugin/plugin.json
├── .codex-plugin/plugin.json
├── .cursor-plugin/plugin.json
├── agents/                     # Specialist sub-agents (QC, rights, royalty, valuation, metadata)
├── commands/                   # Slash commands — start with /recoup-catalog-diligence
├── evals/                      # Behavioral eval scenarios
├── fixtures/
│   ├── demo-data-room/         # Synthetic catalog used by /recoup-catalog-demo
│   └── golden/                 # Per-provider canonical input/output pairs
├── hooks/                      # PreToolUse + Stop guardrails
├── references/                 # Domain knowledge (workflow, red flags, normalization, tooling)
├── scripts/                    # Deterministic Python — validators only, no renderers
├── skills/                     # Loaded by description-matching at runtime
│   └── recoup-catalog-dashboard/      # The agent's guide to authoring DASHBOARD.html
├── templates/deal-workspace/   # Workspace scaffolding (assumptions, findings, evidence, memos)
└── README.md
```

## About

[Recoup](https://recoupable.com) builds AI-powered infrastructure for
music operators.

- Plugin: `recoup-catalog-diligence`
- Repository: <https://github.com/recoupable/recoup-catalog-diligence>
- Support: <support@recoupable.com>
