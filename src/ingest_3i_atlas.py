"""
ingest_3i_atlas.py — Monitoring ingestion pipeline for interstellar object 3I-ATLAS.

Fetches raw observation snapshots from official data providers, computes SHA-256
checksums, records retrieval timestamps, and assembles archival packages matching
the Layer-1 structure expected by abdelkader-omran/AUTO-DZ-ACT-3I-ATLAS-DAILY.
"""

import hashlib
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

import requests

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

OBJECT_NAME = "3I-ATLAS"

# Output directory structure mirrors Layer-1 archive layout
OUTPUT_BASE = Path(os.environ.get("INGEST_OUTPUT_DIR", "output"))

# Request timeout (seconds) applied to every HTTP call
HTTP_TIMEOUT = 30

# ---------------------------------------------------------------------------
# Data sources
# ---------------------------------------------------------------------------

SOURCES = [
    {
        "source_name": "IAU Minor Planet Center (MPC)",
        "source_url": (
            "https://www.minorplanetcenter.net/db_search/show_object"
            "?object_id=3I-ATLAS&json=1"
        ),
        "raw_filename": "mpc_3i_atlas.json",
    },
    {
        "source_name": "NASA JPL Small-Body Database (SBDB)",
        "source_url": (
            "https://ssd-api.jpl.nasa.gov/sbdb.api?sstr=3I-ATLAS&full-prec=1"
        ),
        "raw_filename": "jpl_sbdb_3i_atlas.json",
    },
    {
        "source_name": "NASA JPL Horizons",
        "source_url": (
            "https://ssd.jpl.nasa.gov/api/horizons.api"
            "?format=json"
            "&COMMAND='3I-ATLAS'"
            "&OBJ_DATA='YES'"
            "&MAKE_EPHEM='NO'"
        ),
        "raw_filename": "jpl_horizons_3i_atlas.json",
    },
    {
        "source_name": "ESA Near-Earth Object Coordination Centre (NEOCC)",
        "source_url": (
            "https://neo.ssa.esa.int/search-for-neos"
            "?designation=3I-ATLAS&output=json"
        ),
        "raw_filename": "esa_neocc_3i_atlas.json",
    },
    {
        "source_name": "NASA Center for Near Earth Object Studies (CNEOS)",
        "source_url": (
            "https://cneos.jpl.nasa.gov/scout/data.php"
            "?tdes=3I-ATLAS"
        ),
        "raw_filename": "cneos_3i_atlas.json",
    },
    {
        "source_name": "NASA PDS Small Bodies Node",
        "source_url": (
            "https://pds-smallbodies.astro.umd.edu/data_sb/resources/"
            "3I-ATLAS/index.shtml"
        ),
        "raw_filename": "pds_sbn_3i_atlas.html",
    },
]

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def utc_now_iso() -> str:
    """Return the current UTC time as an ISO-8601 string."""
    return datetime.now(timezone.utc).isoformat()


def sha256_of_bytes(data: bytes) -> str:
    """Compute and return the hex-encoded SHA-256 digest of *data*."""
    return hashlib.sha256(data).hexdigest()


def fetch_source(source: dict, raw_dir: Path) -> dict:
    """
    Fetch one data source, persist the raw bytes to *raw_dir*, and return a
    manifest entry.  Network errors are captured so the overall run continues.
    """
    name = source["source_name"]
    url = source["source_url"]
    raw_filename = source["raw_filename"]
    raw_path = raw_dir / raw_filename

    retrieval_time = utc_now_iso()
    status = "ok"
    sha256 = None
    error_detail = None

    print(f"  Fetching: {name}")
    print(f"    URL: {url}")

    try:
        response = requests.get(url, timeout=HTTP_TIMEOUT)
        raw_bytes = response.content

        # Persist unmodified raw bytes regardless of HTTP status so that
        # even error responses (e.g. 404 with a body) are preserved.
        raw_path.write_bytes(raw_bytes)
        sha256 = sha256_of_bytes(raw_bytes)

        if response.status_code != 200:
            status = f"http_{response.status_code}"
            print(f"    ⚠  HTTP {response.status_code} — raw response saved.")
        else:
            print(f"    ✓  {len(raw_bytes)} bytes — SHA-256: {sha256[:16]}…")

    except requests.exceptions.Timeout:
        status = "fetch_error"
        error_detail = f"Request timed out after {HTTP_TIMEOUT}s"
        print(f"    ✗  Timeout after {HTTP_TIMEOUT}s")
        raw_path.write_bytes(b"")
        sha256 = sha256_of_bytes(b"")

    except requests.exceptions.RequestException as exc:
        status = "fetch_error"
        error_detail = str(exc)
        print(f"    ✗  Fetch error: {exc}")
        # Write an empty placeholder so the path always exists in the package
        raw_path.write_bytes(b"")
        sha256 = sha256_of_bytes(b"")

    entry = {
        "source_name": name,
        "source_url": url,
        "raw_path": str(raw_path.relative_to(OUTPUT_BASE)),
        "sha256": sha256,
        "retrieval_time_utc": retrieval_time,
        "status": status,
    }
    if error_detail:
        entry["error_detail"] = error_detail

    return entry


# ---------------------------------------------------------------------------
# Main pipeline
# ---------------------------------------------------------------------------


def run_ingestion() -> Path:
    """
    Execute the full ingestion pipeline and return the path to the dated
    observation directory that was created.
    """
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    obs_dir = OUTPUT_BASE / "observations" / today
    raw_dir = obs_dir / "raw"
    raw_dir.mkdir(parents=True, exist_ok=True)

    print(f"\n{'='*60}")
    print(f"  3I-ATLAS Monitoring Ingestion Pipeline")
    print(f"  Date : {today}")
    print(f"  Out  : {obs_dir}")
    print(f"{'='*60}\n")

    # ------------------------------------------------------------------
    # 1. Fetch all sources
    # ------------------------------------------------------------------
    manifest_entries = []
    for source in SOURCES:
        entry = fetch_source(source, raw_dir)
        manifest_entries.append(entry)

    # ------------------------------------------------------------------
    # 2. Write raw_sources.json (source manifest)
    # ------------------------------------------------------------------
    raw_sources_path = obs_dir / "raw_sources.json"
    raw_sources_path.write_text(
        json.dumps(manifest_entries, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    print(f"\n  ✓  raw_sources.json written ({len(manifest_entries)} entries)")

    # ------------------------------------------------------------------
    # 3. Write observation.json (archival summary)
    # ------------------------------------------------------------------
    ingestion_time = utc_now_iso()
    success_count = sum(1 for e in manifest_entries if e["status"] == "ok")

    observation = {
        "object": OBJECT_NAME,
        "observation_date": today,
        "ingestion_time_utc": ingestion_time,
        "pipeline_version": "1.0.0",
        "sources_attempted": len(manifest_entries),
        "sources_succeeded": success_count,
        "sources": [
            {
                "source_name": e["source_name"],
                "source_url": e["source_url"],
                "raw_path": e["raw_path"],
                "sha256": e["sha256"],
                "retrieval_time_utc": e["retrieval_time_utc"],
                "status": e["status"],
            }
            for e in manifest_entries
        ],
    }

    obs_json_path = obs_dir / "observation.json"
    obs_json_path.write_text(
        json.dumps(observation, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    print(f"  ✓  observation.json written")
    print(
        f"\n  Pipeline complete: {success_count}/{len(manifest_entries)} sources OK\n"
    )

    return obs_dir


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    obs_dir = run_ingestion()
    print(f"Output directory: {obs_dir}")
    sys.exit(0)
