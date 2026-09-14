# unTRAPPED — Agent Runbook v1

Use this runbook only with the **working-copy** Google My Map. Never edit the production map or V3.

## Operating rules

- Operational CSV: `locations-from-v1-map.csv` only.
- Process `ready` and `update` rows only, unless the human specifies a smaller batch.
- Ignore `done`, blank, and unrecognised statuses.
- Never use `quality` or `photos_on_map` as workflow input.
- Use a temporary batch manifest for agent handoffs. It is not a new source of truth.
- Run the stages below in order.
- Only one agent may edit the working map at a time.
- One map operator owns a location from the start to the end of its map work.
- A failed location does not stop other independent locations.

## 1. Orchestrator

### Start the batch

- [ ] Confirm the target is the working-copy map—not production.
- [ ] Select the requested `ready` and `update` rows.
- [ ] Do not select rows based on `quality`.
- [ ] Create one batch manifest containing, for each selected row:
  - `location_id` and original status;
  - CSV data needed by the later stages;
  - expected source-photo filenames;
  - exact approved icon filename when resolved;
  - preparation, map-operation, and verification outcomes;
  - confirmed attached filenames;
  - any blocker.
- [ ] For new pins, reserve `TEMP IMPORT - YYYY-MM-DD`; add ` - 2`, ` - 3`, etc. for additional same-day batches.
- [ ] Send the manifest and authoritative source locations to the Preparation Agent.

### Control the handoffs

- [ ] Advance each location only after its current stage succeeds.
- [ ] Ensure no two agents edit the map concurrently.
- [ ] Assign one Map Operator to complete all map work for each location, including every photo and the icon.
- [ ] Do not rely on conversation memory between stages.

## 2. Preparation Agent

Perform no My Maps editing.

For each selected location:

- [ ] Confirm `location_id` exists and is unique.
- [ ] Confirm the name exists.
- [ ] For `ready`, confirm latitude and longitude are present and valid.
- [ ] Locate source photos only in `incoming/<location_id>/`.
- [ ] Resolve category plus rating through the authoritative icon mapping.
- [ ] Confirm the mapping names an exact current PNG in `icons/final/`.
- [ ] Never substitute a Google stock icon or infer an icon from colour alone.
- [ ] Preserve every original photo unchanged.
- [ ] Create an upload derivative of each supported source photo with the approved unTRAPPED logo watermark.
- [ ] Use `branding/untrapped-logo.PNG` as the only approved watermark artwork.
- [ ] Read every rendering value from `config/watermark-settings.json`; never hard-code or infer a watermark value.
- [ ] Validate the settings before processing. A missing file, unsupported placement, negative margin, or `width_ratio`/`opacity` outside the range greater than zero through one blocks preparation.
- [ ] Upload the watermarked derivatives to Drive.
- [ ] Record each source filename, exact uploaded derivative filename, staged Drive result, and approved icon filename in the manifest.
- [ ] When HEIC is converted to JPG, use the resulting JPG filename as the upload identity and later `synced_photos` value.
- [ ] Watermarked files created locally may remain locally; uploaded copies remain in Drive. Never re-download a Drive file merely to create a local copy.
- [ ] Do not treat identical photo content in different location folders as an error; shared evidence is allowed.

For an `update` row:

- [ ] Compare expected uploaded derivative filenames with `synced_photos`.
- [ ] Prepare and upload only derivative filenames not already recorded.
- [ ] Preserve all previously recorded filenames.

If preparation is blocked:

- [ ] Record a short, human-readable blocker in the manifest.
- [ ] Do not advance that location to map operation.

No photos is advisory, not blocking. Record it for the Orchestrator.

## 3. Map Operator

Work on one location at a time. After every My Maps interaction, wait **5–8 seconds** before continuing. Never repeat a click merely because it appears unresponsive; most apparent platform-limit errors are delayed interface responses.

Do not use a freshly exported KML file to confirm a just-made map change: it can lag by about one minute and does not show custom icons. Trust the live My Maps page for newly changed content, photos and icons.

### New location: `ready`

- [ ] Create exactly one pin in the assigned temporary layer.
- [ ] Position it at the CSV latitude and longitude.
- [ ] Use the CSV pin name as its title.

### Existing location: `update`

- [ ] Match by `location_id` first.
- [ ] If unavailable on legacy pins, match by exact name plus coordinates.
- [ ] Continue only when exactly one pin matches.
- [ ] Never create a replacement pin merely because matching is uncertain.

### Context box

Populate the visible context in exactly this order:

```text
<PIN NAME>
Address: <street address>

DESCRIPTION:
<description>

Township: <township>
LGA: <lga>
Date last updated: <full month and four-digit year>

latitude: <latitude>
longitude: <longitude>
location_id: <location_id>
category: <category>
rating: <rating>
icon: <icon identifier>
```

- [ ] Use the successful processing month and year, for example `September 2026`.
- [ ] Preserve the displayed blank lines and labels.
- [ ] Use CSV values, except for the mapped icon identifier.

### Photos and icon

- [ ] Attach every staged watermarked photo for a new location.
- [ ] For an update, attach only newly staged filenames.
- [ ] Never remove an existing photo without explicit human authorisation.
- [ ] Treat any expected-photo attachment failure as blocking.
- [ ] Apply the exact approved PNG artwork identified in the manifest.
- [ ] Treat the exact local file in `icons/final/` as authoritative; use it whether or not it is already present in Google's custom icon library.
- [ ] Visually confirm the custom icon; exported data alone is insufficient.

### Record the outcome

- [ ] Record the pin identity, coordinates, visible content, attached filenames and photo count in the manifest.
- [ ] Record the applied icon filename and observable visual result.
- [ ] Report uncertainty or partial completion plainly.
- [ ] Do not alter CSV status, `synced_photos`, or `quality`.

Never move a new pin to a permanent layer or delete its temporary layer. The human performs that housekeeping.

## 4. Verification Agent

Verification is read-only. Do not repair the map unless the human separately requests it.

Use the live My Maps page to verify recently changed content and custom icons. A newly exported KML may lag by about one minute and cannot verify icon artwork.

For each operated location, independently check:

- [ ] Exactly one intended pin exists or exactly one existing pin was updated.
- [ ] Identity and coordinates match the CSV.
- [ ] Title and supplied text are correct.
- [ ] The context box follows the required layout.
- [ ] `Date last updated` is the current successful processing month and year.
- [ ] Every expected photo is attached.
- [ ] Every attached photo visibly carries the approved unTRAPPED watermark.
- [ ] Photo count and filenames agree with the manifest.
- [ ] The visible icon is the exact approved artwork.
- [ ] No unrelated pin or layer was changed.

Record either `PASS` or one specific failure in the manifest. Never soften uncertainty into a pass.

## 5. Finalisation

The Orchestrator finalises each row independently.

### Verification passed

- [ ] Update `synced_photos` with the exact uploaded filenames confirmed attached.
- [ ] For `update`, retain existing filenames and append only newly confirmed ones.
- [ ] Write a concise current advisory in `quality` only when useful—for example, no photos or no description.
- [ ] Otherwise clear an obsolete agent-written concern and leave `quality` blank.
- [ ] Set `status=done`.

`done` means the agent system completed its work. A new pin may still be in the temporary layer awaiting the human's move.

### Incomplete or blocked

- [ ] Leave the original `ready` or `update` status unchanged.
- [ ] Write a concise human-readable reason in that row's `quality` field.
- [ ] Update `synced_photos` only for attachments confirmed successful.
- [ ] State what succeeded, what failed, and what the human must resolve.
- [ ] Do not put technical diagnostics in `quality`.
- [ ] Do not attempt speculative recovery that risks duplication or data loss.

Blocking examples include missing or duplicate identity, invalid coordinates for a new pin, missing name, unresolved approved icon, an ambiguous update match, unavailable map access, failed expected-photo attachment, or an uncertain/destructive map outcome.

Missing photos, description, address, or optional context are advisory and do not prevent `done` when all other required work passes.

## Safety stop

Stop the affected location immediately if identity, target map, result, or safety is uncertain. Never delete a photo-bearing pin, remove an existing photo, overwrite an original source photo, rebuild the working map from CSV, or change unrelated map or CSV content.
