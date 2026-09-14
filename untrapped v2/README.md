# unTRAPPED V2

This folder contains the active Google My Maps workflow for human-curated accessibility information.

## Start here

1. Read [`BUSINESS-REQUIREMENTS.md`](BUSINESS-REQUIREMENTS.md).
2. Follow [`AGENT-RUNBOOK.md`](AGENT-RUNBOOK.md).
3. Use [`locations-from-v1-map.csv`](locations-from-v1-map.csv) as the only operational CSV.
4. Resolve icons through [`config/icon-map.csv`](config/icon-map.csv) and use only artwork in [`icons/final/`](icons/final/).
5. Confirm the map boundary in [`config/map-register.md`](config/map-register.md).
6. Read the adjustable watermark values from [`config/watermark-settings.json`](config/watermark-settings.json).

Only rows with `status=ready` or `status=update` are actionable. Blank, `done` and unrecognised statuses are ignored. The `quality` field is human-readable output, never workflow input.

## Watermark configuration

The approved logo is [`branding/untrapped-logo.PNG`](branding/untrapped-logo.PNG). Its adjustable rendering values are defined in [`config/watermark-settings.json`](config/watermark-settings.json) and explained in [`config/watermark-spec.md`](config/watermark-spec.md). Change the configuration file—not the workflow documents—when a different visual treatment is wanted later.

The existing [`pipeline/`](pipeline/) scripts implement a superseded workflow and must not be used for live work. They remain in place until approved replacements exist.

## Prepare a manual upload batch

Double-click [`Prepare upload batch.cmd`](Prepare%20upload%20batch.cmd). It reads only rows marked `ready` or `update`, validates their matching `incoming/<location_id>/` folders, and creates a dated folder in `batches/`.

Upload only that batch folder's `upload/` folder to Google Drive. Read its `RESULTS.txt` first; `batch-manifest.json` records the exact prepared filenames and validation outcome. The tool never uploads anything, edits My Maps, changes CSV statuses, or alters original photos.

For the curator's complete step-by-step flow, use [`HUMAN-CHEAT-SHEET.md`](HUMAN-CHEAT-SHEET.md).

Historical material is under [`archive/`](archive/). It is not operational guidance. `incoming/`, `processed/`, the canonical CSV and legacy unresolved data remain untouched by repository cleanup.
