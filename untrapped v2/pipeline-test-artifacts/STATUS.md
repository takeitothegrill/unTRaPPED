# unTRaPPED V2 — My Maps pipeline feasibility testing — STATUS

Last updated: 2026-09-04 (paused mid-session, partway through TEST 3 Pass 2)

**If you are a fresh agent/session picking this up: read this whole file before doing
anything. Do not re-run TEST 1 or re-derive the restructure/audit — they're done.**

## Where this fits

Part of the unTRaPPED V2 re-scope: Google My Maps, no downloadable app, owner-only
pins, lived-experience framing (not building-code compliance). See:
- Repo root `README.md` (the unTRaPPED repo split into `untrapped v3/` parked +
  `untrapped v2/` active, commit `2c98c2e`).
- Canon `my-brain-context/projects/untrapped.md`, Decision Log entry 2026-09-03.

**Per explicit instruction: do NOT build the real pipeline until these 3 feasibility
tests are fully answered.** This folder is scratch/test-only, git-ignored
(`untrapped v2/.gitignore`), not part of the eventual build.

## Already fully done (don't redo)

- unTRaPPED repo restructure — committed, verified, history preserved via `git mv`.
- `untrapped-site` audit — map embed is an iframe, `mid=1mOXyoupEm3Pc8QmL-Yvrxrqt9eIsG48`;
  V1 pin icons are PNG-only, no vector source anywhere; site live on Vercel.
- Canon `untrapped.md` updated with the 2026-09-03 Decision Log entry.

## TEST 1 — EXIF coverage: PASSED, conclusively

Ran `scripts/exif_scan.py` (JPG/PNG) then `scripts/exif_scan2.py` (HEIC-aware, needs
`pillow-heif`) on real files:
- Canon-referenced V1 photo trove (55 mixed files): camera originals 17/17 = 100% GPS;
  non-camera files (screenshots, exports, AI-generated icons) near 0%.
- The 4 real test ZIPs (see below): **14/14 HEIC photos = 100% GPS + 100% date**, all
  Apple iPhone 11, coordinates landed exactly on the labelled real-world spots.

**Conclusion: iCloud "unmodified/original" downloads reliably carry full GPS+date.**
`scripts/heic_to_jpg.py` converts HEIC→JPG preserving EXIF — verified 100% GPS-intact
after conversion on 5 test files. GPS is only lost on non-original files (screenshots,
re-exports, messaging-app copies) — the real pipeline needs a "no GPS → manual position"
fallback for stray non-originals, not as the default path.

## Real test source files

Still sitting in the user's **Downloads** folder (not duplicated here — re-extract if
needed):
```
280811 emu street - parking - LIVINGSTONE.zip
280831 multi-story carpark - parking - LIVINGSTONE.zip
280903 stocklands shopping centre - parking - ROCKHAMPTON.zip
280901 yeppon family practice - toilet - LIVINGSTONE.zip
```
Naming convention: `YYMMDD location - category - LGA`.

**Bug found:** the ` - ` delimiter collides with hyphenated location names (e.g.
"multi-story carpark" broke a naive parser). Recommend a different delimiter, or —
better — drop per-file naming entirely once the real pipeline exists; carry
location/category/rating/description as **CSV columns** instead, and let the filename
just be the stable photo key (`IMG_####` is already unique).

Each ZIP also contains `.MOV` videos (5 total) — not usable for My Maps pins, out of
scope for this test.

5 representative HEIC files were converted to JPG (`photos-jpg/`, EXIF preserved):

| File | Real-world spot | Ground-truth GPS (from EXIF) |
|---|---|---|
| `IMG_5425.jpg` | Emu St parking bay, shot 1 | -23.256742, 150.827622 |
| `IMG_5426.jpg` | Emu St parking bay, shot 2 (~20s later) | -23.256794, 150.827592 |
| `IMG_5482.jpg` | Yeppoon multi-storey car park | -23.129442, 150.748353 |
| `IMG_5490.jpg` | Yeppoon Family Practice accessible toilet | -23.127769, 150.744019 |
| `IMG_5497.jpg` | Stocklands Rockhampton undercover parking | -23.353039, 150.522628 |

Full extracted metadata for all 14+5 files: `csv/test3-metadata.csv`.

## TEST 2 — CSV import + style-by-category: MIXED, one real product bug found

Test file `csv/untrapped-mymaps-test.csv` (5 rows, `name,latitude,longitude,description,category`
1–5) imported clean into a throwaway My Maps layer. Confirmed: Google uses the **literal
lat/long values** — does not geocode by name, does not swap columns. Good, mechanism is sound.

**RESOLVED (2026-09-05).** The "1 and 2 merged into one bucket" bug was Google defaulting
the "Group places by → category" panel to **Ranges** mode (numeric bucketing). That same
panel has a **Ranges / Categories** radio toggle — switching to **Categories** gives
correct discrete per-value styling: confirmed `1-1 (1)`, `2-2 (1)`, `3-3 (1)`, `4-4 (1)`,
`5-5 (1)`, each its own group. Fix is a one-time setting per styled layer/column, no need
to change bare integers to text labels.

Aside: the 5 coordinates hand-typed into that test CSV (by Claude, guessing real Yeppoon
landmark locations) turned out to be imprecise — confirmed via the user's own manually-
placed "ACTUAL" comparison pins. **That was bad test data, not a Google import bug** —
production data will come from photo EXIF (proven 100% accurate in TEST 1), so this
failure mode doesn't recur for real.

**Not yet run:** "Reimport and merge → Add more items" — does a newly merged row
automatically inherit the category-based styling, or land unstyled? CSV ready:
`csv/untrapped-mymaps-addmore.csv` (1 row, category 6).

## TEST 3 — Two-pass photo approach: Pass 1 CONFIRMED WORKING. Pass 2 BLOCKED.

**How to actually get photos into My Maps (not obvious from Google's docs — figured out
by trial and error):**
- Layer → Import → **"Google Drive" tab**: only shows data files (CSV/XLSX/KML). A
  Drive folder containing only JPGs shows as **"This folder is empty."** Not usable.
- Layer → Import → **"Upload" button** (same dialog): outright **rejects image files**
  ("image files are not supported"). Not usable.
- Layer → Import → **"Albums" tab**: **this is the one that works.** Point it at a
  **Google Photos album** (not a Drive folder). We made one named `untrapped map test
  260903` and uploaded the 5 `photos-jpg/*.jpg` files into it.

Result: **all 5 photos auto-placed as pins, positioned from embedded EXIF GPS, using
the photo itself as the pin thumbnail/icon.** This confirms the core mechanism the
whole two-pass pipeline depends on.

Observations from that import:
- **Pin names are auto-set by Google reverse-geocoding to the nearest known business**
  (e.g. "Coastal Hill Cafe", "Bendigo Bank") — **not** derived from the filename. Expected
  default behaviour, but a real problem for Pass 2's filename-based merge (see below) —
  had to manually rename pins first.
- `IMG_5425` and `IMG_5426` (Emu St, ~5m / ~20s apart) both reverse-geocoded to the same
  "Coastal Hill Cafe" label → **2 separate pins, not auto-merged.** Confirms: multiple
  photos of one physical spot = multiple pins by default. Real-workflow decision needed
  later — one photo per assessed feature, or accept + manually combine multiple pins.
- Small (~few metres) position drift observed on at least one pin vs. a manually-placed
  comparison marker. Normal phone-GPS precision — not a defect, nothing to fix.
- The Google **Drive** folder `untrapped map test 260903` (same 5 JPGs) is a dead end for
  photo import — don't confuse it with the **Photos album** of the same name, which is
  the one that actually worked.

### Pass 2 — ONE CONFIRMED DESTRUCTIVE FAILURE. Second attempt was NOT independent — needs a clean retry.

1. Manually renamed each of the 5 imported pins' "Name" field to its real photo key
   (`IMG_5425` / `IMG_5426` / `IMG_5482` / `IMG_5490` / `IMG_5497`). Worked fine.
2. Ran **⋮ → Reimport and merge → Update matching items** with `csv/test3-pass2.csv`
   (includes `latitude`/`longitude` columns). The "Select column to match places" dialog
   appeared (previously unseen) — matched **Layer data `name` = Uploaded data `photo_key`**.
3. Result: **"5 rows couldn't be shown on the map." → "Open data table"** revealed the
   match itself had actually worked — all 5 rows showed the correct updated `name`,
   `description`, `category`, `photo_key` from the CSV — but the rows failed to *render*
   on the map, and after dismissing, **the 5 original pins were gone and never came back.**
   **Confirmed destructive on this one data point.**
4. **CORRECTION (caught by the user, 2026-09-05):** the second retry, using
   `csv/test3-pass2-nolatlon.csv` (lat/lon columns removed), was run **after** the pins
   from step 3 were already gone — i.e. against an already-broken layer, not a clean
   baseline. **This was NOT an independent test.** Getting the same "couldn't be shown"
   error again is unsurprising (there was nothing valid left to merge onto) and does
   **not** actually rule out the lat/lon hypothesis. Struck the premature "ruled out"
   conclusion that was here.

**Real state: only ONE genuine data point exists (step 3, with lat/lon, destructive).**
The lat/lon-conflict hypothesis is still open, untested cleanly.

**⚠️ Confirmed operational risk regardless of root cause:** that one real attempt
**permanently destroyed 5 working pins** rather than failing safely. **Never attempt this
merge on the real production map without a duplicate/backup copy of the map first.**

**RESOLVED (2026-09-05): CONFIRMED ROOT CAUSE, CONFIRMED FIX.**

Redid Pass 1 cleanly (Add layer → Import → Albums → same `untrapped map test 260903`
Photos album) → fresh 5 pins with correct auto reverse-geocoded names → carefully
renamed to unique `IMG_5425` / `IMG_5426` / `IMG_5482` / `IMG_5497` / `IMG_5490` (caught
and fixed a duplicate-rename mistake before running the test — checkpoint screenshotted).
Ran **exactly one** merge: `csv/test3-pass2-nolatlon.csv` (no lat/lon columns), matching
`name = photo_key`.

**Result: SUCCESS.** All 5 rows matched and updated correctly — `name`, `description`,
`category`, `photo_key` all show the CSV's content, and critically **the photo thumbnail
survived the merge** (verified on the checked pins) — Google's own claim ("matched
features retain photos and custom styles") holds. No data loss this time.

**Root cause confirmed: including `latitude`/`longitude` columns in an "Update matching
items" merge onto photo-imported placemarks is what caused the earlier destructive
failure.** Fix is simple: never include position columns in a merge-update CSV — the
photo-derived position is already correct and doesn't need resupplying.

Minor cosmetic note: merged pins still carry a leftover **"Details from Google Maps"**
block (the real nearby business's address/phone/rating from the original auto-geocode).
Doesn't conflict with the custom fields, but should be manually removed (there's a
"Remove" link right on it) for real production pins so it doesn't confuse readers.

**TEST 3 is now a full PASS: Pass 1 (photo → pin via EXIF, through Google Photos Albums)
+ Pass 2 (CSV merge to add metadata, with lat/lon columns excluded) both work, and photos
+ styling survive the merge.**

### Fallback test — bare image URL in description: DONE (2026-09-05)

**Result: the URL linkifies as plain clickable blue text. It does NOT render as an
inline image thumbnail.** Confirmed on a fresh plain CSV-imported layer
(`csv/test3-fallback-imageurl.csv`).

Useful, not a dead end — see the hybrid recommendation below. A plain CSV-only import
(no Photos-Albums step) also confirmed it does **not** pick up the stale "Details from
Google Maps" business-card side effect that photo-imported pins get — that side effect
is specific to the Photos-Albums import path.

## Human workflow & master CSV design (2026-09-06)

Worked through the actual end-to-end human workflow with the user. Settled design:

**Capture:** human takes photos on phone. Originally planned: on the **first (hero)
photo** of each batch, manually adjust GPS location in iPhone Photos ("Adjust Location")
if drift/indoor signal is a concern.

**TESTED (2026-09-06), inconclusive — DECIDED NOT TO PURSUE.** Two attempts: (1) user
adjusted a Queensland photo's location to a Victoria hotel, exported, sent — EXIF still
showed the original Queensland coordinate. (2) User tried again with a New Farm,
Brisbane adjustment, sent 2 more exports — but all 3 files across both attempts were
**byte-for-byte identical (same SHA256 hash)**, meaning no fresh export actually happened
each time; the export path was serving a cached copy, not re-exporting after the edit.
Root cause (sync timing, wrong export method, or something else) never isolated.

**DECISION: not worth chasing further — use the CSV override instead.** Human may
pre-fill `latitude`/`longitude` directly in the master CSV (e.g. by looking up the
address on Google Maps) for any problem case (indoor shots, bad auto-GPS, etc.); the
script only pulls from the photo's own EXIF when those cells are left blank on a new row.
Reliable, human-controlled, no dependency on unverified phone-app/export behaviour.

**Master CSV** (not a per-folder .txt file — this supersedes that earlier idea) is the
single source of truth for what's on the map:

| Column | Filled by | Purpose |
|---|---|---|
| `location_id` | Human (= the photo folder name) | Stable unique key |
| `name` | Human | Pin title, e.g. `TOILET - disabled [EXCELLENT]` |
| `description` | Human | Free text (templated sections e.g. STOMA HOOK: yes/no) |
| `category` | Human | One of the 7 TRAPPED types → determines icon glyph |
| `rating` | Human | green/orange/red → determines icon colour |
| `latitude`, `longitude` | **Human (optional override)**, else **script** after processing | If human pre-fills these, script uses them as-is (for indoor/problem locations). If left blank, script backfills from the hero photo's EXIF after processing. |
| `status` | **Human/operator writes both** | blank = untouched; `update` = explicit signal to (re-)process this row; `done` = written **by hand** after a successful sync. **No script writes this** — see correction below. |
| `synced_photos` | **Written by hand** | Comma-separated filenames last pushed for this location — read by `plan_sync.py` on `status=update` runs to diff the current folder against what's on the map. **No script maintains it.** |

**On `status=update`:** the operator re-pushes name/description/category/rating (trusts
the human that something changed, no need to guess), and `plan_sync.py` diffs the current
folder vs `synced_photos` to report `photos_to_add` / `photos_to_remove`.

**CORRECTION (2026-09-06, found by the fresh-agent retest).** The two rows above
previously said the *script* writes `status=done` and maintains `synced_photos`.
**It does not, and never did.** `plan_sync.py` only ever reads `locations.csv`;
nothing in the pipeline writes to it. Step 6 of the runbook is a manual edit. Three
documents disagreed on this — the runbook, this table, and `plan_sync.py`'s docstring —
which is exactly the kind of drift a fresh reader has no way to resolve.

**Photo removal — CONFIRMED (2026-09-06)**, user demonstrated live: open the pin's photo
carousel → click the pencil/**Edit** icon → a trash icon appears next to the currently
shown photo → click it to remove just that photo, pin and remaining photos stay intact.

**Category taxonomy — DECIDED:** the original 7 TRAPPED types (Toilets, Ramps,
Accessibility, Pathway, Parking, Elevators, Doors) determine the icon **glyph**. A
separate `rating` (green/orange/red, i.e. fully-accessible / at-your-own-risk /
hazard-missing) determines the icon **colour**. Confirmed fully flexible to add/change
either axis later — My Maps' "Categories" style mode auto-creates a new group whenever a
new value appears in the data, and the category→icon mapping lives in the local script's
config, not hard-coded into the platform. Live site's current 5-icon set (which conflates
type+rating into one flat list) is being superseded by this 2-axis design for V2, not
carried forward as-is.

**Known open edge case, not yet decided:** hero-photo replacement/repositioning after a
pin already exists — the tested merge workflow explicitly cannot touch position. Default
assumption for now: not auto-handled, would need manual pin-drag or delete-and-recreate.

## Multi-photo / stale-address trade-off — RESOLVED, hybrid recommendation

Two real product limitations surfaced by the user while testing (2026-09-05), both now
fully diagnosed with a concrete design answer:

**1. Only one photo attaches per pin via bulk import (Photos-Albums treats each photo
file as its own separate point).** Native fix exists — a pin's photo viewer shows "1 of
N" with a "+" to manually attach more photos to the *same* point — **confirmed working**
by the user. But the "add more" picker only offers "Photos" (all personal photos, date
order, no album filter) — **impractical at real scale** (no way to quickly find "this
pin's 2nd photo" in a chronological camera roll). A "Google Images" tab also exists in
that picker — untested, almost certainly unrelated generic web image search.

**2. The auto-attached "Details from Google Maps" business card (from Photos-Albums
import's implicit reverse-geocode) is wrong, has a "Remove" link but no auto-update, and
persists even after manually dragging the pin to the correct spot.** Confirmed: this
side effect is specific to the Photos-Albums import path — a plain CSV-only imported pin
never gets one.

**Recommended hybrid design (given full picture of both trade-offs):**
- Use the proven **Pass 1 (Photos-Albums import) + Pass 2 (CSV merge, lat/lon columns
  excluded)** pipeline to attach **one native hero photo per pin** — this is the only
  path that gets a real inline-rendered thumbnail in the balloon. Accept the one-time
  manual "Remove" click per pin to clear the stale address card as the cost of that.
- For **additional context photos** per feature (stoma hook location, door width,
  turning space — real accessibility-audit needs raised by the user), don't fight the
  by-date photo picker. Put them as **labelled clickable links directly in the
  `description` text** (e.g. `Turning space: [url] · Stoma hook: [url] · Door width
  (68cm): [url]`) — proven to work (linkifies, clickable), and — unlike the native
  gallery — lets every photo carry its own caption, which is the actual point for an
  accessibility audit (an unlabelled photo of "the door" is nearly useless).

**Correction/addition (2026-09-05, after report was first drafted):** the "Google Drive"
tab in the **per-pin "+" add-a-photo** picker (not the layer-level bulk Import dialog —
that one still only recognizes CSV/XLSX/KML, confirmed unchanged) genuinely works, and
works on **already-imported** pins too, not just freshly manually-dropped ones. Since a
Drive folder can be organized however you want (unlike the flat by-date "Photos"
picker), this is a real, usable manual source for attaching extra photos — still one at
a time, no multi-select, but far more findable than scrolling a camera roll.

**User sketched a future capture-app workflow using this:** location shared from Apple
Maps → photo taken through a future unTRaPPED GUI → GPS metadata attached → photos
uploaded to a *unique Drive folder per feature* → system bulk-imports the first photo via
Photos-Albums (GPS + hero photo, no automation needed) → remaining photos attached one at
a time via the per-pin Drive picker, navigating to that feature's small unique folder.

**Open architectural fork — not decided:** the last step (repetitive per-pin Drive
click-through for extra photos) is a plausible candidate for browser automation
(Claude driving the browser), but that reintroduces exactly the maintenance-cost
trade-off the original brief asked to be flagged honestly if the no-automation path
didn't fully suffice: no known public API for editing My Maps features (this would be
screen-driving the consumer UI, not calling an API), fragile to Google UI changes, and
this session already hit real Claude-in-Chrome connectivity/auth problems. The
already-proven, zero-automation alternative (labelled links in the description, see
above) solves the same underlying need (multiple *labelled* photos per feature) without
any of that fragility — just without a native inline gallery.

**DECIDED (2026-09-05): user chose the native-gallery-via-automated-Drive-click-through
route**, accepting the maintenance/fragility trade-off for the more polished result
(real inline swipeable photo thumbnails per pin). Labelled-links-in-description was
explicitly offered as the safer default and declined. This means the eventual build
includes a browser-automation component (Claude driving the browser through Google's
consumer My Maps/Drive UI, per-pin, per-extra-photo) — not just a local script. Whoever
builds this should re-verify Claude-in-Chrome connects reliably before relying on it,
since this session hit real connectivity/auth problems with that extension.

**Future idea, not actionable now:** a future unTRaPPED photo-capture app could prompt
for specific standard shots per category (e.g. "now photograph the stoma hook", with a
Skip option) and auto-populate the description ("No stoma hook present") when skipped —
directly generating the labelled-link content above at capture time. Also worth testing
later: iPhone Photos' native per-photo "caption" field — may be readable via EXIF/XMP
and could double as the photo's label in the pipeline, removing a manual-typing step.

## Multi-photo-per-pin investigation (2026-09-05, prompted by user's real accessibility-audit need)

User's real requirement: a single assessed feature (esp. toilets) often needs several
*labelled* photos — turning space, stoma-hook location, door width — not just one
generic shot, and not an anonymous unlabelled gallery either (viewer needs to know what
each photo is showing).

- **Native multi-photo carousel: confirmed it exists.** A pin's photo viewer shows
  "1 of N" with a "+" to add more — you CAN attach multiple photos to one pin manually.
- **But the picker for "add more photos" only offers "Photos" (all personal photos, date
  order) — no "Albums" filter.** Confirmed by the user. At real scale (dozens/hundreds of
  pins) this is impractical — no way to quickly find "this pin's 2nd/3rd photo" in a
  chronological camera roll. Native gallery is a real capability but not a usable bulk
  workflow.
- **A "Google Images" tab also exists in that same picker** — untested, but almost
  certainly generic web image search, unrelated to personal photos. Not pursued.
- **Recommended real solution: multiple captioned image URLs inside the `description`
  text** (e.g. "Turning space: [url] · Stoma hook: [url] · Door width (68cm): [url]").
  This solves the *labelling* problem the native gallery can't (no per-photo captions
  there) and could work at any scale via the same CSV pipeline. Depends on whether a
  bare image URL actually renders inline vs. just linkifies — see fallback test below.
- **Future idea (not actionable now, logged for later):** a future unTRaPPED photo-capture
  app could prompt for specific standard shots per category (e.g. "now photograph the
  stoma hook", with a Skip option) and auto-populate the description ("No stoma hook
  present") when skipped. Also: iPhone photos support a native per-photo "caption" field
  in Photos' own metadata — worth testing later whether that's readable via EXIF/XMP and
  could double as the photo's label in the pipeline.

## Browser-automation half — BUILT AND PROVEN LIVE (2026-09-06)

Built `pipeline/plan_sync.py` (reads `locations.csv` + `processed/`, computes
new/update/blocked work) and `pipeline/RUNBOOK.md` (the exact validated
procedure). Then **executed the full runbook live via Claude-in-Chrome** for
one real location (`emu-street-parking`) end to end, on the disposable
`untrapped v4` test map — not just designed, actually run and verified:

1. Uploaded the hero photo to a fresh Google Photos album (found the
   real `<input type=file>` that briefly exists in the DOM after clicking
   Photos' "Select from computer" — same-origin, automatable, unlike
   My Maps' own CSV-upload widget which is a cross-origin iframe).
2. Photos-Albums import → pin created, correct position from EXIF.
3. Renamed the pin to `location_id` (`emu-street-parking`).
4. Uploaded a merge CSV to Google Drive first (workaround for the
   cross-origin iframe), then Reimport-and-merge → Merge matching items,
   matched `name = location_id`, category as numeric — **no lat/lon in the
   CSV**. Result: "Layer was updated with new content", no destructive
   failure. Verified name/description/category/photo all correct.
5. Created a per-location Drive folder, uploaded the 3 extra photos
   (one at a time — `file_upload` caps at 10MB/call), attached each to the
   pin one at a time via the camera-icon → Google Drive picker (confirmed:
   single-select only, no way to multi-select). Final pin: "4 of 4" photos.
6. Updated `locations.csv`: `status=done`, `synced_photos` = all 4
   filenames. Re-ran `plan_sync.py` — correctly shows this location as
   already-done and skips it, while the second (untouched) test location
   still shows as pending. **The full loop closes correctly.**

Also confirmed live: photo **removal** works exactly as expected (pencil/
edit icon on the carousel → trash icon next to the shown photo).

This is proof the runbook is accurate and executable by Claude driving the
browser, not just a theoretical design. See `pipeline/RUNBOOK.md` for the
exact steps and the friction/gotchas worth knowing before a future run
(iframe-vs-native-input inconsistency across Google products, occasional
CDP screenshot freezes needing a wait-and-retry, Drive's "New" menu being
easy to mis-click after a navigation).

## Custom pin icons — CONFIRMED WORKING (2026-09-06)

Question: can a pin use a fully custom icon (not just Google's built-in colour/glyph
pins or a photo thumbnail)? Tested live via Claude-in-Chrome (now connected) on the
`untrappedmymapstest.csv` layer's category style panel: click a style group → **"More
icons"** → **"Choose an icon"** dialog has tabs for Shapes/Sport/Places/etc, **plus a
"Custom icons" tab and a "Custom icon" button**.

**Confirmed sources for a custom icon:** Image URL, Google Photos, Google Drive, Google
Images, direct file **Upload** (drag-drop/browse — though that specific widget lives in a
cross-origin iframe Claude can't drive directly; a human click works fine), and Webcam.

**Tested end-to-end via Image URL** (`https://untrapped.au/assets/icon-toilet-red.png`,
one of the current live site icons) — inserted successfully and applied to the `1-1`
category style. Confirmed rendering in both the layer sidebar and on the map.

**CORRECTED 2026-09-07 — the earlier claim here was WRONG.** This section previously said
"Google auto-composites the uploaded image into its own pin-drop frame, so a redesign only
needs the circular glyph, not a pin shape." That was a misreading of the upload preview.

**The truth: Google renders the uploaded artwork exactly as drawn. It adds nothing.**
Proof: `icon-toilet-red.png` was never a plain circle — opening the file shows it already
contains its own black teardrop pin shape with a red circle inside. What appeared on the
map was simply that image, unmodified.

**Consequences (these matter for the designer):**
- The icon set must draw its **own** full shape (pin / circle / square). Nothing is added.
- Every transparent pixel of margin in the source file is **wasted map real-estate**.
- Measured in the live viewer DOM: custom markers render at roughly **18–21 px on screen**
  (a 128x128 source displays at 18x18; a 64x64 source displays at 21x21). Source resolution
  affects *sharpness only*, never displayed size. Design decisions must be made against an
  ~18px target, not against the 256px or 512px canvas.

Side finding: previously-used images (including the small grey photo thumbnails from the
Pass 1 photo-import tests) already appear under the "Custom icons" tab, reusable without
re-uploading — Google keeps a running library per map.

### SVG custom icons — ACCEPTED, but RASTERISED. No vector benefit. (2026-09-07)

Vector artwork would have removed the sharpness ceiling entirely, so it was worth testing
properly. Test file: `icons/output/svg-test-parking-green.svg` (240x240 viewBox, blue pin,
white P, green rating dot).

- **Via Google Drive: fails.** The SVG uploads to Drive fine and Drive renders a thumbnail,
  but the file **does not appear in My Maps' custom-icon Drive picker** at all.
- **Via Google Photos: works.** Uploaded to Photos, selected in the custom-icon dialog,
  applied to a category style, renders correctly on the map.

**CORRECTION — an earlier conclusion here was over-broad.** On the strength of the Drive
result alone this was written up as "SVG is rejected — definitively." The user falsified
that by doing it via Photos. Testing one path and generalising to the format was the error.

**But the vector benefit is not real.** Inspecting what the map actually serves for that
styled pin:

```
naturalWidth/Height : 128 x 128
src                 : data:image/png;base64,...   <- PNG, not SVG
```

Google Photos **rasterises the SVG to a 128px PNG on ingest**. The only true SVG element on
the page is a 24-viewBox Google UI glyph, unrelated to the map markers.

Identity of that marker was verified rather than assumed — the SVG and the PNG generator
place the rating dot in measurably different spots:

| | dot centre @128px | dot fill |
|---|---|---|
| SVG source (240x240, dot at 184,52) | 98.1, 27.7 | `#228B3C` |
| PNG generator (240x240, dot at 164,46) | 87.5, 24.5 | `#228B3C` |
| **Measured on the live map** | **97.5, 27.0** | **34,139,60** |

10px apart at 128px — far outside measurement error. It is the SVG-derived file.

**Settled conclusion: there is no route to more than ~128px of icon detail in My Maps.**
Neither source resolution nor source format changes it. Sharpness must be solved by
design — bold, simple, high-contrast shapes — not by file format. `DESIGNER_BRIEF.md` §4.3
now states this.

### Icon treatment — border / shadow / colour / glyph weight (2026-09-07)

Four amendments requested after seeing the draft set on the live map. All tested through
the real pipeline (512px artwork -> 128px Google re-encode -> 18px display), on both the
pale map background and a satellite-like busy background. Sheets:
`_border_shadow_test.png`, `_border_weight_test.png`, `_fluro_and_p_test.png`.

| Request | Verdict | Value |
|---|---|---|
| White border | **YES** | 28px on a 512 canvas (~1px displayed) |
| Drop shadow | **NO** — recommend against | costs ~2 of 18px, near-invisible |
| Fluro rating colours | **YES** | `#00E676` / `#FF9100` / `#FF1744` |
| Bigger, thicker glyph | **YES, with a ceiling** | black weight, 0.66 of head width |

Detail worth keeping:

- **Border weight is not a guess.** 14px (~0.5px displayed) vanishes in the downsample;
  42px (~1.5px) visibly eats the blue body for no extra separation. 28px is the sweet spot.
- **Border must be white, not dark.** A dark outline defines the shape well on the pale map
  but muddies badly against satellite imagery.
- **Border comes OUT of the shape.** Outer silhouette still fills the canvas; the blue body
  is inset by the border width. There is no room to grow outward.
- **The shadow request was reasonable and was tested properly, not waved away.** Google's
  markers do carry one. It fails here for a structural reason: a shadow needs margin to fall
  into, and margin is size we don't have. The white border delivers the separation the
  shadow was wanted for, at a fraction of the cost. Left in the brief as a recommendation
  the designer may overrule, not a veto.
- **Orange and red were brightened too, not just green.** Lifting only the green would make
  "good" the loudest signal on the map, which misleads at a glance.
- **Glyph size has a per-letter ceiling.** "P" fails above ~0.66 because its enclosed
  counter closes up in the downsample and it crowds the rating dot. "T" has no counter and
  holds to ~0.74. One number cannot be applied to both.

Also settled this session: legend wording is **"barriers"** (not "last resort"), and
TRAPPED's **A - Accessible interior** maps to **Venues**. Both now fixed in the brief.

### Rating dot position — moved to BOTTOM-right (2026-09-07)

User flagged the dot as sitting too close to the shoulder of the "P" and suspected it
would clash with the "T". Both correct. Tested all four corners against both glyphs
(`_dot_position_test.png`) and against the Venue wheelchair (`_dot_position_venue.png`).

It is a letterform problem:

- **"P"** has its mass upper-left (stem) and upper-right (bowl). Lower-right is empty.
- **"T"** is the hard case — its crossbar occupies the ENTIRE top of the letter. A dot at
  top-right lands on the crossbar's right arm and eats it; at 18px it reads closer to an
  "F" than a "T". This is worse than the P problem that prompted the question.
- **Bottom-left** fails too — that is where the P puts its stem.
- **Bottom-right is the only corner genuinely empty in both letters.**

**Known trade-off, accepted deliberately.** The Venue wheelchair is not a letter: its
lower-right is the wheel, so bottom-right is contested there, and the Venue square in
isolation would prefer top-left. We still specified bottom-right for the whole set —
a rating signal that moves depending on icon type is one users must hunt for, and a fixed
corner is learnable. It is also the majority case: of the nine icons carrying a dot, six
are P and T (Routes carry no dot; they colour the whole shape). The brief asks the designer
to compose the Venue wheelchair to clear its lower-right instead.

### CORRECTION — Venues are rating-coloured, NOT blue (2026-09-07)

The brief had drifted and was specifying Venues as a **blue** square with a coloured rating
dot. **Wrong.** User caught it. The settled decision was that Venues take the rating colour
as the whole shape, exactly like Routes — from their own earlier reasoning: *"for venues...
red colour is enough, we don't need the slash. i am thinking the same for the routes. a red
wheelchair icon tells the story."*

The system is **two families**, not one rule with one exception:

| Family | Icons | Body | Rating carried by |
|---|---|---|---|
| Facilities you **hunt for** | Parking, Toilets | **always blue** | small dot, bottom-right |
| Things you **assess** | Routes, Venues | **green / orange / red** | the whole shape, no dot |

Why blue is reserved to Parking and Toilets: the user's own rationale — *"when people are
looking for such facilities i believe they will be looking for the colour blue on the map."*
That only applies to things you scan for. Nobody scans a map for "a venue" — you already
know the venue, and the only question is whether you can get in. So colour is free to carry
the rating there, and a fully coloured shape beats a 4px dot at 18px.

**Knock-on effects, all applied:**
- Only **six** of the twelve icons carry a rating dot (3 Parking + 3 Toilets).
- The §6.5 dot-position trade-off **disappeared**. It had been written up as "bottom-right
  is contested on the Venue wheelchair but we're standardising anyway" — with Venues
  dotless there is no third glyph to compromise for, so bottom-right is simply correct.
  Fig 8 (venue dot placement) was removed from the brief as testing something that no
  longer exists.
- The three fluro hexes now do double duty: the dot on facilities, the body on
  Routes/Venues. One palette, so a red venue and a red parking dot are the same red.
- New `_system_sheet.png` renders all 12 at actual size as a single visual check.

### Icon samples — three rounds, measured on the live map (2026-09-07)

Method that worked: don't judge artwork on the artboard or in My Maps' EDIT view (which
renders 32px). Pull the actual PNG Google serves out of the DOM, scan a line across it,
and downscale 128 -> 18 in-page. Every useful number came from that, not from the JPEG.

| | 1st | 2nd | 3rd (approved) |
|---|---|---|---|
| Canvas width used | 81% | 86% | 91% |
| Outlines | 2 | 2 | 1 (white only) |
| White border @128 | 2px | 2-3px | 3px (spec 7px) |
| Dot layers | 3 | 2 | 2 |

**Revised our own advice on the border.** After pushing it three rounds, tested whether it
still earned another: on the road map the difference is invisible (white on cream), on
satellite it is visible but modest. Called it — fold into a future round, don't spend a
round on it. Worth remembering as a pattern: a note repeated across rounds should be
re-tested for whether it still matters, not just repeated louder.

**Stem-length finding generalised.** The binding constraint on a glyph is its counter (the
enclosed hole), not the stem. Rule given: lengthen until the counter is about to close,
keep it >= ~40px on a 512 canvas (~1.5px on screen). The designer went shallower on the
bowl than our 0.52 number but compensated with a thinner stroke and wider bowl - the rule
held, the specific number did not need to.

### FRESH-AGENT RUNBOOK TEST — passed the task, failed the runbook (2026-09-07)

Clean map `untrapped v5 - runbook test` (mid `1xTLQzqrYdHsTqzgIu2Pdh7eAUmbs1lw`).
A fresh agent with no session context synced `spotlight-carpark-rockhampton`
end-to-end from RUNBOOK.md alone.

**Outcome: the agent completed the task** — pin placed, 3/3 photos, styled by
`icon`, published, viewer DOM confirms 128px source at 18px rendered. But it
found **19 runbook defects**, several serious. The runbook has been rewritten.

**Defects I had introduced that same day, unverified:**
- **"⋮ → Publish to the web" does not exist.** I asserted a UI path without
  checking. Verified afterwards: that menu is New map / Copy map / Open a map /
  **Move to Bin** / Set default view / Embed / Export KML / Print. Real route is
  **Share → "Anyone with this link can view"**. Worse, **Move to Bin sits two
  rows from where an operator hunting for "Publish" would click.**
- **Section 0 was labelled one-time-per-map but cannot be run that way.** 0b/0c
  need data in the layer first, and 0c recurs per new icon value, because a
  style group only exists once its value appears in the data.
- **"match them literally" was not executable** — the Photos picker shows no
  filenames at all.

**Pre-existing defects the test exposed:**
- **The UPDATE path was broken.** Step 4's merge *overwrites the pin name* with
  the CSV `name`, destroying the `name = location_id` match key. Every later
  merge must match `location_id = location_id` (the first merge adds that
  column). As written, a second sync would have matched zero rows.
- **The stale "Details from Google Maps" card reaches the public.** After a
  merge the editor balloon hides it, so it looks fixed — the viewer still shows
  a wrong business address. Now step 7.
- **The human lat/long override is inert.** Google places from EXIF and
  merge.csv carries no coordinates, so the override column never reaches the
  map, while `process_locations.py` still prints "using human-provided override
  position". Harmless here (~20 m) but not for the indoor/bad-GPS case the
  column exists for. Documented; not yet fixed in code.
- **`file_upload` is not one-file-per-call.** The inputs are `multiple=true`;
  12 icons went in one call. The real rule is 10 MB per call. The old wording
  cost ~12 needless round-trips.
- **"Before starting" commands didn't run** — both scripts are in `pipeline/`.

**Code changes made in response:**
- `plan_sync.py --only <location_id>` scopes merge.csv to one location. Without
  it, unmatched rows are **silently dropped by the merge with no error** — the
  same symptom as the historic destructive failure.
- Output now states that silent-drop behaviour explicitly.

**Method note worth keeping:** the fresh-agent test was worth far more than
re-reading the runbook myself. I could not see my own gaps — every one of the
three defects I introduced looked correct to me when I wrote it, and two were
pure assertion about UI I had not opened. Cost ~35-40 min and ~50 browser
round-trips.

### RETEST + Upload-path investigation (2026-09-06)

**Retest.** Second fresh agent, clean map `untrapped v6 - runbook retest`
(mid `189o4kIBKSx4yLasAOjdAVd42KIxhlb4`), location
`playground-swing-wheelchair-emu-park` (venue-red, 5 photos).

**The rewrite held.** Where the first run found the runbook broken, this one
found it correct but imprecise. The agent positively confirmed, verbatim: the
⋮ menu contents with no "Publish to the web" and Move to Bin 4th; Albums as a
nav item not a tab; double-click to enter pickers; the Ranges "Not available"
warning; the "Custom icon" button vs "Custom icons" tab; the `untrapped-icons`
search returning 12 + one false positive; the icon identification table; the
Drive picker resetting to root; single-select; the merge overwriting the pin
name and adding `location_id` as a column; editor 32px vs viewer 18px.

24 further defects found, all now fixed. The ones that mattered:

- **"Drag the pin by hand" is impossible for the intended reader.** This is a
  runbook for an automated session and it told the agent to do something by
  hand. Three methods tried (drag tool, hover-then-drag, synthetic mouse
  events) — **all pan the map**, pin coordinates unchanged. The lat/long
  override is therefore genuinely unsupported, not merely undocumented. Runbook
  now says: if the override differs from hero EXIF by >~25 m, **stop and flag
  for a human**; do not mark the row done.
- **Duplicate `merge.csv` in Drive root.** Drive permits duplicate filenames, so
  a stale `merge.csv` from an earlier run sits indistinguishably beside the new
  one in the picker — the precise failure `--only` exists to prevent. Now
  requires `merge-<location_id>.csv`.
- **A step-7 claim I had written did not reproduce.** I claimed the editor stops
  showing the stale address card after a merge while the viewer still shows it.
  The editor kept showing it every time. Corrected.

### Google picker "Upload" tabs — TESTED, dead end (2026-09-06)

The retest agent flagged the **Upload** option in both the custom-icon dialog
and the pin photo dialog as a possible shortcut that would delete Section 0a and
most of Step 5. Tested directly rather than assumed:

| Dialog | Upload panel | Reachable file inputs |
|---|---|---|
| Custom icon ("Choose a file to import") | Browse / drag-a-file | **0** — every frame cross-origin |
| Pin photo ("Choose an image or a video") | identical widget | **0** — every frame cross-origin |

Both are the **same Google picker component inside a cross-origin iframe** — the
same one that already blocks My Maps' CSV-import Upload tab. Zero inputs before
*and after* clicking Browse.

**Conclusion: Photos' and Drive's own upload buttons are the only automatable
upload routes that exist.** The runbook's architecture is correct and now carries
the reason, so no future agent needs to re-derive it. This is recorded at the top
of RUNBOOK.md precisely because it looks like it ought to work.

### Doc drift corrected (2026-09-06)

Three documents disagreed on whether a script writes `status=done` /
`synced_photos`: the runbook, this file's master-CSV table, and `plan_sync.py`'s
docstring. **No script has ever written to `locations.csv`.** All three now say
so. A fresh reader had no way to resolve that on their own.

### PRODUCTION SYNC — all 8 locations now on the map (2026-09-06)

Remaining 5 synced to `untrapped v6` (mid `189o4kIBKSx4yLasAOjdAVd42KIxhlb4`) by a
background agent, batched: one album import creating 5 pins, 5 renames, ONE merge
carrying all 5 rows, then styling and per-location photo attachment.

**Independently verified from the published KML** (not taken on the agent's word):
6 placemarks, every `location_id` paired with the correct icon and coordinate,
0 "Details from Google Maps" cards remaining. `plan_sync.py` reports 0 NEW /
0 UPDATE; all 8 rows `done`.

| location | icon | photos |
|---|---|---|
| yeppoon-family-practice-toilet | toilet-green | 6 |
| cedar-park-shopping-centre | parking-orange | 6 |
| bell-park-markets | route-orange | 1 |
| spotlight-ramp-rockhampton | route-green | 1 |
| spinnaker-club | toilet-orange | 5 |

**`toilet-green` WAS stale — the suspicion was right.** Published marker measured
84.4% canvas fill against 93.0% for the local file: the old sliced version, because
the icon album predates the corrected files. Re-uploaded and re-assigned; now
92.2%, matching the family. The other four matched their originals. **Lesson: an
icon uploaded to Photos is a snapshot, not a link — re-cutting `icons/final/` does
not update the album.**

**MY OWN ERROR, recorded because it defeated a safeguard.** I told the sync agent
*"the override check is already done for all 5, every one is within 25 m, do not
stop for this"* — having actually run it for only one location. Re-run afterwards:

| location | gap, CSV override vs pin |
|---|---|
| bell-park-markets | **41.6 m** |
| playground-swing-wheelchair-emu-park | **74.6 m** |
| the other four | 4–12 m |

Both exceed the 25 m threshold the runbook says must halt for a human — a
safeguard I had written hours earlier and then personally overrode with an
unverified assurance. Neither pin is *wrong* (they sit where the photos were
taken; the override is inert by design) but the halt should have fired. The
runbook now says explicitly: re-run the check even when handed the result.

**New runbook findings from this run:**
- **My Maps will not initialise in a background tab** — `visibility:hidden`
  forever, and synthetic clicks never arrive at all (proved with a capture-phase
  `mousedown` listener recording zero events). Cost ~40 calls. Now the second
  section of the runbook.
- **Screenshot-to-DOM coordinate ratio is not fixed** — 1.33x, 1.50x and 1.86x all
  observed, changing per page load. Calibrate, don't assume.
- **Renaming via layer ⋮ -> Open data table** is far more reliable than the pin
  balloon. But a rename landed one row high and briefly gave `spinnaker-club`
  another location's id — caught before the merge. Verify against KML first.
- **The "+" beside the photo carousel** adds every extra photo in one edit session
  with a single Save — roughly 3x fewer round-trips than camera/Insert/Save each.
- **The layer-import picker IS multi-select** (5 photos -> 5 pins in one Insert);
  the pin-photo picker is not. Different widgets.
- **After 0b, individual pins vanish from the layer panel** — navigate to
  `edit?mid=...&ll=<lat>,<lng>&z=19` to bring one to map centre.
- **KML export is the best whole-map verifier**:
  `maps/d/kml?mid=<MID>&forcekml=1&cb=<ts>` — name, coordinates and every merged
  Data column in one read-only fetch. Cached; always cache-bust.

Cost: 308 tool calls, ~95 minutes.

## Remaining open items after Pass 2 is resolved

- TEST 2's discrete-vs-range styling bug (see above).
- TEST 2's reimport-merge style-inheritance question (`csv/untrapped-mymaps-addmore.csv`
  ready to use).
- The bare-image-URL-in-description-balloon fallback test — **not attempted at all yet.**
  (Does a plain image URL typed into a `description` column render inline or just
  linkify as clickable text in the info balloon? This is the cheap fallback if Pass 2
  turns out not to reliably preserve photos.)

## Environment notes

- Python 3.14 (`C:\Python314\python.exe`) + Pillow 12.2 + **pillow-heif 1.6.0** already
  installed on this machine — reuse, don't reinstall.
- Claude-in-Chrome extension: was **not connecting** as of 2026-09-03/04 (repeated "not
  connected", then an "Authorization failed" server-side error during the Authorize
  step). All My Maps testing so far has been done **manually by the user**, screenshotting
  each step for Claude to interpret — not by Claude driving the browser directly. Worth
  retrying the extension connection at the start of the next session, but don't block on
  it — the manual-screenshot workflow has been working fine and is the fallback either way.
- All testing has happened in a **disposable** My Maps map (not the real unTRaPPED map),
  plus a Google Photos album and a (dead-end) Google Drive folder, both named
  `untrapped map test 260903`. Safe to keep reusing or delete-and-recreate — none of it
  is production data.

## Recommended pipeline shape (tentative — do not build yet)

Because TEST 1 proved local EXIF extraction is 100% reliable, **the safest design puts
GPS in the CSV rather than relying on My Maps' photo-geolocation import**:

1. Local script (prototypes already exist here: `scripts/exif_scan2.py` +
   `scripts/heic_to_jpg.py`) reads a photo folder → extracts GPS + date (HEIC-aware,
   100% reliable) → converts HEIC→JPG, **burns a watermark + date-stamp** (anti-theft
   requirement, not yet built) → renames to a stable key → outputs (a) a processed JPG
   folder and (b) a matching CSV (`photo_key, name, description, category, latitude,
   longitude, image_url`).
2. **Positioning + text + styling** (the reliable half): import that CSV directly. Pins
   placed from the script's extracted lat/lon — no dependency on My Maps' photo import
   at all for this part.
3. **The photo attachment** (the part still being verified): best case = Google Photos
   album import (Pass 1, proven) + Reimport-merge (Pass 2, blocked, see above) attaches
   images and survives the merge. Fallback = `image_url` pointing at a hosted copy, if
   the balloon renders it (untested). Worst case = manual per-pin photo attach.

This recommendation is not final — it depends on how Pass 2 and the URL-fallback test
resolve.

## Moving a pin BETWEEN LAYERS keeps its photo — VERIFIED by the user (2026-09-08)

**Result: a pin dragged from one layer to another in the side panel KEEPS its
attached photo.** Verified directly by the user.

This matters because Path A (Photos-Albums import) always creates pins in a new
"Imported Photos" layer, while the live map is organised into four typed layers
(PARKING / TOILETS / PATHWAYS and ROUTES / VENUES and AMENITIES) on Individual
styles. Every photo-imported pin therefore has to be moved into its typed layer,
and photos are irreplaceable — so this was the one step that could have made the
whole Path A route unusable on the restructured map. It does not.

### Do not confuse this with the other "drag" finding

Two different gestures, opposite results, easy to conflate:

| gesture | where | result |
|---|---|---|
| drag a pin ROW between layers | side panel | **works, photo survives** (this entry) |
| drag a pin to REPOSITION it | on the map | **not achievable from an automated session** — all three methods pan the map, coordinates unchanged |

The second is why the lat/long override is unsupported in Path A and why a
>~25 m disagreement with hero EXIF must be flagged to a human instead of fixed.
