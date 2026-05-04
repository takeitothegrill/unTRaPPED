# unTR@PPED Yeppoon V2

## Project name
unTR@PPED Yeppoon V2 — mobile-first wheelchair whole-outing accessibility planner for Yeppoon, QLD, Australia.

## Current status
**Stage 2B accepted — real venue identity listings, accessibility not assessed.**
Stage 2C has been planned but not started. No Stage 2C features exist in the codebase.

| Stage | Status |
|---|---|
| Stage 0 — Planning docs | Complete |
| Stage 1 — Static demo prototype | Complete and accepted |
| Stage 2A — Data safety and schema review | Complete (planning only) |
| Stage 2B — Real venue identity listings | Complete and accepted |
| Stage 2C — First real accessibility assessments | Planned, not started |
| Stage 3+ | Not planned |

---

## Artifact

| Field | Value |
|---|---|
| Artifact path | `artifacts/untrapped-v2/` |
| Preview path | `/untrapped-v2/` |
| Kind | `web` (React + Vite + TypeScript) |
| Dev port | `24249` |
| Dataset version | `0.2.0-mixed` |
| Dataset mode | `mixed` (demo scenarios + real identity listings) |

---

## How to run / check

All commands run from the workspace root unless noted.

```bash
# Dev server (managed by workflow — do not run manually at root)
# Workflow: "artifacts/untrapped-v2: web"
pnpm --filter @workspace/untrapped-v2 run dev

# TypeScript typecheck
cd artifacts/untrapped-v2 && pnpm run typecheck

# Production build (PORT and BASE_PATH must be set)
PORT=24249 BASE_PATH=/untrapped-v2/ pnpm --filter @workspace/untrapped-v2 run build
```

---

## Project structure

```
artifacts/untrapped-v2/
├── src/
│   ├── data/
│   │   ├── types.ts          # All TypeScript interfaces and union types
│   │   ├── datasetMeta.ts    # datasetMode: "mixed", warning/notice text
│   │   └── venues.ts         # PROTOTYPE_VENUES (3) + REAL_VENUES (3) → VENUES
│   ├── engine/
│   │   ├── freshness.ts      # Computes fresh/aging/stale/unknown from ISO dates at runtime
│   │   ├── assessParking.ts  # Parking stage assessment
│   │   ├── assessPathway.ts  # Pathway/kerb ramp/crossing assessment
│   │   ├── assessEntrance.ts # Entrance/ramp/door assessment
│   │   ├── assessInterior.ts # Interior floor/aisle/level assessment
│   │   ├── assessToilet.ts   # Toilet assessment with essential-flag logic
│   │   ├── assessReturn.ts   # Return journey + time limit + obstructions
│   │   └── runOuting.ts      # Orchestrates all 6 stages; guards against not_assessed venues
│   ├── components/
│   │   ├── PrototypeBanner.tsx  # Sticky banner — red for prototype-only, navy for mixed
│   │   ├── ResultBadge.tsx      # ✅ / ⚠️ / ❌ badge (no numerical scores)
│   │   ├── StageCard.tsx        # Collapsible stage result card
│   │   ├── CallAheadList.tsx    # Numbered call-ahead checklist
│   │   └── PrintSummary.tsx     # Print-only full summary layout
│   ├── views/
│   │   ├── VenueList.tsx        # Screen 1 — venue list, two sections (demo / real)
│   │   ├── VenueNotAssessed.tsx # Screen for real not_assessed venues — identity + generic call-ahead
│   │   ├── ProfileSetup.tsx     # Screen 2 — wheelchair profile form (demo venues only, for now)
│   │   ├── OutingPlanner.tsx    # Screen 3 — six-stage result cards
│   │   └── OutingSummary.tsx    # Screen 4 — full summary + window.print()
│   ├── App.tsx                  # React state router; routes not_assessed → VenueNotAssessed
│   ├── index.css                # Mobile-first plain CSS, max-width 540px
│   └── main.tsx                 # Entry point
├── index.html
├── vite.config.ts
├── package.json
└── tsconfig.json
```

---

## Venues

### Demo scenarios (fictional — `isPrototypeVenue: true`, `verification: "prototype"`)

| Scenario | Venue name | Key feature demonstrated |
|---|---|---|
| Demo Scenario A | Seaside Café | Good accessibility, no toilet on-site — essential vs non-essential toilet logic |
| Demo Scenario B | Beach Path Kiosk | No kerb ramp at crossing (hard blocker), gravel car park, temporary obstruction |
| Demo Scenario C | Community Hall | Good data but 28+ months old — stale data degrades all results |

### Real venue identity listings (`isPrototypeVenue: false`, `accessibilityAssessmentStatus: "not_assessed"`)

| id | Name | Address | suburb | identitySource |
|---|---|---|---|---|
| `yeppoon-main-beach` | Yeppoon Main Beach | Anzac Parade | Yeppoon | direct-knowledge |
| `keppel-bay-plaza` | Keppel Bay Plaza | 64/76 James Street | Yeppoon | direct-knowledge |
| `yeppoon-lagoon` | Yeppoon Lagoon | 3 Anzac Parade | Yeppoon | direct-knowledge |

All three real venues: `parkingArea: null`, `entrance: null`, `interior: null`, `toilet: null`, `pathSegments: []`, `temporaryObstructions: []`. No accessibility claims of any kind.

---

## Key type additions (Stage 2B)

| Addition | Location | Purpose |
|---|---|---|
| `"admin_assessed"` | `VerificationStatus` | Project-owner direct observations (Stage 2C onward) |
| `"rejected"` | `VerificationStatus` | Inaccurate community reports (future use) |
| `AccessibilityAssessmentStatus` | `types.ts` | `"not_assessed" \| "partially_assessed" \| "assessed"` |
| `DatasetMode` | `types.ts` | `"prototype-only" \| "mixed" \| "real-data"` |
| `isPrototypeVenue` | `Venue` | Per-venue flag — controls banner and UI treatment |
| `accessibilityAssessmentStatus` | `Venue` | Controls routing (not_assessed → VenueNotAssessed) |
| `address`, `suburb` | `Venue` | Real venue identity |
| `identityVerifiedDate`, `identityVerifiedBy`, `identitySource`, `identityNotes` | `Venue` | Identity provenance, separate from accessibility freshness |
| `scenarioLabel?` | `Venue` | Now optional — demo venues only |
| `verification?` | `Venue` | Now optional at venue level |
| `parkingArea?`, `entrance?`, `interior?`, `toilet?` | `Venue` | Now optional/nullable — absent for not_assessed venues |

---

## Routing logic (App.tsx)

```
handleSelectVenue(venue):
  if venue.accessibilityAssessmentStatus === "not_assessed"
    → view: "venue-not-assessed"   (VenueNotAssessed — identity + generic call-ahead only)
  else
    → view: "profile-setup"        (full engine flow)

runOuting.ts guards:
  if venue.accessibilityAssessmentStatus === "not_assessed" → throws
```

Real unassessed venues never reach `runOuting`. Two independent layers enforce this.

---

## Freshness rule (agreed — applies to all stages)

The engine computes freshness **at runtime** from `lastAssessedDate` using `computeFreshnessStatus()`. The static `freshnessStatus` field stored in `DataFreshness` objects is documentation only and is never read by any engine function. This prevents a file written today from silently misreporting its own age in the future.

Freshness thresholds: fresh < 12 months → aging 12–24 months → stale > 24 months.

---

## Hard constraints (all stages, until explicitly lifted)

- Static app only — no server-side processing
- No backend, API routes, database, or authentication
- No map integration
- No localStorage or sessionStorage
- No external service calls (no third-party APIs, no analytics, no remote fonts)
- No numerical accessibility scores — results use ✅ / ⚠️ / ❌ only
- Unknown data must produce ⚠️, never ✅
- Stale data degrades results
- No community submissions
- No admin interface
- No evidence photos
- No multiple parking areas, entrances, or toilets per venue (single entity each)
- No cross-slope measurements
- No hoist data
- No Stage 2C or later features until explicitly approved

---

## Planning docs (Stage 0 — complete)

| File | Purpose |
|---|---|
| `README.md` | Project overview and stage transition prompts |
| `docs/V2_PRODUCT_SPEC.md` | Product goals, scope, constraints |
| `docs/V2_WHOLE_OUTING_MODEL.md` | Six-stage outing model |
| `docs/V2_DATA_MODEL_DRAFT.md` | Full data schema |
| `docs/V2_DECISION_ENGINE_DESIGN.md` | Engine rules, hard blockers, result logic |
| `docs/V2_ROADMAP.md` | Stage 0–4 roadmap |
| `docs/V2_REPLIT_PROMPTS.md` | Prompts for each stage transition |
| `docs/REFERENCE_INDEX.md` | Index of all planning docs |

---

## Troubleshooting

**`pnpm run build` fails without PORT**
The `vite.config.ts` requires `PORT` and `BASE_PATH` environment variables. Provided automatically by the workflow. To build manually: `PORT=24249 BASE_PATH=/untrapped-v2/ pnpm --filter @workspace/untrapped-v2 run build`.

**Favicon 404 in browser console**
A browser pre-parse prefetch for `/favicon.ico` produces a harmless 404 that cannot be suppressed via link tags. It predates Stage 2B and does not affect functionality.

**Intermediate HMR runtime errors in workflow logs**
During Stage 2B implementation, hot module replacement produced transient `Cannot read properties of undefined (reading 'freshnessStatus')` errors while files were being updated. These are from intermediate states and are not present in the current running app.

---

## Workspace overview

pnpm workspace monorepo using TypeScript.

| Field | Value |
|---|---|
| Monorepo tool | pnpm workspaces |
| Node.js version | 24 |
| Package manager | pnpm |
| TypeScript version | 5.9 |

Other artifacts (unrelated to unTR@PPED V2):
- `artifacts/api-server/` — shared Express API server (unused)
- `artifacts/mockup-sandbox/` — Replit design canvas tool
