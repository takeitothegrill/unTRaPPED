# V2 Roadmap — unTR@PPED Yeppoon

**Status: Stage 0 Planning Draft**

This roadmap describes the planned stages for building V2. Each stage must be completed and validated before the next stage begins.

---

## Stage 0 — Planning Docs (Current)

**Goal:** Establish all planning documents before any code is written.

**Deliverables:**
- README.md
- docs/V2_PRODUCT_SPEC.md
- docs/V2_WHOLE_OUTING_MODEL.md
- docs/V2_DATA_MODEL_DRAFT.md
- docs/V2_DECISION_ENGINE_DESIGN.md
- docs/V2_ROADMAP.md
- docs/V2_RESEARCH_QUESTIONS.md
- docs/V2_REPLIT_PROMPTS.md
- docs/REFERENCE_INDEX.md

**Constraints:**
- No React scaffolding
- No database
- No API routes
- No frontend components
- No TypeScript app implementation
- No auth
- No map integration

**Status:** In progress

---

## Stage 1 — Static Whole-Outing Prototype

**Goal:** Build a static, mobile-first prototype that demonstrates the whole-outing model with hardcoded sample data. No database, no backend, no real data.

**Deliverables:**
- React (or plain HTML) mobile-first UI
- Hardcoded sample data for 2–3 Yeppoon venues
- All outing stages represented (parking, pathway, entrance, interior, toilets, return)
- Decision engine logic implemented with sample data
- ✅ / ⚠️ / ❌ results displayed per stage and overall
- Reasons displayed for each result
- Call-ahead prompts displayed where relevant
- User mobility profile input (basic version)
- Clear labelling that all data is prototype/sample data
- Print/PDF outing summary (from MVP)

**Constraints:**
- No real venue data
- All data clearly labelled as prototype/sample
- No database
- No backend API
- No user accounts

---

## Stage 2 — Structured Local Data

**Goal:** Replace hardcoded sample data with structured local data files (JSON or YAML) covering real Yeppoon venues. Decision engine operates on real data for the first time.

**Deliverables:**
- Local data files for 5–10 real Yeppoon venues
- Venues assessed in person or from direct knowledge
- Each venue includes: parking, pathway, entrance, toilets (where applicable)
- Data freshness dates recorded
- Verification status recorded (admin-verified vs prototype)
- Decision engine produces results based on real data
- Results no longer labelled as prototype where data is real
- Data clearly attributed and dated

**Constraints:**
- Still no backend database
- Still no community submissions
- Still no map integration
- Data managed as local files only

---

## Stage 3 — Backend Database and Admin Data Entry

**Goal:** Move venue and outing data to a real database. Build a basic admin interface for entering and updating venue data.

**Deliverables:**
- PostgreSQL database (Drizzle ORM)
- Database schema implementing V2 data model
- Admin UI for:
  - Creating and editing venues
  - Adding parking, path, entrance, toilet data
  - Setting verification status and freshness dates
  - Uploading evidence photos
- API routes to serve venue and outing data to frontend
- Migration from local data files to database

**Constraints:**
- Admin access only (no public data submission yet)
- No map integration yet
- No user accounts yet

---

## Stage 4 — Community Submissions

**Goal:** Allow wheelchair users to submit reports and corrections. Build moderation workflow.

**Deliverables:**
- Community report submission form (public, no account required for basic submission)
- Submission review queue for moderators
- Moderation UI (approve / reject / edit)
- Community data displayed with clear unverified labelling
- Verification status reflected in decision engine
- Temporary obstruction reporting

---

## Stage 5 — Map Integration

**Goal:** Add a map view showing venues, parking, and routes.

**Deliverables:**
- Interactive map (OpenStreetMap or similar)
- Venue markers on map
- Accessible parking markers
- Route display from parking to entrance
- Filter by result level (show only ✅ venues, etc.)
- Integration with Google Maps / Apple Maps for navigation handoff

---

## Stage 6 — User Accounts and Saved Profiles

**Goal:** Allow users to save their mobility profile and saved venues.

**Deliverables:**
- User account creation (email or social login)
- Saved mobility profile
- Saved venues / favourite venues
- History of outing plans
- Push notifications for changes to saved venues (optional)

---

## Future Considerations (Not Committed)

The following may be considered for later stages:

- Offline mode (cached data for outings without internet)
- QR codes at venues linking to their accessibility summary
- Integration with MyPlus or other disability service databases
- Broader geographic coverage beyond Yeppoon
- Carer/support worker role and access
- Venue owner portal for self-reporting and verification requests
- Accessibility route planner (full turn-by-turn accessible navigation)
- Data sharing with OpenStreetMap accessibility tagging

---

## Principles for All Stages

- Mobile-first at every stage
- Safety principles and result language rules must be maintained at every stage
- No numerical scores at any stage
- No overclaiming at any stage
- Clear data attribution at every stage
- Prototype data clearly labelled at every stage until replaced by real data
