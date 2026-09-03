# unTR@PPED — repository split (V2 active / V3 parked)

This repository holds the local development workspace for the **unTR@PPED**
accessibility project (Yeppoon / Emu Park, Capricorn Coast, Queensland).

It is deliberately split into two sibling folders:

| Folder | Version | Status | What it is |
|--------|---------|--------|------------|
| [`untrapped v2/`](untrapped%20v2/) | **V2** | **Active** | Current direction. A **Google My Maps**-based map. **No downloadable app.** **Owner-only** pin creation (Michael curates every pin). Framed around **lived experience** — what a real wheelchair/mobility-device user encounters on the ground — **not** building-code / standards compliance. |
| [`untrapped v3/`](untrapped%20v3/) | **V3** | **Parked** | The previous, more advanced concept: a custom whole-outing planner built on a **strict measurement / building-code assessment model** (deterministic compliance scoring against standards). Deferred, **not deleted** — preserved intact for a possible future V3. |

## Why the split

The work formerly labelled "V2" inside this repo (the strict measurement /
building-code assessment model) has been **renamed V3 and parked**. It is an
advanced version that is not the current priority.

A **new V2** takes over as the active line of work with a deliberately smaller
surface:

- **Google Maps (My Maps), not a bespoke app** — no build, no backend, no app store.
- **Owner-only pins** — the map is a curated, single-author evidence base, not
  a community-editable dataset.
- **Lived experience over compliance** — pins describe what actually happens
  when you try to get there, get in, and use it — plainly, without pretending
  to certify against building codes.

The building-code / compliance model is **deferred, not abandoned**. All of its
planning and artifacts remain under `untrapped v3/`.

## Notes

- Git history for every file under `untrapped v3/` is preserved — the contents
  were moved with `git mv`, so `git log --follow` still works.
- `untrapped v3/` is a self-contained pnpm/Replit workspace. Its Replit and
  workspace configs (`.replit`, `pnpm-workspace.yaml`, etc.) now live one level
  down; see that folder's own README and the parent split note before trying to
  build or deploy it.
- This split is organisational only. It does **not** touch the separate,
  live campaign website (`untrapped-site`) or its public Google My Map.
