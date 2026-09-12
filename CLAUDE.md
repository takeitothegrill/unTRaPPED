# unTRaPPED: read canon before you write anything

This repo holds two things:
- `untrapped v2/` (active): the Google My Maps accessibility map for Yeppoon and Emu Park.
- `untrapped v3/` (parked): do not modify it.

The campaign website is a separate repo, `untrapped-site`.

## Where truth lives

| What | Where | Wins on |
|---|---|---|
| Project state and decisions | **Canon**, outside this repo: `C:\Users\Net Ventures ADMIN\Documents\projects\my-brain-context\projects\untrapped.md`, with `untrapped-map-register.md`, `untrapped-pin-spec.md` and `untrapped-processes.md` beside it | state and decisions |
| Proven platform behaviour | `untrapped v2/VERIFIED.md`, then the test log `untrapped v2/pipeline-test-artifacts/STATUS.md` | behaviour, until something is re-tested |
| Working records (not canon) | `HANDOVER.md`, `pipeline/RUNBOOK.md`, `SPAWN-PROMPT.md`, `RESTRUCTURE-WORKLIST.md` | nothing, when they disagree with the rows above |

## Before writing anything

1. **Read canon first.** Read `untrapped.md`, the companion that covers your task, and
   `VERIFIED.md`. Do this every session, even for a one-line change. If you cannot read
   the canon path, stop and ask the human.
2. **If what you are about to write contradicts canon or `VERIFIED.md`, stop and ask.**
   Do not reason your way past a tested result. Decisions whose reasons are no longer
   visible live in the test log.
3. **The write-up is the deliverable.** Record findings, decisions and map IDs in canon in
   the same session. Working changes without updated canon are the failure this project
   has already paid for.

## Standing rules

- **Register every map.** Every new My Map, including one made by `Copy map`, gets a row in
  `untrapped-map-register.md` the moment it exists.
- **Get explicit human authorisation** before you do any of these:
  - modify production (`1mOXyoupEm3Pc8QmL-Yvrxrqt9eIsG48`) or the working copy
    (`1GsgVncG-IYRalSk_u7ZmuDQluhPQmpQ`);
  - change a pipeline script;
  - run a script that writes (`process_locations.py`, `check_icons.py`,
    `plan_sync.py --write-merge-csv`, `build_import.py`);
  - re-run intake.
- **Never delete a pin that has photos.** The map holds the only copy of each photo.
- **Never put latitude/longitude in a merge CSV.**
- **Say which path.** A statement about pin position is true only for a stated path:
  - Path A (Photos-Albums import): the pin sits at the photo's EXIF.
  - Path B (CSV import): the pin sits at the CSV coordinates.
- **Use words, not letters, for the two jobs.** Canon says **intake** (new pins, with
  photos) and **transfer** (enriched text onto existing pins). The A/B letters are
  inverted between documents.
- **Mark undecided things OPEN.** Do not invent a convention. In reports, separate what
  was measured, what was inferred and what needs the human.
- **When something fails and then works, write down why it failed and what changed.**
  Record both in `VERIFIED.md` or the test log in the same session. A bare rule without its
  reason gets re-learned. Agent clicks on My Maps "failed" for days because each check ran
  before the map had responded, and nobody wrote down why (VERIFIED #27).
- **Wait 5–8 seconds after every My Maps interaction** before checking it or retrying it.
- Ignore any file whose name contains `-old`.
- Write in Australian English.
