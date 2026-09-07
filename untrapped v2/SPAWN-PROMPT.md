# How to get CSV changes onto the map

## Easiest: just ask

In a session that already has this project's context, say:

> I've updated the CSV, push it to the map.

That is enough. The agent will read `HANDOVER.md` and `pipeline/RUNBOOK.md`,
work out whether rows are new or changed, and do the right operation.

---

## For a cold session: paste the block below

Everything the agent needs is in it. Update the two bracketed bits first.

---

```
Push updated location data onto a Google My Map for the unTRaPPED accessibility
project. This is live data with irreplaceable photos — read before acting.

Project root: C:\Users\Net Ventures ADMIN\Documents\projects\unTRaPPED\untrapped v2

READ FIRST, IN THIS ORDER:
  1. HANDOVER.md          — state, decisions, and the hard constraints
  2. pipeline/RUNBOOK.md  — the procedure. It is accurate; follow it.

TARGET MAP: [PASTE THE MAP URL]
WHAT CHANGED: [e.g. "12 new rows added" / "ratings corrected on ~20 rows"]

SOURCE OF TRUTH
locations-from-v1-map.csv is authoritative for all TEXT: names, descriptions,
categories, ratings, coordinates, township, LGA, address.
Photos are the exception — they live ONLY on the map.

THE THREE RULES THAT MATTER MOST
1. NEVER delete a pin that has photos. Photos cannot be exported and
   re-attached — CSV import ignores them and the exported image URLs are
   session-scoped and dead outside the editing session. A deleted photo is gone.
2. NEVER rebuild a photo-bearing map from CSV, for the same reason.
   Restructure it in place instead.
3. NEVER put latitude/longitude in a MERGE csv. It destroyed every pin on a
   test map. (Imports are different — they REQUIRE coordinates.)

PRE-FLIGHT — do these three before touching anything
  a. The map tab must be the VISIBLE, FOREGROUNDED browser tab. Check with
     document.visibilityState — if it returns "hidden", My Maps will not
     initialise, no click will land, and you will waste an hour. Ask the human
     to bring the window and tab to the front.
  b. Record the photo count. This is your safety line:
       curl -s "https://www.google.com/maps/d/kml?mid=<MID>&forcekml=1" | grep -c gx_media_links
  c. Run: python pipeline/check_icons.py
     to see which pins' icons no longer match their data.

WHICH OPERATION
  NEW rows (no pin on the map yet)
      -> layer menu -> Reimport and merge -> "Add more items"
      Appends. Import is disabled on a populated layer, by design.
  CHANGED text on rows that already have pins
      -> layer menu -> Reimport and merge -> "Merge matching items"
      Match Layer data location_id = Uploaded data location_id.
      NO lat/long columns. Rows matching nothing are SILENTLY DROPPED.
  Staging the CSV
      -> The Google Drive MCP connector uploads it directly, no browser:
         contentMimeType "text/csv" AND disableConversionToGoogleType true.
         Give it a UNIQUE filename — Drive allows duplicates and the picker
         cannot tell them apart.

ICONS — depends on the layer's style mode, check which is in use
  "Individual styles"  -> every new pin needs its icon assigned BY HAND.
                          Batch by icon, not by pin: once an icon has been used
                          on the map it appears under "Other icons" in the
                          paint-can, so repeats are one click.
  "Group places by"    -> icons follow the data automatically. Nothing to do.

VERIFYING
  The KML export lags, even with a cache-buster and cache: 'reload'. For
  anything you have JUST changed, read the live DOM instead. If the two
  disagree, trust the DOM.

STOP AND ASK if: the photo count drops, a merge reports rows it could not match,
the pin count moves unexpectedly, or anything looks irreversible and the runbook
has not explicitly told you to do it.

REPORT: pins before/after, photo count before/after, which icons still need
assigning, and anything in the runbook that was wrong.
```

---

## After it finishes

- Re-run `python pipeline/check_icons.py` and assign any flagged icons.
- Then `python pipeline/check_icons.py --synced` to move the baseline forward.
- Confirm the photo count is unchanged.
