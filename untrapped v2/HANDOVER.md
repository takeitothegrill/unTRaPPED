# unTRaPPED V2 — handover, 2026-09-06

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

- **CSV is now the source of truth for coordinates.** Pins cannot be dragged
  from an automated session, so positions come from importing a CSV that
  carries lat/long — NOT from photo EXIF. This is a change of approach.
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
  nothing happened. So `7 town layers + 4 feature layers = 11` is NOT possible.
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
  This means photo attachments are portable DATA, not locked to the map — if
  that column re-imports, photos can be carried to a rebuilt map without
  re-attaching anything by hand.
- **KML for any map** can be downloaded from
  `https://www.google.com/maps/d/kml?mid=<MID>&forcekml=1` — no UI needed, and
  it avoids opening the production map's ⋮ menu (which contains Move to Bin).
- **The Google Drive MCP connector works** for staging import CSVs — pass
  `contentMimeType: "text/csv"` and `disableConversionToGoogleType: true`.
  No browser involved.

## OPEN — untested

- **Is the layer cap really 10?** Not verified. Planned structure is 7 town
  layers (Yeppoon, Emu Park, Keppel Sands, Byfield, Cawarral, Great Keppel
  Island, Cedar Park) + 4 feature layers = **11**, which would exceed it.
  Test by adding layers until refused.
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
- Before and after any batch edit, check the photo count:
  `curl -s "https://www.google.com/maps/d/kml?mid=<MID>&forcekml=1" | grep -c gx_media_links`
  Working copy should read **71 pins carrying 253 photos**.

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

1. **Does the legend sort alphabetically, or by insertion order?** Unknown, and
   it matters: the whole venue-type naming scheme assumes a user can scan for
   "playground". Check this on v7 first.
2. **Photos.** CSV-imported pins arrive empty. ~24 attachments would need
   redoing on any rebuilt map. Not yet decided.
3. **`status` is map-agnostic** — it records "synced" but not "synced to which
   map". Bit us once. Needs a `synced_map` column or one-map discipline.
4. The lat/long override remains inert on the photo-import path; the CSV-import
   path replaces it. Runbook still documents the old behaviour in step 2.

## Housekeeping

- Google Drive root has `merge.csv`, `merge-playground-...csv`,
  `merge-batch-260906.csv` from three runs — clutter, user to delete.
- Google Photos album `untrapped-icons` has 13 items: 12 icons plus a duplicate
  `toilet-green` (an older smaller version alongside the corrected one).
- v5 browser tab was left on the v6 viewer by an agent.
