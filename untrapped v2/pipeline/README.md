# unTRaPPED V2 — photo pipeline

Local preprocessing only: EXIF extraction, GPS backfill, HEIC→JPEG, watermark
+ date stamp. Does **not** touch Google Maps/Drive — that's a separate,
not-yet-built step. See `../pipeline-test-artifacts/STATUS.md` for the full
design and why it's split this way.

## Setup

```
pip install -r requirements.txt
```

## Workflow

1. Take photos. The **first photo taken** in a batch is the hero photo — its
   GPS position places the pin.
2. Download originals (iCloud "Download Original", not a share/message —
   anything else can strip GPS).
3. Drop the folder into `incoming/<location_id>/`. `location_id` is your own
   name for the folder — pick something short and stable, you'll reuse it.
4. Add or edit a row in `../locations.csv` for that `location_id`: `name`,
   `description`, `category` (one of: Toilets, Ramps, Accessibility, Pathway,
   Parking, Elevators, Doors), `rating` (green/orange/red). Leave
   `latitude`/`longitude` blank unless you need to override the hero photo's
   GPS (e.g. an indoor shot with no signal) — fill those in yourself if so.
5. Run:
   ```
   python process_locations.py
   ```
6. Processed, watermarked JPEGs land in `processed/<location_id>/`, ready to
   upload to a Google Photos album / Drive folder by hand (or by the
   browser-automation step once that's built).

Safe to re-run any time — it only fills blank `latitude`/`longitude` cells
and regenerates `processed/`, never overwrites text you've written.

`incoming/` and `processed/` are git-ignored (real photos, not committed).
`../locations.csv` is the one file that *is* committed — it's the whole
project's data.
