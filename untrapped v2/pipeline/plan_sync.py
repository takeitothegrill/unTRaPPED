#!/usr/bin/env python3
"""unTRaPPED V2 — sync planner.

Reads locations.csv and processed/, and works out what needs to happen to
bring the My Maps map up to date. This does NOT talk to Google — there's no
API for My Maps, so pushing the actual changes means a live Claude Code
session driving the browser by hand, following pipeline/RUNBOOK.md. This
script's job is just to compute and print the work list precisely, so nothing
gets missed or double-handled.

A row is:
  - NEW    if status is blank and processed/<location_id>/ exists.
  - UPDATE if status == "update" and processed/<location_id>/ exists.
  - SKIP   if status == "done" (nothing changed), or no processed folder
           exists yet (run process_locations.py first).

For UPDATE rows, diffs the current processed/<location_id>/ file list
against the synced_photos column to report which photos are newly added
(need attaching) and which were removed (need removing from the pin).

This script NEVER writes to locations.csv. Marking a row done -- setting
status=done and filling synced_photos -- is a manual edit, RUNBOOK.md step 6.
Earlier docs claimed a script did it; none ever has.

Usage:
    python plan_sync.py
"""
import csv
import sys
from pathlib import Path

from categories import normalize_category, normalize_rating, icon_key

ROOT = Path(__file__).resolve().parent.parent
LOCATIONS_CSV = ROOT / "locations.csv"
PROCESSED_DIR = ROOT / "processed"
MERGE_CSV = ROOT / "merge.csv"

# Columns written to merge.csv. latitude/longitude are deliberately ABSENT and
# must stay absent: including them in a "Reimport and merge" destroyed every
# pin on the test map (see pipeline-test-artifacts/STATUS.md). This tuple is
# the enforcement point -- do not add them here.
MERGE_COLUMNS = ("location_id", "name", "description", "category", "rating", "icon")


def load_locations():
    if not LOCATIONS_CSV.exists():
        print(f"ERROR: {LOCATIONS_CSV} not found.")
        sys.exit(1)
    with open(LOCATIONS_CSV, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def plan():
    rows = load_locations()
    new_work, update_work, skipped, blocked = [], [], [], []

    for row in rows:
        loc_id = row["location_id"].strip()
        status = (row.get("status") or "").strip().lower()
        folder = PROCESSED_DIR / loc_id

        if status == "done":
            skipped.append(loc_id)
            continue
        if not folder.is_dir():
            blocked.append((loc_id, "no processed/ folder — run process_locations.py first"))
            continue
        if not row.get("latitude") or not row.get("longitude"):
            blocked.append((loc_id, "no latitude/longitude — process_locations.py couldn't place it"))
            continue

        photos = sorted(p.name for p in folder.iterdir() if p.suffix.lower() == ".jpg")
        if not photos:
            blocked.append((loc_id, "processed/ folder exists but has no .jpg files"))
            continue

        cat_id, cat_name = normalize_category(row.get("category"))
        rating = normalize_rating(row.get("rating"))

        item = {
            "location_id": loc_id,
            "name": row.get("name", ""),
            "description": row.get("description", ""),
            "category_id": cat_id,
            "category_name": cat_name or row.get("category"),
            "rating": rating or row.get("rating"),
            "latitude": row["latitude"],
            "longitude": row["longitude"],
            "icon": icon_key(row.get("category"), row.get("rating")),
            "hero_photo": photos[0],
            "extra_photos": photos[1:],
            "all_photos": photos,
        }

        if status == "update":
            prev = set(x for x in (row.get("synced_photos") or "").split(",") if x)
            now = set(photos)
            item["photos_to_add"] = sorted(now - prev)
            item["photos_to_remove"] = sorted(prev - now)
            update_work.append(item)
        else:
            new_work.append(item)

    return new_work, update_work, skipped, blocked


def print_plan(new_work, update_work, skipped, blocked):
    print("=" * 70)
    print(f"NEW locations to add to the map: {len(new_work)}")
    for item in new_work:
        print(f"\n  [{item['location_id']}]")
        print(f"    name: {item['name']}")
        print(f"    category: {item['category_name']} (id {item['category_id']})   rating: {item['rating']}")
        print(f"    map icon: {item['icon']}")
        print(f"    position: {item['latitude']}, {item['longitude']}")
        print(f"    hero photo (Pass 1, creates the pin): {item['hero_photo']}")
        if item["extra_photos"]:
            print(f"    extra photos to attach after (Pass 2): {item['extra_photos']}")

    print(f"\nUPDATE (status=update) locations: {len(update_work)}")
    for item in update_work:
        print(f"\n  [{item['location_id']}]")
        print(f"    re-push name/description/category/rating (merge CSV, no lat/lon)")
        if item["photos_to_add"]:
            print(f"    photos to ATTACH: {item['photos_to_add']}")
        if item["photos_to_remove"]:
            print(f"    photos to REMOVE from pin: {item['photos_to_remove']}")
        if not item["photos_to_add"] and not item["photos_to_remove"]:
            print(f"    (no photo changes — text/category/rating only)")

    if blocked:
        print(f"\nBLOCKED (needs attention before syncing): {len(blocked)}")
        for loc_id, reason in blocked:
            print(f"  [{loc_id}] {reason}")

    print(f"\nAlready done, nothing to do: {len(skipped)}  {skipped}")
    print("=" * 70)
    print("\nTo execute this plan, see pipeline/RUNBOOK.md.")


def _only_arg():
    """Return the value of --only <location_id>, or None."""
    if "--only" not in sys.argv:
        return None
    i = sys.argv.index("--only")
    if i + 1 >= len(sys.argv):
        print("ERROR: --only needs a location_id")
        sys.exit(1)
    return sys.argv[i + 1]


def write_merge_csv(new_work, update_work, only=None):
    """Write the CSV used by My Maps' Reimport and merge step.

    Covers NEW and UPDATE rows together -- merging is keyed on location_id, so
    a row that is already on the map is simply updated in place.
    """
    rows = new_work + update_work
    if only:
        rows = [r for r in rows if r["location_id"] == only]
        if not rows:
            print(f"ERROR: --only {only!r} matched no NEW or UPDATE row.")
            sys.exit(1)
    if not rows:
        print("\nNothing to merge — merge.csv not written.")
        return

    missing = [r["location_id"] for r in rows if not r["icon"]]
    if missing:
        print("\nERROR: these rows have an unrecognised category/rating, so no "
              "icon could be chosen. Fix locations.csv first:")
        for loc_id in missing:
            print(f"  [{loc_id}]")
        sys.exit(1)

    assert "latitude" not in MERGE_COLUMNS and "longitude" not in MERGE_COLUMNS,         "merge.csv must never carry coordinates — it wipes the pins"

    with open(MERGE_CSV, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(MERGE_COLUMNS))
        w.writeheader()
        for item in rows:
            w.writerow({
                "location_id": item["location_id"],
                "name": item["name"],
                "description": item["description"],
                "category": item["category_name"],
                "rating": item["rating"],
                "icon": item["icon"],
            })

    icons = sorted({r["icon"] for r in rows})
    print(f"\nWrote {MERGE_CSV} — {len(rows)} rows, no coordinates.")
    print("  NOTE: rows whose location_id is not already a pin on the map are")
    print("  silently ignored by the merge — no error, no warning. Use --only")
    print("  <location_id> to scope this file when that ambiguity matters.")
    print(f"  style the layer by the 'icon' column (Categories mode). "
          f"Values present: {', '.join(icons)}")


if __name__ == "__main__":
    n, u, sk, b = plan()
    print_plan(n, u, sk, b)
    if "--write-merge-csv" in sys.argv:
        write_merge_csv(n, u, only=_only_arg())
    else:
        print("\nRe-run with --write-merge-csv to generate merge.csv.")
