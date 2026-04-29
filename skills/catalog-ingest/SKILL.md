---
name: catalog-ingest
description: Use when ingesting a music catalog data room, royalty statements, rights files, metadata exports, or messy catalog spreadsheets for diligence. Triggers include "catalog data room", "clean royalty statements", "normalize royalties", "music rights diligence", "catalog ingest", "merge catalog metadata", "prepare this catalog for valuation", or seller files containing ISRCs, ISWCs, splits, PRO statements, distributor reports, contracts, recoupment schedules, or YouTube Content ID reports.
---

# Catalog Ingest

Turn messy music catalog data rooms into auditable hand-off artifacts for
diligence and valuation. The job is not to value the catalog. The job is to make
the data trustworthy enough that valuation can happen.

## Decision tree

Start here based on what the user gives you:

- **Full data room** -> inventory files, classify sources, then build the ingest
  package.
- **Single royalty statement** -> parse it into normalized ledger rows and
  preserve source lineage.
- **Conflicting catalog spreadsheets** -> reconcile into a canonical catalog
  table with confidence scores and unresolved conflicts.
- **Royalty income without rights files** -> keep the income, but mark ownership
  support as missing.
- **User asks for valuation immediately** -> first verify whether canonical
  ingest artifacts exist. If not, ingest before valuation.

If the user only wants lightweight cleanup, still preserve raw files and source
columns. Never silently overwrite source data.

## Core workflow

1. **Preserve raw files.** Do not edit source exports in place.
2. **Inventory the data room.** Build a file map with path, source, file type,
   period, currency, likely rights type, and confidence.
3. **Classify each source.** Use financial, legal, metadata, asset, analytics,
   or unknown.
4. **Profile spreadsheets before cleaning.** Check grain, keys, null rates,
   duplicates, date ranges, mixed types, identifier formats, and split totals.
5. **Propose fixes before destructive cleanup.** Show the issue, count, and
   planned fix. Ask before removing rows, overwriting values, or deduplicating.
6. **Build the canonical catalog table.** Match recordings and compositions
   using ISRC, ISWC, title, writer, artist, release, and alternate-title clues.
7. **Normalize royalty statements.** Convert every statement into ledger rows
   with source, period, asset, right type, territory, gross, deductions,
   participant shares, owner net, and source lineage.
8. **Build the rights map.** Link songs and recordings to contracts,
   registrations, splits, controlled shares, restrictions, and missing support.
9. **Reconcile and flag exceptions.** Separate financial facts from rights
   certainty. A royalty line proves money was reported; it does not prove clean
   transferable ownership.
10. **Export the ingest package.** Include canonical tables, source lineage,
    data-quality notes, and missing-file tracker.

## Output contract

Use these artifacts unless the user asks for a different structure:

| Artifact | Purpose |
| --- | --- |
| `ingest-manifest.md` | Explains source files, assumptions, and scope. |
| `data-room-inventory.csv` | One row per source file. |
| `canonical-catalog.csv` | One row per controlled work/recording candidate. |
| `royalty-ledger.csv` | Normalized income lines across statements. |
| `rights-map.csv` | Ownership, splits, contracts, restrictions, support level. |
| `source-lineage.csv` | Field-level or row-level source traceability. |
| `missing-files.md` | Required files, unresolved conflicts, and diligence asks. |
| `data-quality-report.md` | Profiling results and cleanup decisions. |

Detailed schemas are in
**[references/canonical-schema.md](references/canonical-schema.md)**.

## Critical gotchas

- **Do not value before lineage.** If the catalog table and royalty ledger cannot
  tie back to source files, the valuation will look precise and be unreliable.
- **NPS and NLS are different.** Publishing uses Net Publisher Share; masters use
  Net Label Share. Do not merge them into one "net revenue" field without a
  rights-type column.
- **A royalty statement is not chain of title.** Income for a song with no split
  sheet or agreement is unsupported income, not clean ownership.
- **Splits must reconcile.** Writer, publisher, master, producer, and
  participant splits may live on different bases. Do not force them to total
  100% until you know what the denominator represents.
- **Identifiers beat names.** Match by ISRC/ISWC/IPI/UPC first. Use title and
  artist matching only as lower-confidence evidence.
- **Preserve PRO detail.** If statements expose use type, credits, premium/
  bonus columns, cue-sheet data, or territory, keep those fields. They matter
  for sustainability analysis.
- **Keep unsupported income in the ledger.** Excluding it hides the size of the
  issue. Mark it with low rights confidence and list required follow-up.
- **Do not fabricate missing legal facts.** If rights, recoupment, reserves, or
  restrictions are unknown, keep them unknown.

## What to read next

- For expected data-room files, read
  **[references/data-room-checklist.md](references/data-room-checklist.md)**.
- For canonical fields and confidence scoring, read
  **[references/canonical-schema.md](references/canonical-schema.md)**.
- For cleanup rules and review tables, read
  **[references/cleaning-rules.md](references/cleaning-rules.md)**.
