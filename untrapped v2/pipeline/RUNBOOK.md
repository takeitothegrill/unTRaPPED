# unTRaPPED V2 — sync runbook

> **READ `VERIFIED.md` FIRST.** It lists what has already been PROVEN on this
> project. Never ask the human to re-test anything on that list. If this
> document contradicts it, VERIFIED.md wins.


How to push `locations.csv` + `processed/` onto a Google My Map. There is no API
for My Maps — this is a live Claude Code session driving the browser via
Claude-in-Chrome.

Corrected against two full end-to-end fresh-agent runs, 2026-09-06. Test log:
`pipeline-test-artifacts/STATUS.md` (git-ignored, so not beside this file).

**Production map mid:** `1mOXyoupEm3Pc8QmL-Yvrxrqt9eIsG48` (embedded on
untrapped.au). Never run an untested change against it.

---

## Read this first: what is and is not automatable

**Only two upload routes work.** Google Photos' and Google Drive's *own* upload
buttons expose a real `<input type=file>` in the page after you click them.

**Every "Upload" tab inside a Google picker is a dead end.** Tested 2026-09-06 on
both the custom-icon dialog ("Choose a file to import") and the pin photo dialog
("Choose an image or a video"): the Upload panel is the same component in a
**cross-origin iframe** — zero reachable file inputs, before and after clicking
Browse. My Maps' CSV-import Upload tab is the same widget.

**Do not try to shortcut Section 0a or Step 5 by using those Upload tabs.** It
looks like it should work. It cannot. That is why icons go via a Photos album and
photos go via a Drive folder.

## Two paths — pick the right one

**Path B (CSV import) is now the primary route for building a map.** Path A
(photo import + merge) is retained because it is how photos get attached and how
EXIF coordinates are discovered.

| | Path A — photo import + merge | Path B — CSV import |
|---|---|---|
| Creates pins from | a Google Photos album | a CSV with lat/long columns |
| Pin position | on Path A the pin sits at photo EXIF; the CSV lat/long **never reaches the map** | on Path B the pin sits on **exactly the CSV coordinates** |
| Photos | attached automatically (hero) | none — must be attached by hand |
| Pin naming | reverse-geocoded, must be renamed | taken from a CSV column |
| Stale address card | yes, must be removed | **none — no geocoding happens** |
| Legend | usually grouped by column -> no per-pin list | individual styles -> **clickable per-pin legend** |

Use **Path B** when position accuracy and a usable legend matter — i.e. for the
real maps. Use **Path A** only when the point is to let photos place themselves.

Verified on the v7 test map, 2026-09-06: all 9 CSV-imported pins landed on
byte-exact coordinates, and the legend listed every pin individually.

## Path B — build a map from CSVs

1. `python pipeline/build_import.py` writes `import/<lga>/<Layer>.csv` — one
   file per map layer, four layers per LGA, rows **sorted by name**.
2. **Legend order is import order, not alphabetical** (confirmed on v7). Because
   names are `TOWNSHIP | TYPE - descriptor [RATING]`, sorting by name groups the
   legend by township. Change the sort in `build_import.py` and you change what
   the public sees.
3. Create the map at `https://www.google.com/mymaps` -> **"Create a new map"**.
   (`https://www.google.com/maps/d/edit` with no mid **404s**.) A consent dialog
   appears — *"Creating a MyMaps map always uploads title, thumbnail and
   associated metadata to Drive"* — click **CREATE**.
4. Get the CSVs into Drive. The **Google Drive MCP connector uploads them
   directly, no browser needed** — pass `contentMimeType: "text/csv"` **and**
   `disableConversionToGoogleType: true`, or Drive silently converts them to
   Sheets and the import breaks.
5. Import each file as its **own layer**: first one into the empty "Untitled
   layer", the rest via **Add layer**. In the Drive picker the **search box
   works** — click, type the filename, Enter, then **double-click** the tile.
   There is no Insert step.
6. Two wizard screens follow: **"Choose columns to position your placemarks"**
   (latitude/longitude auto-ticked -> **Continue**), then **"Choose a column to
   title your markers"** -> pick **`name`** -> **Finish**.
7. The layer is named after the FILE (`Parking.csv`). Rename via layer ⋮ ->
   **Rename this layer**.
8. **Leave every layer on "Individual styles".** Never "Group places by" — it
   collapses the per-pin legend into style groups, which is the whole reason
   this shape exists.
9. Assign each pin's icon individually (0c below). Every row carries an `icon`
   column naming the exact file.
10. Publish and verify (section 7). No stale address card to remove.

## Wait for My Maps before you check or retry

**My Maps takes 3–5 seconds to respond to a click** (VERIFIED #27). Allow 5–8
seconds before checking whether an interaction worked.

- **Why agent clicks used to "fail":** the checks ran about 3 seconds after each
  click, before the map had responded, so clicks that had registered were read
  as failures.
- **Why retrying is dangerous:** the retry lands too. v7 gained six empty layers
  this way.
- **What fixed it:** wait, then check, and never repeat a click that looks dead
  until the wait is over. The human spotted the lag on 6 Sep; once the agent
  waited, its clicks worked.

## The map tab MUST be the visible, active tab

**My Maps will not initialise in a background tab.** The editor stays at
`visibility:hidden` indefinitely, and **synthetic clicks never arrive** — proved
with a capture-phase `mousedown` listener that recorded zero events. Google
Drive's "New" menu fails the same way.

**In the ACTIVE tab, synthetic JS events DO work on My Maps' own DOM.**
Dispatching `mouseover` / `mousedown` / `mouseup` / `click` reliably drives the
paint-can, "More icons", "Custom icon", "OK", "Share" and "Close" — no
coordinate guessing. Only the **cross-origin pickers** (Photos, Drive) need real
coordinate clicks.

Do all UI work in the browser's one active tab. If several tabs are open you will
be taking over whichever is visible — note which, so it can be restored
afterwards. This cost one run ~40 wasted calls and is the single biggest trap in
the procedure.

**Do not trust a fixed screenshot-to-DOM coordinate ratio.** Ratios of 1.15,
1.33, 1.49, 1.5, 1.6, 1.72, 1.8 and 1.86 have all been observed — changing
between *consecutive screenshots at the same scale*, within one session.

Reliable method for a cross-origin picker: arm a capture-phase `mousemove`
listener, `hover` at a known coordinate over the top document (outside the
iframe), read `clientX/clientY` to get the factor `k`; then take
`iframe.getBoundingClientRect()` and click at `(iframeX + localOffsetX) / k`.
Measure element offsets **relative to the iframe origin**, never to the
screenshot.

## Photos CANNOT be moved between maps except by Copy map

Two methods were tested on 2026-09-06. **Both fail.**

- **CSV import does not carry photos.** A `gx_media_links` column imports as
  plain TEXT into the pin's data, not as an attachment.
- **The pin's "Image URL" option does not work either.** Pasting a
  `https://mymaps.usercontent.google.com/hostedimage/...` URL from a KML export
  renders a preview in the editing session, which looks like success — but the
  image is **not retrievable afterwards**: "we can't find or access the image at
  that URL". Those URLs carry `?authuser=0` and are session-scoped, not durable
  public links. **A loaded preview is not proof the link works.**

**Therefore: `Copy map` is the ONLY way to move photos.** It preserves them
exactly (verified: 103 pins / 254 photos copied identically) because Google is
duplicating its own internal references rather than resolving a URL.

**The practical consequences, which shape the whole pipeline:**

- A map with photos can be **restructured** (rename/reorder layers, move pins
  between layers, edit names and descriptions) but never **rebuilt** from CSV
  without losing every photo.
- Photos are effectively welded to the pin they were uploaded to. Deleting a pin
  destroys its photos irrecoverably — the only copy is whatever the source
  photo album still holds.
- **So: never delete a pin that has photos.** Move it, rename it, re-rate it —
  but do not delete it. Check the photo count before and after any batch of
  deletions:

```js
// pins carrying photos, AND the true photo count
const txt = await fetch(`https://www.google.com/maps/d/kml?mid=<MID>&forcekml=1&cb=`+Date.now(),
                        {cache:'reload'}).then(r=>r.text());
const vals = [...txt.matchAll(/<Data name="gx_media_links">[\s\S]*?<value>([\s\S]*?)<\/value>/g)]
  .map(m => m[1].replace(/<!\[CDATA\[|\]\]>/g,'').trim());
({ pinsWithPhotos: vals.length,
   photos: vals.reduce((n,v) => n + v.split(/\s+/).filter(Boolean).length, 0) })
```

⚠ **`grep -c gx_media_links` does NOT count photos.** That tag appears once per
pin, with all of that pin's photo URLs inside a single `<value>`. Counting the
tag gives you *pins that have photos*. On the working copy that is **70**, while
the true photo count is **253**. Comparing the two numbers as if they measured
the same thing will look like a loss that never happened.


## Adding new rows to a layer that already has pins

Tested on v7, 2026-09-06.

**`Import` is DISABLED on a populated layer** (`aria-disabled="true"`). Google
removes the option rather than letting you overwrite by accident.

**Use: layer ⋮ -> `Reimport and merge` -> `Add more items`.** It APPENDS.
Verified: Parking went 4 pins -> 5, nothing replaced, no other layer touched.
No column wizard appears — the layer already knows its mapping — so it is one
file pick and done.

That submenu holds three things. Know which is which:

| item | does |
|---|---|
| **Add more items** | **appends new pins** — this is the one for new locations |
| Merge matching items | UPDATES existing pins matched on a key; **rows that match nothing are silently dropped** |
| Reimport | untested. Assume it REPLACES the layer. Do not touch it on a layer with photos. |

### The icon does NOT follow the data under Individual styles

An appended pin arrives with the DEFAULT marker even though its row carries
`icon=parking-green` and `legend_label=good`. Those columns are just text in the
pin's data; they style nothing on their own.

**This is the whole trade-off:**

| | icons | public legend |
|---|---|---|
| **Individual styles** | manual, one per pin, forever | every pin listed and clickable |
| **Group places by <column>** | automatic — a pin joins the group matching its value and inherits that group's icon | the group VALUES only, one line per group |

So under Individual styles every bulk upload is followed by a manual styling
session in proportion to its size. Under grouping, an upload arrives styled.

Group by a HUMAN-READABLE column (`legend_label` holds "good" /
"check before you go" / "barriers"), never by `icon` — the legend prints the
column's raw values, and "parking-orange" is useless to a member of the public.

## Canonical map settings

**Base map: always "Simple Atlas".**

Google's default base map renders every unrelated business as a coloured POI
pin, which competes visually with our own markers — at 18px an accessibility
pin and a random cafe pin are hard to tell apart. Simple Atlas calms those
colours so our pins are the loudest thing on the map, which is the entire point.

Set it via the **Base map** control at the bottom of the layer panel. It is a
per-map setting, so apply it to every map at creation.

Viewers can still switch to Terrain or Satellite themselves in the published
map if they want more context when zoomed in — so nothing is lost by defaulting
to the calmest option.

**Also set at creation:**
- **Default view** (map ⋮ → Set default view) — open the map already zoomed to
  the LGA's main town rather than the whole shire.
- **Share** → "Anyone with this link can view" ON; the second toggle, "let
  others search for and find this map on the internet", stays OFF unless the
  map is meant to be publicly discoverable.

## Path A — photo import + merge

Everything from here to "Per UPDATED location" is **Path A**. Use it to attach
photos, and to discover coordinates from EXIF. It is NOT the way to position
pins accurately — see the table above.

## Step order

```
0a  upload icons          once per Google ACCOUNT (check before repeating)
1   hero photo -> Photos  per location
2   import -> creates pin
3   rename pin to location_id
4   merge metadata
0b  style layer by `icon` once per layer, after the first merge
0c  assign icon to group  ONCE PER NEW ICON VALUE — recurs
5   attach extra photos
6   mark done (manual)
7   remove stale address card, then publish
```

**Before starting** — note the `cd`; both scripts live in `pipeline/`:

```
cd pipeline
python process_locations.py
python plan_sync.py --write-merge-csv --only <location_id>
```

`--only` scopes `merge.csv` to one location. Without it the file holds every
pending row, and the merge **silently ignores rows that aren't already pins** —
no error, no warning, indistinguishable from failure.

---

## 0a. Icons → Google Photos (once per Google ACCOUNT)

**Check first.** Open `photos.google.com/albums` and look for **`untrapped-icons`**.
If it exists with 12 items, skip to step 1 — but confirm it is current: compare
against `icons/final/MANIFEST.md`, since icons have been re-cut *after* being
uploaded before.

The album **must** be named `untrapped-icons` — step 0c finds the icons by
searching that exact name, and there is no other way to locate them.

- `photos.google.com` → **Albums** → **"Create album"**.
  - `find` returns **three** "Create album" elements; clicking two of them by ref
    does nothing. Click the visible one by **coordinate**.
  - **The album is created the moment you click**, before you type a title — an
    abandoned attempt leaves a stray untitled album behind, unconditionally.
  - The editor takes **~10 seconds** to render. Screenshot to confirm it is up
    before typing, or your click lands on the left-nav and navigates away.
- **Add photos → Select from computer.** The real `<input type=file>` only exists
  *after* this click. Get its ref with **`find` or `read_page`** —
  `document.querySelectorAll('input[type=file]')` returns DOM nodes, not the
  `ref_N` handles `file_upload` needs.
- The input accepts **multiple files**. `icons/final/` is **~2.0 MB** total, so
  all 12 fit in one call. Keep any single call under **10 MB**.
- A **"You've backed up 12 items / Done"** card appears while the album still
  reads "Album is empty". Not a failure — click Done. Note there are **two**
  Done buttons: the one on this card, and one in the top bar that exits edit
  mode. You want the card's.
- Google re-encodes to ~128px. Expected. SVG is accepted but also rasterised.

## 1. Hero photo → Google Photos album

Same mechanics as 0a. Album e.g. `untrapped-v2-<location_id>`, **hero photo
only** (`processed/<location_id>/<first photo>.jpg`), click Done on the toast.

## 2. Import into My Maps — creates the pin

- **On a fresh map, use the existing "Untitled layer" and its own Import link.**
  Clicking "Add layer" first leaves a second, empty layer behind.
- **On a map that already has a populated layer there is no "Untitled layer"** —
  you must "Add layer", and you then have **two layers both named "Imported
  Photos"**, each needing its own 0b styling. Expect this when adding to an
  existing map.
- **This picker IS multi-select** — selecting 5 photos and clicking Insert once
  creates 5 pins together. The *pin photo* picker in step 5 is single-select;
  they are different widgets.
- **Import** → **Albums** is a **left-side nav item, not a tab** →
  **double-click** the album to open it (single-click selects and appears to do
  nothing) → select the photo → **Insert**.
- The pin is placed from the photo's **EXIF GPS** and auto-named after a nearby
  **business or street address**. Both expected.
- The imported-photo marker's **anchor is its centre**, not its bottom tip.

### The lat/long override does not reach the map — PATH A ONLY

⚠ **This whole subsection applies only to Path A.** On Path B the CSV
coordinates are honoured exactly and none of the following is relevant — no
25 m check, no halt, no repositioning problem.

On Path A, a human lat/long override in `locations.csv` **does not reach the
map**. Google places the pin from EXIF, and `merge.csv` deliberately carries no
coordinates. The override does govern the CSV: `process_locations.py` keeps it
instead of back-filling from EXIF, and on Path B that CSV value is where the pin
lands. The script prints "using human-provided override position" whenever both
cells are filled, including values it back-filled itself on an earlier run, so
that message tells you nothing about the map.

**An agent CAN reposition a pin** (VERIFIED #28–#29, tested on v5, 13 Sep). The
pin moved 50.4 m south and kept all 3 photos.

1. Work in the visible, active tab, in the editor (`/maps/d/edit`).
2. Take a screenshot and locate the marker. Work out the offset: at zoom 18 near
   Yeppoon, 1 CSS px ≈ 0.55 m. Convert CSS px to screenshot px with
   `innerWidth / screenshot width`.
3. In ONE `browser_batch`: `left_click` on the marker, then `left_click_drag`
   from the same point to the target. That is the human's gesture, a rapid
   double-click with the second press held. The two presses must land together.
4. Wait 8 s. Read the balloon's live lat/long, then confirm with the KML a
   minute later.

**These do NOT move a pin; they pan the map** (6 Sep): `left_click_drag` on its
own, hover-then-drag, and synthetic mousedown/mousemove/mouseup events.

So: if the override differs from the hero photo's EXIF by **more than ~25 m**,
**stop and flag it for a human**, rather than silently shipping a misplaced pin.
Do not record the location as done. (This rule was written when no agent could
move a pin. Whether an agent should now move the pin itself is OPEN: canon P9.)

⚠ **Actually run this check, per location, and print the numbers.** On
2026-09-06 an operator told a sync agent "the check is already done for all 5,
none exceed 25 m", having only run it for one. Two pins were in fact 42 m and
75 m out. An assurance that the check was done is not the check. If someone hands
you the result, re-run it anyway — it costs seconds.

Useful while checking:
- The pin balloon shows the pin's **live lat/long** next to the action icons.
- Typing `-23.25593, 150.8257` into the editor's **search box** drops a marker at
  exactly those coordinates and recentres the map, so you can see the gap.

## 3. Rename the pin to `location_id`

**Use the data table, not the pin balloon:** layer **⋮ → Open data table** puts
every pin in one grid — double-click the name cell, ctrl+a, type, Enter, next row.
The pin/pencil/Save path constantly loses focus to the map's re-centring
animation.

⚠ **Check you are on the right row.** A rename landing one row high silently
gave one pin another location's id. Verify against the KML export before merging.

This is the match key for step 4.

## 4. Merge metadata

- Use the `merge.csv` from `plan_sync.py`. It carries
  `location_id,name,description,category,rating,icon` and **no coordinates**.
- **Never put latitude/longitude in a merge CSV.** It destroyed every pin on the
  test map and they did not come back.
- Upload `merge.csv` to **Google Drive** first (the picker's own Upload tab is
  the blocked iframe — see the top of this file).
  - **Give it a unique name**, e.g. `merge-<location_id>.csv`. Drive allows
    duplicate filenames, so a plain `merge.csv` from an earlier run leaves two
    indistinguishable files in the picker and you can silently merge the stale
    one — the exact failure `--only` exists to prevent.
  - `file_upload` **refuses paths outside the session's readable directories** —
    stage the CSV inside the project directory, not a scratch folder.
- In My Maps: layer **⋮ → Reimport and merge → Merge matching items** → **Google
  Drive** → **double-click the file, which goes straight to the column-match
  screen** (there is no Insert step).
  - ⚠ That ⋮ menu also holds **"Delete this layer"** two rows above "Open data
    table", and **"Reimport"** directly above "Merge matching items". Read before
    clicking.
- **Column matching:**
  - **First merge on a pin:** Layer data `name` = Uploaded data `location_id`.
    Only `name` and `description` exist as layer columns yet.
  - **Every later merge:** Layer data **`location_id`** = Uploaded data
    `location_id`. The first merge **overwrites the pin's name** with the CSV's
    `name`, so `name` is no longer the key — but the merge *adds* `location_id`
    as a layer column, which is what you match on from then on.
  - The confirm button is **Finish**, not "Merge".
- Confirm the toast reads "Layer was updated with new content".

## 0b. Style the layer by `icon` (once per layer, after the first merge)

- The control is the **"Individual styles"** link under the layer name — there is
  no control labelled "Style". → **Group places by** → **`icon`** → **Categories**.
- With one distinct value present, **Ranges is greyed out ("Not available")**,
  Categories is already selected, and a yellow warning appears: *"There are not
  enough distinct values in your data set for this styling method."* **Not a
  failure** — the grouping applies.
- With several values Ranges *is* the default and silently buckets them together.
  If two icons share a group, this is why.

## 0c. Assign an icon to each style group (recurs per new icon value)

- **The paint-can only renders on hover, has no accessible name (`find` will not
  return it), and sits ~9 px from the group label.** Hover the group row, then
  `zoom` to locate it precisely. Clicking a few px off opens the pin balloon.
- Paint-can → **More icons** → the **"Custom Icon" button, bottom-left** of the
  "Choose an icon" dialog. Not the **"Custom icons" tab**, which is the reuse
  library of already-used images.
- Left-nav item is labelled **"Photos"**, not "Google Photos".
- **No album browsing, no filenames** — the picker dumps the library in date
  order. Type `untrapped-icons` into **"Search Google Photos"**; it narrows to
  the 12 icons plus the occasional false positive. Fuzzy text search, not an
  album filter.
- Identify by eye, since filenames are invisible:

| Family | Shape | Glyph | Rating colour is |
|---|---|---|---|
| parking | blue teardrop pin | white **P** | small dot, bottom-right |
| toilet | blue teardrop pin | white **T** | small dot, bottom-right |
| route | circle | white *leaning* wheelchair | the whole circle |
| venue | rounded square | white *seated* wheelchair | the whole square |

Parking and toilet differ by **one letter** at 128px. Check the glyph.

- Then click **Insert** in the picker, then **OK** in the "Choose an icon"
  dialog. Both are easy to miss.

A group only exists once its icon value is in the layer's data, so you cannot
pre-assign all 12. Expect to return here when a new value first appears.

**After 0b, individual pins disappear from the layer panel** — only style groups
are listed. The only way to open one is to click its marker. Navigating to
`edit?mid=<MID>&ll=<lat>,<lng>&z=19` puts the pin you want at map centre.

## 5. Extra photos → per-location Drive folder

- Drive → **New → Folder** named `<location_id>`. Upload the non-hero photos from
  `processed/<location_id>/`. The input takes **multiple files** — but **split
  them into pairs**: four photos can total 9.9 MB against a 10 MB cap, which is
  far too close.
- Pin → camera icon (**third of five**; the fifth is delete) → **Google Drive** →
  **double-click** into `<location_id>` → click one photo → **Insert** → **Save**.
- **The Drive picker resets to My Drive root every time it opens** — re-navigate
  for each photo. It is single-select (ctrl+click deselects rather than adding).
- **Much faster: the "+" beside the photo carousel.** Once in the pin's photo
  editor it reopens the picker *without leaving edit mode*, so you can add every
  extra photo and **Save once**, instead of a camera/Insert/Save cycle per photo.
  Roughly 3x fewer round-trips.
- The pin popup **stays open** after Save; click the camera icon again.

## 6. Mark done — manual, no script does this

Edit `locations.csv` by hand: `status=done`, and `synced_photos` set to the
comma-joined filenames **wrapped in double quotes** (it contains commas):

```
...,done,"IMG_5339.jpg,IMG_5340.jpg,IMG_5341.jpg"
```

Some rows have a **single space** in the `synced_photos` cell rather than being
empty — replace the cell, don't append to it.

`plan_sync.py`'s docstring and STATUS.md both imply a script maintains these.
Neither does. Re-run `python plan_sync.py` to confirm the row is now skipped.

## 7. Stale address card, then publish

**Remove the "Details from Google Maps" card.** The pin was created by
reverse-geocoding, so it carries a business name or street address that is
usually wrong for the feature being described. Open the pin and use the card's
**Remove** link.

**The card is usually scrolled out of view** in a tall balloon — scroll the
balloon body before hunting for Remove. Presence check:
`document.body.innerText.includes('Details from Google Maps')`.

The editor keeps showing this card until you remove it — it does **not** hide
itself after a merge. (An earlier version of this runbook claimed it did; that
was wrong and could not be reproduced.) Verify removal on the **viewer**, where
the published `window._pageData` should contain no address string.

**Publishing:**

- There is **no "Publish to the web"** anywhere. The map ⋮ menu contains: New
  map, Copy map, Open a map, **Move to Bin**, Set default view, Embed on my site,
  Export to KML/KMZ, Print map. **Move to Bin is the 4th row — do not go hunting
  for "Publish" in this menu.**
- Publish via **Share** → toggle **"Anyone with this link can view"**.
- The Share dialog has a **second toggle, "Let others search for and find this
  map on the internet"**. Leave it **off** unless the map is meant to be
  publicly discoverable.
- Verify on the **viewer**, never the editor:
  `https://www.google.com/maps/d/viewer?mid=<MID>`
- On first publish, edits already made appear immediately.

**Verification.** The editor renders markers at **32px**; the public sees
**18px**. Anything judged in the editor looks ~1.8× better than reality.

The viewer's **`window._pageData`** holds the whole feature record — name,
description, every merged column, coordinates, whether an address is attached.
It is the reliable way to check step 7. (The *editor's* `_pageData` is `null`, so
this only works on `/viewer`.)

```js
[...document.querySelectorAll('img')]
  .filter(i => i.naturalWidth === 128)
  .map(i => ({ len: i.src.length, css: i.getBoundingClientRect().width }))
```

A custom marker reports `naturalWidth` 128 and rendered width 18.

**Best whole-map verifier — the KML export.** Read-only, no UI needed:

```
https://www.google.com/maps/d/kml?mid=<MID>&forcekml=1&cb=<timestamp>
```

It returns every placemark's name, coordinates and all merged `<Data>` columns,
so the whole `location_id` / coordinate / icon pairing can be confirmed in one
fetch.

⚠ **The KML endpoint is aggressively cached, and a query-string cache-buster is
NOT enough.** On 2026-09-06 an audit reported a deleted layer as still present,
several minutes after deletion, despite a `&cb=<timestamp>` parameter. That is
the dangerous failure mode: a confident, precise, wrong answer.

Always pass `cache: 'reload'` as well:

```js
fetch(kmlUrl + '&cb=' + Date.now(), { cache: 'reload' })
```

**And cross-check against the live DOM**, which cannot be cached:

```js
[...document.querySelectorAll('[aria-label="Layer options"]')].length
```

If the two disagree, **trust the DOM**. `window._pageData` on the viewer is
cached the same way.

## Per UPDATED location (status=update)

Steps 4–5 only. **Match on `location_id`, not `name`** (step 4). Use
`plan_sync.py`'s `photos_to_add` / `photos_to_remove`.

**Removing a photo:** pin → pencil → navigate the carousel (`< n of N >`) to the
photo → trash icon beside the displayed photo.

## Known friction

- **Google's picker "Upload" tabs are all blocked** (top of this file). Photos'
  and Drive's own upload buttons are the only automatable route.
- **Drive's "New" menu mis-fires while an upload toast is showing** — you land on
  Drive Home and lose your folder. **Dismiss the toast first**; that fixes it.
  Prefer `find` + ref clicks over coordinates.
- **Double-click** to enter albums and folders in every Google picker.
- **Screenshot coordinates are ~1.5× smaller than DOM/CSS coordinates** here
  (viewport 1738×958 vs screenshot frame 1159×639). Never mix
  `getBoundingClientRect()` values with screenshot coordinates.
- **Tabs occasionally freeze mid-screenshot** (CDP timeout) after a burst of
  interactions — wait and retry; a reload is rarely needed. Repeated blind clicks
  stack duplicate popups and corrupt the page.
- A full single-location sync is roughly **55 browser round-trips** and
  **50–70 minutes**.

## Icon verification — KML CANNOT DO THIS (found 2026-09-07)

**Every placemark in the KML export reports the stock icon
`503-wht-blank_maps.png` no matter what custom icon is actually applied.**

This is the most dangerous inaccuracy found so far, because it fails *silently
and confidently*: you get a clean, well-formed export that says all pins are on
the default marker while the screen plainly shows custom icons. An agent
trusting it will "fix" work that was never broken, or report a completed job as
not done.

KML remains reliable for names, coordinates, `<Data>` columns and
`gx_media_links`. For ICON STATE it is useless.

Verify icons instead by:
  - the layer-panel row's icon `background-image` (its byte length fingerprints
    each distinct icon), or
  - a screenshot. For a whole-map check a screenshot is faster and more
    honest than DOM archaeology — My Maps recycles marker elements, so a DOM
    scan that worked a moment ago can return zero on the next call.

## The paint-can does not need coordinate clicking

Earlier guidance said to hover and `zoom` to land within ~9px. Not needed. The
paint-can is `child[2]` of each layer-panel row
(`.un1lmc-pbTTYe-ibnC6b-DyVDA`) and responds to synthetic events, as do
"More icons", the icon tiles, and "OK". This removes coordinate drift and panel
scrolling from the whole job.

Note the CSS `:hover` limitation still stands for *revealing* hover-only
controls — but the paint-can can be actioned directly without being revealed.

## The custom-icon picker is SINGLE-SELECT

Selecting several icons at once silently keeps only one ("1 selected"). The
multi-select behaviour documented for the step-2 photo picker does NOT apply
here. The failure is invisible — no error, no warning.

Also: no Photos search is needed. Newly uploaded icons sit at the top of the
grid, and the picker remembers the Photos tab, so a repeat import is 3 clicks.

## Geometry-less placemarks are invisible in the layer panel

A placemark with no `<Point>` (e.g. `<Placemark><name/></Placemark>`) does not
appear in the layer list at all. It surfaces only in the DATA TABLE, announced
by a "N rows couldn't be shown on the map" banner. Open the table through that
banner, then right-click the row -> **Delete row**. The layer ⋮ menu offers no
route to it.

## KML caching — confirmed, and worse than documented

Immediately after deleting a placemark, KML still reported the OLD counts
(88 placemarks, TOILETS 20) despite BOTH `cache: 'reload'` AND a cache-buster
query param, and caught up roughly a minute later. The DOM was correct
instantly. "Trust the DOM for anything you just changed" is validated — treat
it as a rule, not a precaution.
