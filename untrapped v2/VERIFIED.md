# SETTLED — do not re-test these

One line per fact that has been PROVEN. If something is here, it is known.
**Never ask the human to re-verify anything on this list.** They have already
done it, often more than once, and being asked again is the single most
annoying failure mode of this project.

If a doc elsewhere contradicts this file, **this file wins**. Append here the
moment something is proven; never rewrite an entry, and never delete one
because you personally could not reproduce it — add a dated note instead.

| # | Fact | Verified by | When |
|---|---|---|---|
| 1 | Dragging a pin **between layers** in the side panel KEEPS its photo | user | 2026-09-08 |
| 2 | Three agent methods of repositioning a pin **on the map** — the drag tool on its own, hover-then-drag, and synthetic mouse events — all pan the map instead of moving the pin. A different gesture does move it: see #28 | agent, 3 methods | 2026-09-06 |
| 3 | Photos-Albums import (layer → Import → **Albums** tab) creates pins at EXIF GPS with the photo attached natively | user, by hand | 2026-09-04 |
| 4 | The layer Import dialog's **Drive tab shows only CSV/XLSX/KML**, and its **Upload button rejects images** | user, by hand | 2026-09-04 |
| 5 | CSV merge adds metadata and **photos + styling survive it** — provided lat/lon columns are EXCLUDED | user, by hand | 2026-09-04 |
| 6 | Including **lat/lon in a merge is destructive** — it wrecked every pin on a test map | user, by hand | 2026-09-04 |
| 7 | A merge **silently drops rows that match nothing**. No error, no warning | agent | 2026-09-05 |
| 8 | An image URL in a description **linkifies as blue text**; it does NOT render as an inline thumbnail | user, by hand | 2026-09-04 |
| 9 | Extra photos: the pin's **"+" → Google Drive** tab works, including on already-imported pins. One at a time, no multi-select | user | 2026-09-04 |
| 10 | The **"Photos" tab** in that picker is flat and by-date with no album filter — impractical at scale | user | 2026-09-04 |
| 11 | Photos-Albums import attaches a wrong **"Details from Google Maps"** card. Has a Remove link, does not auto-update, survives dragging. CSV-imported pins never get one | user | 2026-09-04 |
| 12 | **Photos cannot be moved between maps** except by `Copy map`. Export gives session-scoped URLs that die outside the session | agent | 2026-09-06 |
| 13 | `Copy map` **regenerates every photo URL** — so URLs cannot be used to compare an original with its copy | agent | 2026-09-07 |
| 14 | **CSV import places pins on byte-exact coordinates**, and Individual styles keeps the legend clickable per pin | agent | 2026-09-06 |
| 15 | **Legend order is import order**, not alphabetical | agent | 2026-09-06 |
| 16 | `Import` is **disabled on a populated layer**; use Reimport and merge → the APPEND option | agent | 2026-09-06 |
| 17 | **Max 10 layers.** Google fails silently past it | agent | 2026-09-06 |
| 18 | My Maps **will not initialise in a hidden tab** — no click lands, everything appears to succeed. A covered window counts as hidden | agent | 2026-09-06 |
| 19 | **KML cannot verify icons** — every placemark reports the stock blank marker regardless of the icon actually applied | agent | 2026-09-07 |
| 20 | **KML lags**, sometimes a minute, even with `cache:'reload'` + cache-buster. The DOM is correct instantly | agent | 2026-09-07 |
| 21 | The **custom-icon picker is single-select** — choosing several silently keeps one | agent | 2026-09-07 |
| 22 | Every Google picker's **Upload tab is a dead end** — cross-origin iframe, zero reachable file inputs. Icons must go via a Photos album, photos via Drive | agent | 2026-09-06 |
| 23 | A **geometry-less placemark never appears in the layer panel** — only in the data table, via the "N rows couldn't be shown" banner | agent | 2026-09-07 |
| 24 | The **paint-can responds to synthetic events** — no coordinate clicking needed | agent | 2026-09-07 |
| 25 | Icon artwork is re-encoded to **128px** and renders at **18×18** at all zooms | agent | 2026-09-05 |
| 26 | A **human** moves a pin like this: click **"Open in My Maps"** (if the map opened outside the editor), **double-click** the marker, **keep the mouse held down on the second click**, then drag | user | 2026-09-13 |
| 27 | **My Maps takes 3–5 s to respond to a click.** Agent checks made ~3 s after a click raced the UI, so clicks that had registered were read as failures. Retrying them double-applied: v7 gained six empty layers. Fix: wait (5–8 s) before checking, and never repeat a click that looks dead until the wait is over | user spotted it; agent confirmed | 2026-09-06 |
| 28 | **An agent CAN move a pin on the map.** Gesture: a rapid double-click on the marker with the second press held, then drag. It was done as `left_click` then `left_click_drag` from the same point in one `browser_batch`, in the visible tab, followed by an 8 s wait. On v5 the parking pin moved **50.4 m south, 0 m east** (target 50 m), and the map did not pan | agent (Claude in Chrome), at the human's direction | 2026-09-13 |
| 29 | **A pin moved on the map keeps its photos:** 3 before and 3 after the #28 drag (KML `gx_media_links`, and the balloon's "1 of 3") | agent | 2026-09-13 |

**Provenance of rows 3–6 and 8–11 (audited 13 Sep 2026 from session `3fd56563`).**
Claude-in-Chrome failed on every call on 3 Sep ("Authorization failed", 23:24 AEST) and
first succeeded at **15:17 AEST on 4 Sep**. Every one of these rows was done by the user by
hand between 00:28 and 11:09 AEST on 4 Sep, with screenshots for the agent to interpret.
Rows 3–6 and 8 had been credited to the agent; all eight had been dated 3 or 5 Sep. These
corrected dates are AEST. An agent has never independently re-run any of them. Do not treat
that as a reason to re-test: they were proven by the human, on the screen.

## Still genuinely unknown

Short list. Do not add to it speculatively.

- The exact label of the merge submenu's UPDATE option. Docs contain both
  "Merge matching items" and "Update matching items". It renders only on hover
  and the menu sits two items from **Delete this layer**, so it has not been
  worth a click to confirm. **Go by behaviour:** the option that updates
  existing rows by matching a key, NOT the one that appends. Whoever opens that
  menu next: read the real label and settle line this.

## Why this file exists

Findings were spread across STATUS.md, RUNBOOK.md, HANDOVER.md and
SPAWN-PROMPT.md with overlapping scope, and each session rewrote rather than
appended. Verified facts kept getting lost and then re-flagged as unverified,
so the user was repeatedly asked to re-test what they had already proven.
This file is the single place that survives.
