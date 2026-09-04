# unTRaPPED V2 — sync runbook

How to actually push `locations.csv` + `processed/` onto the real My Maps map.
There is no API for My Maps — this is a live Claude Code session driving the
browser via Claude-in-Chrome, following the exact steps below. Validated
end-to-end on a real location (2026-09-06) — see STATUS.md for the test log.

**Before starting:** run `python process_locations.py` then
`python plan_sync.py` to get the work list. Do NOT attempt this runbook on
the real production map until you've dry-run it once on a throwaway map —
a failed merge can be destructive (see the lat/lon warning below).

## Per NEW location (status blank)

**1. Hero photo → Google Photos album**
- `photos.google.com` → `+` → Album → title it (any unique name, e.g.
  `untrapped-v2-<location_id>`).
- Click **Add photos** → **Select from computer**. This opens a native OS
  dialog — Claude can't drive that directly, but a real `<input type=file>`
  briefly exists in the DOM right after the click. Find it with
  `document.querySelectorAll('input[type=file]')` (via javascript_tool) or
  the `find` tool, then use `file_upload` on its ref with the **hero photo
  only** (`processed/<location_id>/<first photo>.jpg`).
- Click **Done** on the "backed up" toast — the photo auto-adds to the album.

**2. Import into My Maps (Pass 1)**
- On the target map: **Add layer** (or reuse an existing "Imported Photos"
  layer) → **Import** → **Albums** tab → select the album → select the 1
  photo → **Insert**.
- This creates a pin, positioned from the photo's own EXIF GPS, auto-named
  to a nearby real business (e.g. "Coastal Hill Cafe") — expected, not a bug.

**3. Rename the pin**
- Click the new pin → pencil (edit) icon → triple-click the name field →
  type the **exact `location_id`** → Save. This is the match key for the
  next step — there is no shortcut, it must be done for every new pin.

**4. Merge metadata (Pass 2) — CSV must NOT include latitude/longitude**
- Build a small CSV: `location_id,name,description,category` (category as
  the **numeric** id from `categories.py`, e.g. Parking=5). Do **not**
  include lat/lon — including them destructively wiped pins in earlier
  testing (see STATUS.md). No known official reason; just never do it.
- The layer's data-file **Upload** widget is a cross-origin iframe Claude
  cannot drive — instead: upload the CSV to **Google Drive** first (same
  technique as step 1: find the file input after clicking Drive's own
  `New → File upload`, `file_upload` it there), then in My Maps: layer
  **⋮ → Reimport and merge → Merge matching items** → **Google Drive** tab
  → select the uploaded CSV → Insert.
- **Column-match screen:** pick **Layer data `name`** = **Uploaded data
  `location_id`** → Finish. Confirm the toast says "Layer was updated with
  new content" (not an error). Click the pin to verify name/description/
  category landed and the photo is still attached.

**5. Extra photos → per-location Drive folder → attach one at a time**
- Google Drive → **New → Folder**, named `<location_id>`. Upload every
  *non-hero* photo from `processed/<location_id>/` into it (one at a time —
  `file_upload` caps at 10MB per call regardless, and Drive's own picker
  only allows single-select anyway).
- On the pin: camera icon → **Google Drive** → double-click into the
  `<location_id>` folder → click one photo → **Insert** → **Save**. Repeat
  once per extra photo — this dialog is single-select only, confirmed by
  testing both single-click-then-second-click (deselects the first) and
  there being no visible multi-select control.
- After each Save, the pin's popup closes — re-click the pin in the layer
  list to reopen it before adding the next photo.

**6. Mark done**
- Update `locations.csv`: set `status=done`, `synced_photos=` comma-joined
  list of every photo filename now attached (hero + extras).

## Per UPDATED location (status=update)

Same as steps 4–5, using `plan_sync.py`'s `photos_to_add` /
`photos_to_remove` lists — skip steps 1–3 (the pin already exists and is
already renamed to `location_id` from its original sync).

**Removing a photo:** open the pin → pencil (edit) icon → the photo
carousel shows a trash icon next to the currently-displayed photo → click
it. Confirmed working (2026-09-06). Navigate the carousel (`< n of N >`)
to the specific photo before deleting it.

## Known friction, so you don't re-discover it

- **Google's own "Upload"/"Choose a file to import" widgets are
  inconsistent**: Photos' and Drive's own upload buttons expose a real
  `<input type=file>` in the DOM right after clicking (automatable). My
  Maps' own CSV-import "Upload" tab does not — it's a cross-origin iframe.
  Route CSVs through Drive first instead of fighting that iframe.
- **The Drive "New" menu is easy to mis-click** after a page has just
  navigated or a toast is showing — screenshot to confirm the menu actually
  opened before clicking "File upload", or you'll silently navigate to
  Drive's Home instead.
- **My Maps tabs occasionally freeze mid-screenshot** (CDP timeout) after a
  burst of interactions — wait a few seconds and retry the screenshot
  rather than clicking again blindly; repeated clicks into a frozen tab
  can stack duplicate popups and visually corrupt the page (a reload fixes
  it).
- **file_upload has a 10MB per-call limit** — upload photos one at a time,
  not batched, even when a picker looks like it might accept multiple
  paths at once.
