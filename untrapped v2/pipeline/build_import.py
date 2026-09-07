#!/usr/bin/env python3
"""unTRaPPED V2 — build the per-LGA, per-layer CSVs that get imported into
Google My Maps.

This replaces the old photo-import-then-merge approach for POSITIONING. Google
places pins at the exact latitude/longitude in an imported CSV, so locations.csv
is the source of truth for where a pin sits. (Photo EXIF is still how those
coordinates get *discovered* in the first place — process_locations.py backfills
blank cells — but once a coordinate is in the CSV, the CSV wins.)

Output shape:

    import/<lga>/PARKING (disability sticker).csv
    import/<lga>/TOILETS (disability).csv
    import/<lga>/PATHWAYS and ROUTES.csv
    import/<lga>/VENUES and AMENITIES.csv

One file per map layer. Four layers per map, one map per LGA.

ORDERING MATTERS. The My Maps legend lists pins in the order they were
imported, NOT alphabetically — confirmed on the v7 test map. So rows are sorted
by `name` here, and because names are formatted "TOWNSHIP | TYPE - descriptor
[RATING]" that groups the legend by township, then by type. Change the sort and
you change what the public sees.

Usage:
    python build_import.py
"""
import csv
import sys
from collections import defaultdict
from pathlib import Path

from categories import MAP_ICON, normalize_category, normalize_rating

ROOT = Path(__file__).resolve().parent.parent
LOCATIONS_CSV = ROOT / "locations.csv"
IMPORT_DIR = ROOT / "import"

# icon family -> layer name, in the order layers should be created on the map
# Layer names as they appear in the public legend. "Pathways and Routes" leads
# with the concrete word people recognise while covering ramps, doors and lifts.
# "Venues and Amenities" is one layer by design -- see the Amenities note in
# categories.py. NOTE: spell out "and" -- never "&" -- in layer names, because
# the layer name becomes the import FILENAME and "&" is a shell/URL hazard.
# categories.py.
# These strings are the layer names the public sees AND the import filenames,
# so they must match the live map exactly. Never use "&" -- spell out "and".
LAYERS = [("parking", "PARKING (disability sticker)"),
          ("toilet",  "TOILETS (disability)"),
          ("route",   "PATHWAYS and ROUTES"),
          ("venue",   "VENUES and AMENITIES")]

# Columns written to each import file. latitude/longitude are REQUIRED here —
# unlike merge.csv, where they are forbidden. Different mechanism entirely:
# an import CREATES pins at these coordinates; a merge UPDATES existing pins
# and including coordinates there destroyed the map.
COLUMNS = ["name", "description", "latitude", "longitude",
           "location_id", "township", "lga", "category", "rating", "icon"]


def compose_description(row):
    """Prefix the description with a searchable location line.

    The published viewer's search box matches DESCRIPTION text as well as pin
    names, and surfaces this map's pins above general Google places. So putting
    the place, street and township at the top of every description means a user
    searching "Lioness Park" gets the toilet, the ramp, the parking and the
    pathway together — which is the actual task, and no amount of legend
    tuning achieves it.

    Format: "[place name - if any], <address>, <township>"
    Empty parts are dropped, so a location with no place name still works.
    """
    parts = [(row.get("place_name") or "").strip(),
             (row.get("street_address") or "").strip(),
             (row.get("township") or "").strip()]
    header = ", ".join(p for p in parts if p)
    body = (row.get("description") or "").strip()
    if not header:
        return body
    return header + "\n\n" + body if body else header


def load():
    if not LOCATIONS_CSV.exists():
        sys.exit(f"ERROR: {LOCATIONS_CSV} not found.")
    with open(LOCATIONS_CSV, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def build():
    rows = load()
    buckets = defaultdict(list)
    problems = []

    for r in rows:
        loc_id = r["location_id"].strip()
        cat_id, _ = normalize_category(r.get("category"))
        rating = normalize_rating(r.get("rating"))
        lga = (r.get("lga") or "").strip()

        if cat_id is None:
            problems.append(f"{loc_id}: unrecognised category {r.get('category')!r}")
            continue
        if rating is None:
            problems.append(f"{loc_id}: unrecognised rating {r.get('rating')!r}")
            continue
        if not lga:
            problems.append(f"{loc_id}: no lga set")
            continue
        if not r.get("latitude") or not r.get("longitude"):
            problems.append(f"{loc_id}: no coordinates — run process_locations.py")
            continue

        family = MAP_ICON[cat_id]
        buckets[(lga, family)].append({
            "name": r["name"],
            "description": compose_description(r),
            "latitude": r["latitude"],
            "longitude": r["longitude"],
            "location_id": loc_id,
            "township": (r.get("township") or "").strip(),
            "lga": lga,
            "category": r["category"],
            "rating": rating,
            "icon": f"{family}-{rating}",
        })

    if problems:
        print("PROBLEMS — these rows were skipped:")
        for p in problems:
            print(f"  {p}")
        print()

    written = []
    for (lga, family), items in sorted(buckets.items()):
        # legend order == import order, so sort deliberately
        items.sort(key=lambda i: i["name"])
        layer = dict(LAYERS)[family]
        d = IMPORT_DIR / lga.lower()
        d.mkdir(parents=True, exist_ok=True)
        path = d / f"{layer}.csv"
        with open(path, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=COLUMNS)
            w.writeheader()
            w.writerows(items)
        written.append((lga, layer, path, items))

    by_lga = defaultdict(list)
    for lga, layer, path, items in written:
        by_lga[lga].append((layer, path, items))

    for lga in sorted(by_lga):
        entries = by_lga[lga]
        total = sum(len(i) for _, _, i in entries)
        print(f"{lga}  —  {len(entries)} layers, {total} pins")
        order = [name for _, name in LAYERS]
        entries.sort(key=lambda e: order.index(e[0]))
        for layer, path, items in entries:
            icons = sorted({i["icon"] for i in items})
            print(f"  {layer:9} {len(items):2} pins   {path.relative_to(ROOT)}")
            for i in items:
                print(f"       {i['name']}")
            print(f"       icons needed: {', '.join(icons)}")
        print()

    print("Import each file as its OWN layer, in the order listed above.")
    print("Leave every layer on 'Individual styles' — grouping by a column")
    print("collapses the per-pin legend, which is the whole point of this shape.")


if __name__ == "__main__":
    build()
