# unTRAPPED V2 — Human cheat sheet

Use this checklist when you want to add a new accessibility location or update one that is already on the **working-copy** map. Do not use it for the production map or V3.

## 0. What the preparation tool does

`Prepare upload batch.cmd` is a local photo-preparation step. It reads only CSV rows marked `ready` or `update`, then looks only in the matching `incoming/<location_id>/` folder for each selected row. It creates watermarked copies of new photos in a dated `batches/` folder, plus a short result file and a detailed batch manifest.

It does **not** upload anything to Google Drive, edit Google My Maps, change the CSV, or alter your original photos.

## 1. Add a new location

1.1. Open `locations-from-v1-map.csv` in your spreadsheet program.

1.2. Add one row for the location. Give it a stable, unique `location_id`, using lower-case words separated by hyphens, for example `toilet-example-park`.

1.3. Fill in at least the location name, category, rating, latitude and longitude. Add the address, description, township and LGA when you have them.

1.4. Check that the category and rating are one of the recognised combinations in `config/icon-map.csv`. Do not choose an icon yourself.

1.5. Set `status` to `ready`. Leave `synced_photos` alone. Do not use `quality` or `photos_on_map` to tell the system what to do.

1.6. Create a folder named exactly like the `location_id` inside `incoming/`, for example `incoming/toilet-example-park/`.

1.7. Copy the original photos into that folder. Keep the originals there; do not watermark, rename, replace or delete them after preparation.

1.8. Double-click `Prepare upload batch.cmd` and wait for the window to say it has finished. The tool processes photos only from the `incoming/<location_id>/` folders belonging to rows currently marked `ready` or `update`.

1.9. Open the newest dated folder in `batches/` and read `RESULTS.txt`.

1.10. If it lists a blocker, correct the CSV row, folder name or source photos, then run the tool again. Do not upload a blocked location.

1.11. If it says `PREPARED`, manually upload the contents of that batch's `upload/` folder to Google Drive. Keep the location-id subfolders intact.

1.12. Give the batch folder and its `batch-manifest.json` to the map operator. The operator applies the prepared photos and approved icon to the working-copy map, then an independent check is completed.

1.13. After successful verification, the agent system records the attached filenames in `synced_photos` and changes the row to `done`. For a new pin, move it from its temporary map layer to its permanent layer when instructed.

## 2. Update an existing location

2.1. Find the existing row in `locations-from-v1-map.csv`. Do not create a duplicate row.

2.2. Update the information that has changed and set `status` to `update`.

2.3. Do not remove or edit the filenames already in `synced_photos`.

2.4. Put any new original photos in the matching `incoming/<location_id>/` folder.

2.5. Double-click `Prepare upload batch.cmd`, then read the newest batch's `RESULTS.txt`.

2.6. Upload only the new batch folder's `upload/` contents to Google Drive. It contains only photos not already recorded in `synced_photos`.

2.7. Give the batch and manifest to the map operator. Existing map photos must remain in place unless you explicitly authorise their removal.

2.8. After successful verification, the agent system appends the confirmed new filenames to `synced_photos` and changes the row to `done`.

## 3. Before you upload

3.1. Read `RESULTS.txt` every time.

3.2. Upload only the current batch's `upload/` folder, not `incoming/` and not a whole previous batch.

3.3. Keep the location-id folders inside `upload/` unchanged.

3.4. Keep `batch-manifest.json` with the batch; it is the record of what was prepared.

3.5. If a result is unclear, stop and ask before uploading or making map changes.

## 4. Common messages

4.1. `PREPARED` — Upload that location's prepared files from the batch `upload/` folder.

4.2. `READY_WITH_NO_NEW_PHOTOS` — No new photo upload is needed. It may be a valid text or icon update; continue through the map workflow.

4.3. `BLOCKED` — Read the `Attention` line in `RESULTS.txt`, fix the stated issue, then prepare a new batch.

4.4. `Nothing to prepare` — There are currently no CSV rows with `status` set to `ready` or `update`.

## 5. Safety reminders

5.1. Work only in V2 and the working-copy map.

5.2. Never use the tool on the production map or V3.

5.3. Never alter original photos in `incoming/`.

5.4. Never change a CSV row to `done` yourself; that happens only after map verification.

5.5. Never delete an existing map photo or a photo-bearing pin without explicit approval.
