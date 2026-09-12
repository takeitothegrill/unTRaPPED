# How to start an agent on this project

> **READ `VERIFIED.md` FIRST.** It lists what has already been PROVEN on this
> project. Never ask the human to re-test anything on that list. If this
> document contradicts it, VERIFIED.md wins.


There are **two different jobs** and they use **two different CSVs**. Picking
the wrong one is the most common way to waste a session, because the failure is
silent — a merge that matches nothing reports success and changes nothing.

| | Job A — add NEW pins | Job B — update EXISTING pins |
|---|---|---|
| CSV | `locations.csv` | `locations-from-v1-map.csv` |
| Photos | yes, new photos attached | no, photos already on the map |
| Map operation | import (creates pins) | merge (updates pins) |
| Source folder | `incoming/<location_id>/` | none |

## Easiest: just ask

In a session that already has this project's context:

> I've added rows to locations.csv, put them on the map.        (Job A)
> I've updated locations-from-v1-map.csv, push it to the map.   (Job B)

---

# JOB A — add new pins with photos

## What is and is not automatic

Be honest with yourself about this before promising the human anything:

- **Automatic:** photo conversion, watermarking, EXIF coordinate discovery,
  building the import CSV, and the text of every pin.
- **Not scriptable, but still YOUR job:** attaching photos 2..n to a pin. Only
  the *hero* photo rides along with a Path A import. Every additional photo goes
  on through the pin's own photo picker, which is **single-select**, sourced
  from a Drive folder. A location with 6 photos means 5 separate attachments.

  These are done by YOU in the browser. Do NOT hand them back to the human —
  they are slow, not manual. Budget for it: ~30 photos across 9 locations is
  the bulk of the session's clicking.

The CSV carries photo FILENAMES, not photos. `incoming/` holds the originals
and `processed/` holds the watermarked JPEGs that actually get uploaded.

## Which path — USE PATH A. This is tested and was explicitly decided.

**Do not substitute a CSV import here, however sensible it looks.** A
CSV-imported pin gets **no inline photo** — a bare image URL in the description
linkifies as blue text and does NOT render as a thumbnail (tested 2026-09-05).
The Photos-Albums import is the ONLY route that produces a real inline photo in
the balloon. The user was offered the safer links-in-description alternative
and **explicitly declined it** in favour of the native gallery, accepting the
extra fragility. That decision is not yours to quietly reverse.

TEST 3 in `pipeline-test-artifacts/STATUS.md` is a full PASS for:

```
Pass 1  Google Photos album -> layer -> Import -> "Albums" tab
        => pins created at EXIF GPS, hero photo attached natively
Pass 2  layer ⋮ -> Reimport and merge -> match on the renamed pin
        => metadata added; photos and styling SURVIVE the merge
```

- The layer-level Import dialog's **"Google Drive" tab only shows CSV/XLSX/KML**
  and its **"Upload" button rejects images**. The **"Albums" tab** is the one
  that works. Do not waste a session rediscovering this.
- **Pass 2 MUST exclude lat/lon columns.** Including them on photo-imported
  placemarks is what caused the earlier destructive failure. The photo-derived
  position is already correct and does not need resupplying.

## Steps

```
cd pipeline
python process_locations.py     # HEIC->JPEG, watermark, EXIF lat/lon backfill
python plan_sync.py --write-merge-csv --only <location_id>
```

`--only` scopes `merge.csv` to one location. Without it the file holds every
pending row, and the merge **silently ignores rows that are not already pins**.

Then per location: hero photo -> Photos album -> Import (Albums tab) -> rename
the pin to its `location_id` -> merge -> attach extra photos -> remove the
stale address card -> assign the icon.

## New pins land in the wrong layer — move them, it is safe

Path A creates pins in a NEW "Imported Photos" layer at EXIF coordinates. The
map is organised into four typed layers on Individual styles, so every new pin
must be dragged into its correct layer in the side panel.

**Dragging a pin between layers KEEPS its photo — verified by the user,
2026-09-08.** You do not need to re-prove this or ask permission.

Do not confuse that with repositioning a pin ON THE MAP, which is a different
gesture and is **not achievable from an automated session** — drag tool,
hover-then-drag and synthetic mouse events all just pan the map. That is why a
lat/long override differing from hero EXIF by >~25 m must be flagged to the
human rather than fixed.

The photo count is still your safety line either way: it should RISE as you
attach photos and must never fall.

## Extra photos and the stale address card — both per-pin

- Extra photos: the pin's **"+" -> "Google Drive" tab**. This works on
  already-imported pins. The **"Photos" tab in that picker is flat and
  by-date** with no album filter — impractical at scale, do not use it. One
  photo at a time; there is no multi-select.
- Photos-Albums import attaches a wrong **"Details from Google Maps"** business
  card via implicit reverse-geocode. It has a **Remove** link, does not
  auto-update, and survives dragging the pin. Remove it on every pin. A
  CSV-imported pin never gets one — this side effect is Path A only.

## Before you start — check every row has a folder

A row whose `location_id` has no matching `incoming/<location_id>/` folder is
**skipped in silence**. This has already bitten this project twice. Run:

```
python -c "
import csv, os
rows=list(csv.DictReader(open('../locations.csv',encoding='utf-8')))
inc=set(os.listdir('../incoming'))
bad=[r['location_id'] for r in rows if r['location_id'].strip() and r['location_id'].strip() not in inc]
print('MISSING FOLDERS:', bad or 'none')"
```

Folder names must match `location_id` EXACTLY, including case. If two rows
share one photo shoot (e.g. two car parks at one centre), the folder must be
SPLIT — the `synced_photos` column already declares which photos belong to
which row.

---

# JOB B — update existing pins

layer ⋮ -> **Reimport and merge** -> **"Merge matching items"**.
Match `Layer data location_id` = `Uploaded data location_id`.

**Menu label:** this project's notes contain both "Merge matching items" (4
places, including the most recent) and "Update matching items" (once, in the
earliest test log). Only one is real and it has not been re-checked against the
live UI. Go by BEHAVIOUR, not the label — under `Reimport and merge` you want
the option that UPDATES existing rows by matching a key, not `Add more items`
which APPENDS. Read what the dialog actually says and correct these docs.

- **NO latitude/longitude columns in a merge CSV.** It destroyed every pin on a
  test map. (Imports are the opposite — they REQUIRE coordinates.)
- Rows matching nothing are **SILENTLY DROPPED**. No error, no warning.
- A merge does NOT change icons. See below.

---

# THINGS THAT APPLY TO BOTH

## Target map

WORKING COPY: `1GsgVncG-IYRalSk_u7ZmuDQluhPQmpQ`
Never modify PRODUCTION `1mOXyoupEm3Pc8QmL-Yvrxrqt9eIsG48` — it is the live
public map and its URL has been shared. Read it if you like; do not write to it.

## Pre-flight

**a. The map tab must be the VISIBLE, FOREGROUNDED tab.** Check
`document.visibilityState`. If it returns `"hidden"`, My Maps does not
initialise, no click lands, and everything appears to succeed. A Chrome window
that is merely open but fully covered by another window counts as hidden. Ask
the human to put the windows side by side.

**b. Record the photo count. This is the safety line.**

```js
const txt = await fetch(`https://www.google.com/maps/d/kml?mid=<MID>&forcekml=1&cb=`+Date.now(),
                        {cache:'reload'}).then(r=>r.text());
const vals = [...txt.matchAll(/<Data name="gx_media_links">[\s\S]*?<value>([\s\S]*?)<\/value>/g)]
  .map(m => m[1].replace(/<!\[CDATA\[|\]\]>/g,'').trim());
({ pinsWithPhotos: vals.length,
   photos: vals.reduce((n,v) => n + v.split(/\s+/).filter(Boolean).length, 0) })
```

Baseline as at 2026-09-07: **253 photos across 70 pins**, 87 placemarks
(85 points + 2 CBD boundary polygons). Adding pins makes these numbers RISE.
The rule is that they must never FALL.

⚠ **`grep -c gx_media_links` does NOT count photos.** That tag appears once per
pin with all its URLs inside one `<value>`, so it counts pins (70), not photos
(253). Comparing the two as if they measured the same thing looks like a loss
that never happened.

**c. `python pipeline/check_icons.py`** — lists pins whose icon no longer
matches their data.

## Icons

All 11 icons are already in this map's custom library, so a new pin is
hover -> paint-can -> one click, with no dialogs and no re-importing.

- The layer is on **Individual styles**, so a new pin does NOT get its icon
  automatically. Every one is assigned by hand.
- Batch **by icon, not by pin**. Previously-used icons sit under "Other icons".
- **The icon picker is SINGLE-SELECT.** Selecting several silently keeps one.

## Rating -> colour

EXCELLENT / GOOD = green, OKAY / STANDARD = orange, POOR / BAD = red.
When in doubt go one colour LOWER. When you cannot decide, choose RED.
Parking and Toilets are always the blue shape with a rating DOT; Routes and
Venues take the rating colour as the WHOLE shape.

## Verifying

- **KML CANNOT verify icons.** Every placemark reports the stock blank marker
  no matter what icon is applied. Use a screenshot or the layer-panel row's
  icon `background-image`.
- **KML lags** — sometimes by a minute — even with `cache: 'reload'` and a
  cache-buster. For anything you JUST changed, read the live DOM. If the DOM
  and the KML disagree, trust the DOM.
- Comparing two maps: there is **no single reliable key**. Copying regenerates
  every photo URL, renaming breaks name matching, and moving a pin breaks
  coordinate matching. Cross-check at least two of {coordinates, name, photo
  count}, and diff in BOTH directions or you will not see moves and additions.

## STOP AND ASK if

The photo count drops, a merge reports rows it could not match, the pin count
moves unexpectedly, the tab goes hidden, or anything looks irreversible that
the runbook has not explicitly told you to do.

## Report honestly

Pins before/after, photos before/after, which icons still need assigning, what
you could NOT do, and anything in the runbook that turned out to be wrong.
If you completed 6 of 9, say 6 — never round up or imply completeness you have
not verified.

---

## After it finishes

- `python pipeline/check_icons.py` and assign anything flagged.
- `python pipeline/check_icons.py --synced` to move the baseline forward.
- Confirm the photo count went UP by the number you attached, and that no
  existing pin lost any.
