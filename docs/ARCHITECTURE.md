# TRIZEL Architecture — Repository Coordination Reference

This document defines the coordination contract for the TRIZEL 3I-ATLAS monitoring
pipeline. It specifies repository purpose, boundaries, data flow, and operational
rules for all repositories in the architecture.

---

## 1. Repository Purpose

**`trizel-ai/Auto-dz-api-monitor`** (this repository) is the **monitoring layer**
of the TRIZEL 3I-ATLAS pipeline. Its sole purpose is:

> Automated source retrieval and archival package preparation for the
> interstellar object **3I-ATLAS**.

Concretely, this means:

- Fetching raw observation snapshots from official external providers on a
  daily schedule.
- Saving unmodified raw files alongside their SHA-256 checksums and UTC
  retrieval timestamps.
- Assembling dated archival packages that match the Layer-1 archive structure.
- Submitting those packages to the archive via Pull Request.

---

## 2. Repository Boundaries

### What this repository does

| Activity | Description |
|----------|-------------|
| **Automated source retrieval** | HTTP GET requests to official APIs; raw bytes saved verbatim |
| **Checksum computation** | SHA-256 over raw bytes for every source file |
| **Timestamp recording** | UTC ISO-8601 retrieval time per source |
| **Archival package assembly** | `observation.json` + `raw_sources.json` + `raw/` directory |
| **Pull Request submission** | Opens a dated PR to the Layer-1 archive for human review |

### What this repository must never do

| Prohibited Activity | Reason |
|--------------------|--------|
| Scientific analysis or interpretation | Out of scope; belongs to the analysis layer |
| Modification of raw source data | Archives must contain unmodified originals |
| Direct commits to the Layer-1 archive | Violates the append-only, PR-reviewed invariant |
| Force-pushing to archive branches | Would bypass human review |
| Introducing automation into the archive repo | Architecture rule: archive is passive |

---

## 3. Upstream Dependencies

All data must originate from **official external providers only**. No third-party
intermediaries, mirrors, or derived datasets may be used as primary sources.

| Provider | Base URL | Data type |
|----------|----------|-----------|
| IAU Minor Planet Center (MPC) | `https://www.minorplanetcenter.net/` | Astrometric observations |
| NASA JPL Small-Body Database (SBDB) | `https://ssd-api.jpl.nasa.gov/` | Orbital elements, physical parameters |
| NASA JPL Horizons | `https://ssd.jpl.nasa.gov/` | Ephemeris data |
| ESA NEOCC | `https://neo.ssa.esa.int/` | ESA observation catalogue |
| NASA CNEOS | `https://cneos.jpl.nasa.gov/` | Close-approach and scout data |
| NASA PDS Small Bodies Node | `https://pds-smallbodies.astro.umd.edu/` | Archival observational datasets |

---

## 4. Downstream Integration

### Layer-1 Archive

| Field | Value |
|-------|-------|
| **Repository** | `abdelkader-omran/AUTO-DZ-ACT-3I-ATLAS-DAILY` |
| **Integration method** | Pull Request (automated, opened by this monitoring repo) |
| **Branch pattern** | `ingest/3i-atlas-YYYY-MM-DD` |
| **Base branch** | `main` |
| **Merge authority** | Human reviewer only |

The Layer-1 archive is **append-only**. Once a daily package is merged, it is
never modified or deleted. The monitoring repository must never commit to the
archive directly.

### Analysis Layer

| Field | Value |
|-------|-------|
| **Repository** | `abdelkader-omran/AUTO-DZ-ACT-ANALYSIS-3I-ATLAS` |
| **Integration method** | Reads from the Layer-1 archive |
| **Responsibility** | Scientific analysis and interpretation of archived raw data |

The analysis layer has no write relationship with this monitoring repository.
It consumes the output of the archive, not of the monitoring layer directly.

---

## 5. Architecture Position

The three repositories form a strict linear pipeline:

```
External Providers
  (MPC, JPL SBDB, JPL Horizons, ESA NEOCC, CNEOS, NASA PDS SBN)
        │
        │  HTTP GET (official APIs)
        ▼
┌────────────────────────────────────────────────────┐
│  MONITORING LAYER                                  │
│  trizel-ai/Auto-dz-api-monitor          ◄── HERE  │
│                                                    │
│  Runs:  daily GitHub Actions workflow              │
│  Does:  fetch → checksum → package → PR            │
│  Out:   PR to Layer-1 archive                      │
└──────────────────────┬─────────────────────────────┘
                       │  Pull Requests only
                       │  (human review required)
                       ▼
┌────────────────────────────────────────────────────┐
│  LAYER-1 ARCHIVE (append-only)                     │
│  abdelkader-omran/AUTO-DZ-ACT-3I-ATLAS-DAILY       │
│                                                    │
│  Stores: observations/YYYY-MM-DD/                  │
│            observation.json                        │
│            raw_sources.json                        │
│            raw/<source-files>                      │
│  Rules:  no automation; passive; human-merged PRs  │
└──────────────────────┬─────────────────────────────┘
                       │  read-only consumption
                       ▼
┌────────────────────────────────────────────────────┐
│  ANALYSIS LAYER                                    │
│  abdelkader-omran/AUTO-DZ-ACT-ANALYSIS-3I-ATLAS    │
│                                                    │
│  Does:  scientific analysis and interpretation     │
│  In:    archived raw packages from Layer-1         │
└────────────────────────────────────────────────────┘
```

### Layer summary

| Layer | Repository | Role | Automation |
|-------|-----------|------|-----------|
| Monitoring | `trizel-ai/Auto-dz-api-monitor` | Source retrieval, packaging, PR submission | ✅ Full automation |
| Archive | `abdelkader-omran/AUTO-DZ-ACT-3I-ATLAS-DAILY` | Append-only raw data archive | ❌ None (passive) |
| Analysis | `abdelkader-omran/AUTO-DZ-ACT-ANALYSIS-3I-ATLAS` | Scientific analysis | Independent |

---

## 6. Operational Rule

### Archive updates are PR-only and reviewable

This rule is absolute and applies to all automation in this repository:

1. The monitoring workflow **must not** push directly to any branch of the
   Layer-1 archive repository.
2. Every ingestion run **must** submit its package through a Pull Request.
3. The PR **must** target the `main` branch of the archive.
4. The PR **must** be reviewed by a human before being merged.
5. Once merged, the package **must not** be modified or removed (append-only).
6. The monitoring branch created for the PR (`ingest/3i-atlas-YYYY-MM-DD`) is
   retained after merge to provide a permanent audit trail.

This operational rule ensures that the archive remains a trustworthy, traceable,
and human-verified record of raw observation data.

---

## Document Maintenance

This document should be updated whenever:

- A new data source is added to or removed from the ingestion pipeline.
- The archive or analysis repository names or branches change.
- The workflow schedule or PR submission logic changes.
- Any new layer is introduced into the TRIZEL pipeline.

_Last updated: 2026-03-17_
