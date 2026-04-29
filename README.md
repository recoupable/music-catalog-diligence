# Music Catalogs Plugin

Claude Code plugin for music catalog diligence, royalty normalization, and
valuation analysis.

## Skills

| Skill | What it does |
| ----- | ------------ |
| `catalog-ingest` | Ingest and normalize music catalog data rooms, royalty statements, metadata, and rights files into auditable hand-off artifacts. |
| `catalog-analysis` | Analyze normalized catalog royalties, risk, and cash flows to project catalog value for acquisitions, financing, or sale processes. |

## Structure

```text
music-catalogs/
├── .claude-plugin/
│   └── plugin.json
├── skills/
│   ├── catalog-ingest/
│   └── catalog-analysis/
└── README.md
```

## Development

Keep each skill focused and self-contained. Use `references/` for detailed
domain material so each `SKILL.md` stays easy to scan.

## About

[Recoupable](https://recoupable.com) builds AI-powered infrastructure for music
operators.
