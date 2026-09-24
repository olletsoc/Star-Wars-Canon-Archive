#!/usr/bin/env python3
"""
Build data.json from data.csv for the Star Wars Canon Media Chronology.

Usage:
    python3 build.py            # reads ./data.csv, writes ./data.json

data.csv columns (this is the source of truth you hand-edit):
    y     integer sort key — years relative to the Battle of Yavin.
          Negative = BBY (before), positive/zero = ABY (after). e.g. -382, 9, 34
    disp  human-readable date label shown on the card. e.g. "382 BBY", "9 ABY"
    f     format code: F, N, JR, YR, VG, TV, C, SS, A, RPG, P
    t     title (may contain <em>...</em> for italics)
    rel   real-world release date (YYYY-MM-DD, or blank if unknown/unreleased)
    note  optional note shown on the card (or blank)
    url   optional link to the media (blank if none yet)

The "era" field in data.json is DERIVED from y — do not store it in the CSV.
Change a row's y and rebuild, and its era updates automatically.
"""

import csv
import json
import os
from collections import Counter

ERA_ORDER = ["dawn", "highrepublic", "fall", "reign",
             "rebellion", "newrepublic", "firstorder", "beyond"]


def era_of(y):
    """Map an in-universe year (BBY negative / ABY positive) to an era id."""
    if y <= -500:
        return "dawn"
    if y <= -100:
        return "highrepublic"
    if y <= -19:
        return "fall"
    if y < 0:
        return "reign"
    if y <= 4:
        return "rebellion"
    if y < 34:
        return "newrepublic"
    if y <= 35:
        return "firstorder"
    return "beyond"


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "data.csv")
    out = os.path.join(here, "data.json")

    rows = []
    with open(src, newline="", encoding="utf-8") as f:
        for lineno, r in enumerate(csv.DictReader(f), start=2):
            title = (r.get("t") or "").strip()
            y_raw = (r.get("y") or "").strip()
            if not title or not y_raw:
                continue  # skip blank/incomplete rows
            try:
                y = int(y_raw)
            except ValueError:
                raise SystemExit(f"data.csv line {lineno}: y must be an integer, got {y_raw!r}")
            rel = (r.get("rel") or "").strip()
            note = (r.get("note") or "").strip()
            url = (r.get("url") or "").strip()
            rows.append({
                "era": era_of(y),
                "f": (r.get("f") or "").strip(),
                "t": title,
                "disp": (r.get("disp") or "").strip() or "—",
                "y": y,
                "rel": rel or None,
                "note": note or None,
                "url": url or None,
            })

    def enc(v):
        return "null" if v is None else json.dumps(v, ensure_ascii=False)

    lines = [
        '  {"era":%s,"f":%s,"t":%s,"disp":%s,"y":%d,"rel":%s,"note":%s,"url":%s}' % (
            json.dumps(o["era"], ensure_ascii=False),
            json.dumps(o["f"], ensure_ascii=False),
            json.dumps(o["t"], ensure_ascii=False),
            json.dumps(o["disp"], ensure_ascii=False),
            o["y"],
            enc(o["rel"]),
            enc(o["note"]),
            enc(o["url"]),
        )
        for o in rows
    ]

    with open(out, "w", encoding="utf-8") as f:
        f.write("[\n" + ",\n".join(lines) + "\n]\n")

    tally = Counter(o["era"] for o in rows)
    print(f"Wrote {len(rows)} records to {out}")
    for k in ERA_ORDER:
        if tally.get(k):
            print(f"  {k:<13} {tally[k]}")


if __name__ == "__main__":
    main()
