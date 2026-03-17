# Auto-dz-api-monitor

**TRIZEL-AI — Monitoring Repository**
Live Scientific API Monitoring using AUTO DZ ACT

---

## Purpose

This repository performs **automated source retrieval and archival package preparation** for the interstellar object **3I-ATLAS**.

It is the **monitoring layer** of the TRIZEL architecture: it fetches raw observation snapshots from official external providers, computes SHA-256 checksums for traceability, and assembles dated archival packages ready for review and inclusion in the Layer-1 archive.

---

## Repository Boundaries

| Allowed | Not Allowed |
|---------|-------------|
| Automated source retrieval | Scientific analysis or interpretation |
| SHA-256 checksum computation | Direct commits to the Layer-1 archive |
| Archival package preparation | Any modification of raw source data |
| Opening Pull Requests to the archive | Force-pushing or bypassing review |

---

## Architecture Position

```
┌─────────────────────────────────────────────┐
│  MONITORING LAYER                           │
│  trizel-ai/Auto-dz-api-monitor  ◄── (this) │
│                                             │
│  • fetches raw observations                 │
│  • computes checksums                       │
│  • prepares archival packages               │
│  • opens PRs to Layer-1 archive             │
└──────────────────┬──────────────────────────┘
                   │  Pull Requests only
                   ▼
┌─────────────────────────────────────────────┐
│  LAYER-1 ARCHIVE (append-only)              │
│  abdelkader-omran/AUTO-DZ-ACT-3I-ATLAS-DAILY│
│                                             │
│  • passive, human-reviewed archive          │
│  • no automation runs here                  │
└──────────────────┬──────────────────────────┘
                   │  source data consumed by
                   ▼
┌─────────────────────────────────────────────┐
│  ANALYSIS LAYER                             │
│  abdelkader-omran/                          │
│    AUTO-DZ-ACT-ANALYSIS-3I-ATLAS            │
│                                             │
│  • scientific analysis                      │
│  • interpretation                           │
└─────────────────────────────────────────────┘
```

---

## Upstream Dependencies

All data comes exclusively from **official external providers**:

| Provider | Role |
|----------|------|
| IAU Minor Planet Center (MPC) | Astrometric observations |
| NASA JPL Small-Body Database (SBDB) | Orbital elements and physical parameters |
| NASA JPL Horizons | Ephemeris data |
| ESA Near-Earth Object Coordination Centre (NEOCC) | ESA observation catalogue |
| NASA Center for Near Earth Object Studies (CNEOS) | Close-approach and scout data |
| NASA PDS Small Bodies Node | Archival observational datasets |

No third-party intermediaries or derived datasets are used as primary sources.

---

## Downstream Integration

| Destination | Method | Purpose |
|-------------|--------|---------|
| `abdelkader-omran/AUTO-DZ-ACT-3I-ATLAS-DAILY` | Pull Request | Append daily observation packages to the Layer-1 archive |
| `abdelkader-omran/AUTO-DZ-ACT-ANALYSIS-3I-ATLAS` | Reads from archive | Scientific analysis consumes the archived packages |

---

## Operational Rule

> **Archive updates are PR-only and reviewable.**

The monitoring workflow never commits directly to the Layer-1 archive. Every daily ingestion run opens a Pull Request to `abdelkader-omran/AUTO-DZ-ACT-3I-ATLAS-DAILY`. No package is merged into the archive without human review.

---

## Further Reading

- [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) — Detailed TRIZEL architecture coordination reference
- [`docs/GOVERNANCE_REFERENCE.md`](docs/GOVERNANCE_REFERENCE.md) — Governance framework pointer
- [`src/ingest_3i_atlas.py`](src/ingest_3i_atlas.py) — Ingestion pipeline implementation
- [`.github/workflows/3i-atlas-ingestion.yml`](.github/workflows/3i-atlas-ingestion.yml) — Daily automation workflow
