#!/usr/bin/env python3
"""
Build the static dataset used by the Exoplanet Bestiary.

Default mode is COMPACT and downloads only the columns used by the website.
This is much faster than `select * from pscomppars`.

Use:
    python3 update_exoplanets.py

If you really want every PSCompPars column:
    python3 update_exoplanets.py --full

No third-party packages are required.
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import shutil
import sys
import urllib.parse
import urllib.request
from pathlib import Path

NASA_TAP = "https://exoplanetarchive.ipac.caltech.edu/TAP/sync"

# Everything currently used by the catalogue, system view, sonification
# and scientific-information panel.
COMPACT_COLUMNS = [
    "pl_name",
    "hostname",
    "sy_pnum",
    "discoverymethod",
    "disc_year",
    "disc_facility",
    "pl_orbper",
    "pl_orbsmax",
    "pl_orbeccen",
    "pl_orbincl",
    "pl_bmasse",
    "pl_bmassj",
    "pl_rade",
    "pl_radj",
    "pl_dens",
    "pl_eqt",
    "pl_insol",
    "st_spectype",
    "st_teff",
    "st_rad",
    "st_mass",
    "st_met",
    "st_logg",
    "sy_dist",
    "ra",
    "dec",
    "pl_ntranspec",
    "pl_ndispec",
    "pl_nespec",
]

HERE = Path(__file__).resolve().parent
DATA_DIR = HERE / "data"

STAR_KEYS = [
    "st_spectype", "st_teff", "st_rad", "st_mass", "st_met", "sy_dist"
]
MIN_PLANET_KEYS = [
    "pl_name", "pl_orbper", "pl_orbsmax", "pl_orbeccen"
]


def make_query(full: bool) -> str:
    if full:
        return "select * from pscomppars"
    return "select " + ",".join(COMPACT_COLUMNS) + " from pscomppars"


def download_rows(query: str, full: bool) -> list[dict]:
    url = NASA_TAP + "?" + urllib.parse.urlencode({
        "query": query,
        "format": "json",
    })

    mode = "FULL" if full else "COMPACT"
    print(f"Downloading NASA PSCompPars ({mode} mode)…")
    if not full:
        print(f"Only {len(COMPACT_COLUMNS)} useful columns are requested.")

    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "ExoplanetBestiaryStaticUpdater/1.1",
            "Accept": "application/json",
        },
    )

    with urllib.request.urlopen(req, timeout=300) as response:
        content_length = response.headers.get("Content-Length")
        if content_length:
            mb = int(content_length) / 1024 / 1024
            print(f"NASA response size: about {mb:.1f} MiB")
        rows = json.load(response)

    if not isinstance(rows, list) or not rows:
        raise RuntimeError("NASA returned no PSCompPars rows.")

    print(f"Downloaded {len(rows):,} confirmed planets.")
    return rows


def best_star_row(planets: list[dict]) -> dict:
    return max(
        planets,
        key=lambda row: sum(row.get(key) not in (None, "") for key in STAR_KEYS),
    )


def write_snapshot(rows: list[dict], query: str, full: bool) -> None:
    groups: dict[str, list[dict]] = {}

    for row in rows:
        hostname = row.get("hostname") or "Unknown host"
        groups.setdefault(hostname, []).append(row)

    tmp = HERE / ".data_tmp"
    if tmp.exists():
        shutil.rmtree(tmp)
    (tmp / "systems").mkdir(parents=True)

    systems = []

    for hostname, planets in sorted(groups.items(), key=lambda kv: kv[0].casefold()):
        planets.sort(
            key=lambda row: (
                row.get("pl_orbper") is None,
                row.get("pl_orbper") or 1e99,
            )
        )

        file_id = hashlib.sha1(hostname.encode("utf-8")).hexdigest()[:16]
        relative_file = f"systems/{file_id}.json"

        rep = best_star_row(planets)
        summary_planets = []

        for planet in planets:
            summary = {key: planet.get(key) for key in MIN_PLANET_KEYS}
            summary["st_mass"] = planet.get("st_mass")
            summary_planets.append(summary)

        known_count = max(
            [int(row.get("sy_pnum") or 0) for row in planets] + [len(planets)]
        )

        systems.append({
            "hostname": hostname,
            "n": known_count,
            "rep": {
                key: rep.get(key)
                for key in ["hostname", "sy_pnum", *STAR_KEYS]
            },
            "planets": summary_planets,
            "file": relative_file,
        })

        (tmp / "systems" / f"{file_id}.json").write_text(
            json.dumps(
                {"hostname": hostname, "planets": planets},
                ensure_ascii=False,
                separators=(",", ":"),
                allow_nan=False,
            ),
            encoding="utf-8",
        )

    meta = {
        "source": "NASA Exoplanet Archive",
        "table": "PSCompPars",
        "mode": "full" if full else "compact",
        "columns": "*" if full else COMPACT_COLUMNS,
        "query": query,
        "generated_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
        "planet_count": len(rows),
        "system_count": len(systems),
    }

    (tmp / "index.json").write_text(
        json.dumps(
            {"meta": meta, "systems": systems},
            ensure_ascii=False,
            separators=(",", ":"),
            allow_nan=False,
        ),
        encoding="utf-8",
    )

    if DATA_DIR.exists():
        shutil.rmtree(DATA_DIR)
    tmp.rename(DATA_DIR)

    total_bytes = sum(p.stat().st_size for p in DATA_DIR.rglob("*.json"))
    print(f"Wrote {len(systems):,} systems.")
    print(f"Static JSON size: {total_bytes / 1024 / 1024:.1f} MiB")
    print(f"Index: {DATA_DIR / 'index.json'}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--full",
        action="store_true",
        help="Download every PSCompPars column. Much slower and usually unnecessary.",
    )
    args = parser.parse_args()

    query = make_query(args.full)

    try:
        rows = download_rows(query, args.full)
        write_snapshot(rows, query, args.full)
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
