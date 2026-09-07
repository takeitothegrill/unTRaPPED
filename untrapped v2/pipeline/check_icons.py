#!/usr/bin/env python3
"""unTRaPPED V2 — which pins need their icon re-assigned by hand?

WHY THIS EXISTS
---------------
The map uses "Individual styles" so that every pin is listed and clickable in
the public legend. The price is that each pin's icon is assigned BY HAND through
the paint-can, and a `Reimport and merge` does NOT touch it.

So a rating change in the CSV updates the pin's DATA but leaves the old icon on
the map. The data says orange; the public sees green. This script finds those.

HOW IT WORKS
------------
Two baseline columns record what the MAP is believed to show:

    category_on_map, rating_on_map

The live columns `category` and `rating` are what the CSV says. When the icon
derived from the live pair differs from the icon derived from the baseline pair,
that pin needs a new icon.

WORKFLOW
--------
    python check_icons.py              # report what needs re-assigning
    ...assign those icons on the map...
    python check_icons.py --synced     # baseline := live, flags clear

Work through the report ICON BY ICON, not pin by pin — the paint-can keeps
previously-used icons under "Other icons", so a repeat assignment is
hover -> paint-can -> one click, with no dialogs.
"""
import csv
import sys
from collections import defaultdict
from pathlib import Path

from categories import MAP_ICON, normalize_category, normalize_rating

ROOT = Path(__file__).resolve().parent.parent
CSV_PATH = ROOT / "locations-from-v1-map.csv"
FLAG = "ICON OUT OF DATE"


def icon_for(category, rating):
    """Return the icon name for a category/rating pair, or None."""
    cat_id, _ = normalize_category(category)
    r = normalize_rating(rating)
    if cat_id is None or r is None:
        return None
    return f"{MAP_ICON[cat_id]}-{r}"


def load():
    if not CSV_PATH.exists():
        sys.exit(f"ERROR: {CSV_PATH} not found.")
    with open(CSV_PATH, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    if "rating_on_map" not in rows[0]:
        sys.exit("ERROR: no rating_on_map column — this CSV predates icon tracking.")
    return rows


def save(rows):
    with open(CSV_PATH, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)


def strip_flag(quality):
    parts = [p.strip() for p in (quality or "").split(";")]
    return "; ".join(p for p in parts if p and not p.startswith(FLAG))


def main():
    rows = load()
    synced = "--synced" in sys.argv
    stale, unresolvable = defaultdict(list), []

    for r in rows:
        want = icon_for(r.get("category"), r.get("rating"))
        have = icon_for(r.get("category_on_map"), r.get("rating_on_map"))
        r["quality"] = strip_flag(r.get("quality"))

        if want is None:
            # a Locator row, or a category/rating the vocabulary doesn't know
            if (r.get("category") or "").strip().lower() != "locator":
                unresolvable.append((r["location_id"], r.get("category"), r.get("rating")))
            continue

        if want != have:
            stale[want].append((r["location_id"], r["name"], have or "(none)"))
            note = f"{FLAG} - map shows '{have or 'none'}', data says '{want}'; re-assign on the map"
            r["quality"] = (r["quality"] + "; " + note) if r["quality"] else note

    if unresolvable:
        print("CANNOT DERIVE AN ICON — fix the category or rating first:")
        for lid, c, rt in unresolvable:
            print(f"  {lid:44} category={c!r} rating={rt!r}")
        print()

    total = sum(len(v) for v in stale.values())
    if not total:
        print("All icons match the data. Nothing to re-assign.")
    else:
        print(f"{total} pin(s) need a new icon, grouped so you can batch them:\n")
        for icon in sorted(stale):
            print(f"  ==> assign '{icon}' to {len(stale[icon])} pin(s):")
            for lid, name, had in stale[icon]:
                print(f"        {name[:56]:58} (was {had})")
            print()

    if synced:
        for r in rows:
            r["category_on_map"] = r.get("category", "")
            r["rating_on_map"] = r.get("rating", "")
            r["quality"] = strip_flag(r.get("quality"))
        save(rows)
        print("Baseline updated: the map is now recorded as matching the data.")
    else:
        save(rows)
        if total:
            print("Quality column flagged. Re-run with --synced AFTER you have")
            print("assigned these icons on the map.")


if __name__ == "__main__":
    main()
