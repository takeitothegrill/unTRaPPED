# unTRaPPED V2 — handover, 2026-09-06

> **2026-09-12: this is a working record, not canon.** Project state, the full map
> register (incl. v4 `1Gt4Y0lCkLbi7DVXk0IJIOw_tmFX0U4k`, never recorded here), the pin
> spec and the process description are in `my-brain-context/projects/untrapped*.md`.
> Where this file and canon disagree on state or decisions, canon wins.

> **READ `VERIFIED.md` FIRST.** It lists what has already been PROVEN on this
> project. Never ask the human to re-test anything on that list. If this
> document contradicts it, VERIFIED.md wins.


Picking this up cold? Read `pipeline/RUNBOOK.md` first, then
`pipeline-test-artifacts/STATUS.md` for the full test history.

## State

- **Icons: DONE.** 12/12 in `icons/final/`, all designer originals, verified at
  true 18px. See `icons/final/MANIFEST.md`.
- **Runbook: validated** by two independent cold fresh-agent runs plus one
  production run. Corrected against all findings.
- **Pipeline:** `plan_sync.py --write-merge-csv [--only <id>]`; `merge.csv`
  structurally cannot carry coordinates.
- **Maps built (all throwaway tests):**
  - v5 `1xTLQzqrYdHsTqzgIu2Pdh7eAUmbs1lw` — 1 pin
  - v6 `189o4kIBKSx4yLasAOjdAVd42KIxhlb4` — 6 pins + photos, single layer
    grouped by `icon` (legend NOT clickable — this is the problem)
  - v7 `untrapped v7 - layered legend test` — being built: 4 layers,
    individual styles, positions from CSV. **Find it in the My Maps list.**
  - PRODUCTION `1mOXyoupEm3Pc8QmL-Yvrxrqt9eIsG48` — untouched, do not use
    until the pipeline is settled.

## Decisions made

- **On Path B (CSV import) the CSV is the source of truth for coordinates.**
  Pins cannot be dragged from an automated session, so on a map built by CSV
  import positions come from the CSV's lat/long — NOT from photo EXIF. On Path A
  (Photos-Albums import, the only route to a native photo) the pin is placed
  from EXIF and the CSV coordinate does not reach the map. This is a change of
  approach.
- **Four layers, individual styles** — never "Group places by", which collapses
  the per-pin legend into style groups.
- **Split by LGA**, not township. Layers are by type, so one map holds every
  township; what degrades is legend length. `import/locations-livingstone.csv`
  (7 rows) and `import/locations-rockhampton.csv` (2 rows) are generated from
  `locations.csv`, which stays the master.
- **Names:** `TOWNSHIP | TYPE - descriptor [RATING]`. Descriptor is `disability`
  for parking/toilets, the SURFACE for routes (grass, concrete), and the VENUE
  TYPE for venues (playground, cafe, park...) so users can scan the legend for
  the kind of place they want.

## Settled since (2026-09-06, later)

- **v7 proves the shape works.** mid `1Ka4jUTKP4dQKiDzwvC-mMtVobdW8Ri8`.
  4 layers, individual styles, all 9 pins listed individually and clickable,
  all 9 coordinates byte-exact from the CSV.
- **Legend order is IMPORT order, not alphabetical** — confirmed on the live v7
  legend (Parking reads GOOD, OKAY, GOOD, OKAY = CSV row order; alphabetical
  would put the Cedar Parks first). So the CSV sort controls what the public
  sees.
- **`pipeline/build_import.py` added.** Emits `import/<lga>/<Layer>.csv`, one per
  map layer, sorted by name — which groups the legend by township, since names
  start with the township.
- **Runbook restructured around two paths.** Path B (CSV import) is now primary
  for building maps; Path A (photo import + merge) is for attaching photos and
  discovering EXIF. The "lat/long override is inert" warning is scoped to Path A
  only — on Path B coordinates are honoured exactly.

## OPEN — needs a decision before the real build

**Pin names are not unique, and the legend is now the navigation control.**
Livingstone currently produces two identical `YEPPOON | PARKING - disability
[OKAY]` entries and two identical `YEPPOON | TOILET - disability [OKAY]`
entries. A user scanning for an accessible toilet cannot tell the Family
Practice from the Spinnaker Club.

The name needs the PLACE in it, e.g.
`YEPPOON | Spinnaker Club - TOILET [OKAY]`. Format to be agreed, then applied to
the `name` column in locations.csv.

## My Maps behaviour — established by the human, not automatable

These were all confirmed by hand. Claude's browser automation could NOT do any of
them, which is a limitation of the tooling, not the product:

- **Layers CAN be dragged into a new order.** There is no "move up/down" in the
  layer ⋮ menu (only Rename / Delete / Open data table / Import / Reimport and
  merge / Export data) — you drag the layer header.
- **Pins CAN be reordered within a layer.**
- **Pins CANNOT be repositioned by an agent** — every drag method pans the map.

## Public viewer vs editor — a real usability gap

- **Hovering a legend entry highlights its pin on the map in EDIT mode, but NOT
  in the published viewer.** So the public legend cannot show you *where*
  something is; it can only navigate when clicked. This is why the map, not the
  legend, has to be the primary search surface.
- **The viewer HAS a search box, and it searches pin DESCRIPTIONS as well as
  names, surfacing this map's pins above general Google places.**
  Consequence: put the town and street address in the `description`, and
  everything at one site ("Lioness Park") surfaces together on a search. This
  removes most of the pressure from pin names.

## Legend text budget

Legend rows are `white-space: nowrap; overflow: hidden; text-overflow: ellipsis`
and cap at **301px ≈ 40 characters** at 14px Roboto. They TRUNCATE, never wrap,
and the END of the name is what is lost — so never put the rating last if the
name is long.

## CONFIRMED 2026-09-06 (late)

- **The layer cap IS 10.** Tested by adding layers to v7 until refused: it
  stops at 10 and **fails SILENTLY — no error, no message**. You just notice
  nothing happened. So the planned `7 town layers + 4 feature layers = 11`
  (towns: Yeppoon, Emu Park, Keppel Sands, Byfield, Cawarral, Great Keppel
  Island, Cedar Park) is NOT possible. OPEN in canon: `untrapped-processes.md` P8.
- **My Maps is very laggy — allow 5-8 seconds per interaction.** Several
  "failed" clicks in earlier sessions had in fact registered; the checks were
  racing the UI. If a click seems not to work, WAIT before retrying, or you will
  double-apply it (this is how v7 gained six stray empty layers).
- **Production map contents (read-only KML audit):** 103 placemarks across
  9 layers (already one short of the cap), 71 of them carrying photos,
  **254 photo links total**, max 10 photos on one pin. Almost none of this data
  exists in `locations.csv` (9 rows) — so the production map, not the CSV, is
  currently the system of record.
- **Photos export as a plain data column**, `gx_media_links`, holding
  space-separated `https://mymaps.usercontent.google.com/hostedimage/...` URLs.
  **Photos are not portable.** Re-importing the column gives plain text, not
  photos, and the URLs are session-scoped and dead outside the editing session
  (VERIFIED #12). Only `Copy map` carries photos to another map.
- **KML for any map** can be downloaded from
  `https://www.google.com/maps/d/kml?mid=<MID>&forcekml=1` — no UI needed, and
  it avoids opening the production map's ⋮ menu (which contains Move to Bin).
- **The Google Drive MCP connector works** for staging import CSVs — pass
  `contentMimeType: "text/csv"` and `disableConversionToGoogleType: true`.
  No browser involved.

## OPEN — untested

- **Z-order.** Observed on v7: layer order is Parking, Toilets, Routes, Venues,
  and the green Route icon draws OVER the blue Parking icon where they are ~6 m
  apart. That implies **later layers draw on top**, i.e. legend order and z-order
  are INVERTED — to put Parking on top of the map it must be LAST in the list.
  Unverified; test by dragging Routes above Parking and seeing if P now wins.

## Category and layer decisions (2026-09-06)

- **Layers are: Parking / Toilets / Pathways & Routes / Venues & Amenities.**
  "Pathways & Routes" leads with the concrete word people recognise while still
  covering ramps, doors and lifts.
- **Venues and Amenities share ONE layer, deliberately.** A park with markets on
  is an amenity on Monday and a venue on Sunday. If the surveyor cannot reliably
  tell them apart, a user cannot either, and a filter that cannot be applied
  consistently is worse than none. It also costs a layer that towns need.
  The distinction is preserved in the DATA: `Amenities` is category 9 in
  `categories.py`, mapping to the same `venue` icon — and the venue TYPE inside
  the pin name (playground, beach, cafe, plaza) carries it for users.
- **Ratings:** EXCELLENT and GOOD are green, OKAY is orange, anything negative
  is red. **When undecidable, default to RED** — never overclaim accessibility.
- **Base map is always Simple Atlas** — see RUNBOOK "Canonical map settings".

## THE CSV IS NOW THE SOURCE OF TRUTH (decided 2026-09-06)

`locations-from-v1-map.csv` (87 rows, extracted from the V1 map) is authoritative
for all TEXT: names, descriptions, categories, ratings, coordinates, township,
LGA, address.

**But photos are the exception, and it is a hard one.** Photos live only on the
map. They cannot be exported and re-attached — CSV import ignores them, and the
exported image URLs are session-scoped and dead outside the editing session.
`Copy map` is the only thing that preserves them.

**So the model is a hybrid, and it must stay one:**

| | source of truth | how it moves |
|---|---|---|
| text, category, rating, position | the CSV | regenerate + re-import, or merge |
| **photos** | **the live map only** | **Copy map, or re-upload by hand** |

**Consequences to respect:**
- **Never rebuild a photo-bearing map from CSV.** You would lose every photo.
- To push CSV text changes onto an existing map, use **Reimport and merge**
  matching `location_id` = `location_id`, with **no lat/long columns**.
- **Never delete a pin that has photos.** Move it, rename it, re-rate it.
- Before and after any batch edit, check both counts. `grep -c gx_media_links`
  counts **pins carrying photos** (the tag appears once per pin), not photos:
  `curl -s "https://www.google.com/maps/d/kml?mid=<MID>&forcekml=1" | grep -c gx_media_links`
  For the **photo count**, use the script in RUNBOOK.md ("Photos CANNOT be
  moved between maps"), which splits each tag's URLs. Working copy: **70 pins
  carrying 253 photos**. Its KML needs a signed-in session: an anonymous `curl`
  gets a 403 and counts 0.

## Live layer names (must match `build_import.py` exactly)

    YEPPOON CBD                    town locator, 1 pin
    EMU PARK CBD                   town locator, 1 pin
    TOILETS (disability)           20 pins, 105 photos
    PARKING (disability sticker)   28 pins,  60 photos
    PATHWAYS and ROUTES            28 pins,  66 photos
    VENUES and AMENITIES           10 pins,  22 photos

6 of a maximum 10 layers — 4 spare for further town locators.
Base map: Simple Atlas (set 2026-09-06).

## Open questions

1. **Photos.** CSV-imported pins arrive empty. ~24 attachments would need
   redoing on any rebuilt map. Not yet decided.
2. **`status` is map-agnostic** — it records "synced" but not "synced to which
   map". Bit us once. Needs a `synced_map` column or one-map discipline.
3. The lat/long override does not reach the map on Path A (photo import); on
   Path B (CSV import) the CSV coordinates are where the pin lands.

## Housekeeping

- Google Drive root has `merge.csv`, `merge-playground-...csv`,
  `merge-batch-260906.csv` from three runs — clutter, user to delete.
- Google Photos album `untrapped-icons` has 13 items: 12 icons plus a duplicate
  `toilet-green` (an older smaller version alongside the corrected one).
- v5 browser tab was left on the v6 viewer by an agent.

## Photo reconciliation, copy vs production (checked 2026-09-07)

PRODUCTION `1mOXyoupEm3Pc8QmL-Yvrxrqt9eIsG48` — ~~100~~ **103** placemarks, 71 pins with
photos, **254 photos**. Untouched.
*(Corrected 2026-09-12: "100" was a transcription slip — the measurement taken seconds
earlier read 103, and both the 6 Sep export and the 12 Sep live KML read 103 = 95 points
+ 3 polygons + 4 lines + 1 geometry-less. Detail: my-brain-context
`projects/untrapped.md`, 2026-09-12 entry.)*

WORKING COPY `1GsgVncG-IYRalSk_u7ZmuDQluhPQmpQ` — as measured that day:
88 `<Placemark>` = 85 `<Point>` + 2 `<Polygon>` (the CBD boundaries) + 1
geometry-less empty placemark. 70 pins with photos, **253 photos**.
After the blank placemark was deleted on 2026-09-07: **87 `<Placemark>`**
= 85 Points + 2 Polygons, still 253 photos.

(Careful with these three counts. "Placemarks", "pins", and "pins with photos"
are three different numbers — 88 / 85 / 70 — and mixing them up is how the
earlier "71 vs 70" confusion started.)

The single-photo difference is fully accounted for. **`Copy map` lost nothing.**
A KML read of the copy on 6 Sep measured 103 placemarks and 254 photos at 18:18,
and still 254 photos at 18:24, after the human's layer deletions.

    PEDESTRIAN CROSSING - disabled [EXCELLENT]
        production  150.74666,-23.12873   1 photo
        copy        150.74666,-23.12885   0 photos

- **The original crossing pin was deleted.** It happened during the hand
  restructure, between 18:24 and 21:31 on 6 Sep. Pins and photos each fell by
  one at the same time.
- **The agent re-created it at 22:32.** It imported
  `import/_RECOVER_crossing.csv` at production's exact coordinates, with
  `location_id` `pedestrian-crossing-recovered`. CSV import cannot carry photos
  (VERIFIED #12), so the re-created pin has none.
- **The human then moved it about 13 m** to its correct position. The
  production pin had been in the wrong place (human, 13 Sep).

That is the whole of the 254 -> 253 gap; every other pin kept all of its photos.

Recovering it is manual only — My Maps regenerates photo URLs on copy and the
hosted image needs an authenticated session. Either save the image from the
production map and re-add it, or find the geotagged original in Google Photos.

### The trap here

Coordinates survive copying and renaming, which is why they are the right key
for those. They do NOT survive a manual move, so a moved pin looks the same as
a deleted one under a coordinate diff. And a pin re-created at the same spot
looks the same as a surviving one. Check the session record before you explain
a difference.

There is no single reliable key. Cross-check at least two of {coordinates,
name, photo count} and reconcile the totals before claiming anything was lost.
A one-directional diff (production -> copy) also cannot see additions or moves;
run it BOTH ways.

### How to compare two maps — the two traps

1. **Photo URLs are regenerated by `Copy map`.** Every `hostedimage` URL differs
   between an original and its copy, so diffing by URL reports ~250 false
   losses. Useless as an identity key.
2. **Names change.** Renaming pins makes a name-based diff report renamed pins
   as deleted, which also badly overstates loss.

Diff on **coordinates**. They survive both copying and renaming. Compare
per-coordinate photo counts, which distinguishes "pin deleted" from "photos
removed from a surviving pin" — a distinction the totals alone cannot make.
