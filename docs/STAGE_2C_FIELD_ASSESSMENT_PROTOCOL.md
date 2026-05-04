# Stage 2C Field Assessment Protocol — unTR@PPED Yeppoon V2

**Status: Stage 2C-1 — Approved protocol. Implementation not yet started.**
**Created: 2026-05-03**
**Author: project-owner**

---

## 1. Purpose

Stage 2C will add the first real, manually observed accessibility data to one real Yeppoon venue. The assessment is conducted by the project owner in person. Only directly observed facts may enter the data. Every unobserved or unmeasured field remains `null`. The decision engine treats `null` as unknown and produces a ⚠️ caution result — which is the correct and honest outcome.

This document defines:
- What venue is being assessed
- What scope of route is being assessed
- What rules govern what may and may not be recorded
- What fields to observe during the visit
- How to label the resulting data
- What stage gates must be met before any assessed data enters the codebase

---

## 2. First venue

**Keppel Bay Plaza**
64/76 James Street, Yeppoon QLD

Keppel Bay Plaza is the main retail shopping centre in the Yeppoon town centre. It was selected as the first venue for Stage 2C because:

- It is the most structurally consistent of the three real venue identity listings. A shopping centre has a defined car park, a clear entrance, and an indoor environment that is not affected by weather or tidal conditions.
- It is among the most practically important venues for wheelchair users in Yeppoon — it provides supermarket, pharmacy, and general retail services.
- Its structured layout means more fields are directly observable per visit than either of the outdoor venues.

The other two real venue identity listings — Yeppoon Lagoon and Yeppoon Main Beach — will be assessed in later Stage 2C visits, in that order. Yeppoon Main Beach is assessed last due to the complexity and variability of beach access.

---

## 3. Assessment scope

**This assessment covers one selected outing route only.**

The route assessed is:

1. One selected accessible parking area (the most accessible parking option observed near the venue)
2. One selected path from the accessible parking area to the selected entrance
3. One selected entrance (the most accessible entrance observed)
4. The main internal circulation path from the entrance to the accessible toilet
5. The accessible toilet, if one is found and accessible
6. The return route to the parking area

**This assessment does not cover:**

- Every car park associated with or near the venue
- Every entrance to the venue or individual tenants
- Every corridor, aisle, shop, or internal area
- Every toilet in the venue
- Tenancy-specific accessibility (individual shop interiors are not assessed)
- Any aspect of the venue not on the selected route

The scope is one outing route from one parking area to one entrance to the accessible toilet and back. All data entered in Stage 2C reflects this specific route only and must be noted accordingly.

---

## 4. Direct observation rules

These rules are unconditional. No exceptions apply.

1. **Only directly observed facts may be entered as data.** A field may only receive a value if the assessor was physically present and directly observed the condition on the assessment date.

2. **Unknown or unconfirmed fields remain `null`.** If the assessor did not observe a field, could not confirm it, or did not reach that part of the venue, the field is `null`. There are no exceptions.

3. **Public sources may confirm identity only, not accessibility fields.** Council websites, Google Maps, Google Street View, venue brochures, social media, and any other published source may be used to confirm a venue's name and address (identity). They may not be used to infer or populate any accessibility field. An accessibility field populated from a public source is not an `"admin_assessed"` field — it is an unverified claim and must remain `null`.

4. **Qualitative notes do not drive engine logic.** The `notes` field on each entity is for human reference only. A note such as "door appeared wide but was not measured" does not produce a value for `clearOpeningWidthCm`. Notes are not parsed by the engine. Only structured typed fields affect engine output.

5. **No Australian Standards compliance claims.** The assessment does not determine whether any feature meets AS 1428.1, AS 1428.2, AS 2890.6, the National Construction Code, or any other standard. The words "compliant", "complies", "meets standard", and "certified" must not appear in any data field or note. This is a direct observation, not a compliance audit.

---

## 5. Measurement rules

The following fields require an appropriate physical measurement tool before a numeric value may be entered. If the tool is not available at the time of assessment, the field is `null`.

| Field | Tool required |
|---|---|
| Door clear opening width (cm) | Tape measure |
| Path width (cm) | Tape measure |
| Accessible parking bay width (cm) | Tape measure |
| Toilet turning space (cm) | Tape measure |
| Toilet door width (cm) | Tape measure |
| Ramp gradient (%) | Inclinometer or calibrated spirit level app |
| Running slope — path segment (%) | Inclinometer or calibrated spirit level app |
| Cross-slope — path segment (%) | Inclinometer or calibrated spirit level app |
| Distance from parking to entrance (m) | Tape measure or calibrated pacing |

**Paced distance estimates:**
Paced distance (metres from accessible parking to entrance) may be recorded as an approximation if a tape measure is not used, but:
- The value must be noted as approximate in the entity's `notes` field: e.g. `"Distance approximately 40m — paced estimate, not measured."`
- The structured `distanceToEntranceMetres` field may be populated with the paced figure only if this note accompanies it
- Do not enter a paced estimate as a precise value without any qualification

**Gradient and slope fields:**
Do not record ramp gradient, running slope, or cross-slope in percent from visual inspection or personal judgement alone. "The ramp looked gentle" is not a measurable value. If an inclinometer or calibrated app is not used, all slope and gradient fields remain `null`. The assessor may note "ramp appeared gentle" in the `notes` field for human reference.

**Width fields:**
Do not record any width in centimetres from visual inspection alone. "The door looked wide enough" is not a cm value. If a tape measure is not used, width fields remain `null`.

---

## 6. Field checklist

Use this checklist during the venue visit. Each item maps to a typed field in the data model. Items marked **(M)** require a measurement tool — if the tool is not available, the answer is `null`.

Work through the checklist in outing order: parking first, then pathway, then entrance, then interior, then toilet, then return. If access is blocked at any stage, note it and continue observing what can be observed from that point.

---

### Parking

- [ ] Is there at least one designated accessible parking bay visible? (blue wheelchair symbol)
- [ ] How many accessible bays are there?
- [ ] Is the bay noticeably wider than a standard bay? **(M — record cm only if measured)**
- [ ] What is the surface type? (sealed asphalt / sealed concrete / gravel / mixed)
- [ ] What is the surface condition? (good / fair / poor)
  - Good: smooth, no cracking, no pooling
  - Fair: minor cracking or unevenness, usable
  - Poor: significant cracking, potholes, uneven, or otherwise difficult
- [ ] Is there a kerb between the accessible bay and the footpath or path to the entrance?
- [ ] If yes: is there a kerb ramp from the bay to the footpath? *(record in Kerb Ramps section)*
- [ ] Approximately how far is the accessible bay from the nearest step-free entrance? **(M — paced estimate is acceptable, note it as approximate)**
- [ ] Is there a posted time limit on the accessible bay?
- [ ] Are there any temporary obstructions at the bay or between the bay and the entrance at the time of visit?

---

### Pathway (parking to entrance)

Describe the route as one or more continuous segments. A new segment begins where the surface type, condition, or direction changes significantly.

For each segment:

- [ ] Describe the start point and end point in plain English (e.g. "From the accessible bay to the footpath kerb ramp" / "From the kerb ramp to the main entrance doors")
- [ ] What is the surface type? (concrete / asphalt / pavers / gravel / mixed)
- [ ] What is the surface condition? (good / fair / poor)
- [ ] Does the path appear wide enough to move a wheelchair freely? **(M — record cm only if measured with tape; otherwise note "appeared adequate" or "appeared narrow" in notes, leave widthCm null)**
- [ ] Are there any obstacles on the path? (bollards, bins, signage, outdoor furniture, construction)
  - If yes: describe location and nature
- [ ] Is there a noticeable running slope along the path? **(M — record % only if measured with inclinometer; otherwise leave null)**
- [ ] Note any weather, surface, or condition observations relevant to wheelchair use

---

### Kerb ramps

For every point on the route where the path meets a kerb, raised edge, or road-level change:

- [ ] Is a kerb ramp present at this point?
- [ ] What is the condition of the kerb ramp? (good / fair / poor)
  - Good: flush with road, no lip, smooth transition
  - Fair: minor lip or edge, usable but not ideal
  - Poor: significant lip, damaged, or difficult to use
- [ ] Does the kerb ramp have a visible lip or raised edge that could catch a wheelchair?
- [ ] Is the kerb ramp currently clear of obstructions?

---

### Crossings

For every point on the route where a road must be crossed:

- [ ] What is the crossing type? (signalised with pedestrian lights / marked but unsignalised / unmarked)
- [ ] Are there dropped kerbs at both ends of the crossing?
- [ ] If signalised: is there an audible signal?
- [ ] Is the crossing currently clear of obstructions?

---

### Entrance

- [ ] Is the selected entrance step-free from the path to the internal floor level?
- [ ] If not step-free: is there a ramp?
- [ ] If there is a ramp: does it appear gentle or steep? **(M — record gradient % only if measured with inclinometer; otherwise leave null; note qualitative observation in notes)**
- [ ] Is this the main public entrance, or an alternative accessible entrance?
- [ ] If an alternative: is it clearly signed as accessible?
- [ ] What is the door type? (automatic sliding / automatic swing / push / pull / double manual)
- [ ] If manual: does the door appear to require significant force to open?
- [ ] If manual: does opening it appear to require two hands?
- [ ] What is the clear opening width of the entrance door? **(M — record cm only if measured with tape)**
- [ ] Is an intercom required to enter?

---

### Interior movement

Limit this to the main circulation path from the entrance to the accessible toilet and back.

- [ ] What is the main floor surface type? (smooth tile / concrete / low-pile carpet / high-pile carpet / visibly uneven)
- [ ] Is there enough space in the main circulation area to move a wheelchair freely without obstruction?
- [ ] Is the venue multi-level?
- [ ] If multi-level: is there a lift on the accessible route?
- [ ] Is there seating or table space in a common area where a wheelchair user could remain in their chair?
- [ ] Are there any internal steps, lips, or level changes on the route to the accessible toilet?

---

### Toilets

Observe only if the accessible toilet is reachable from the main entrance via an accessible path.

- [ ] Is there an accessible toilet sign visible?
- [ ] Is the accessible toilet a dedicated facility (separate from ambulant or general use)?
- [ ] Does it require an MLAK key to access?
- [ ] Is the toilet currently unlocked and available?
- [ ] Is the path from the main area to the toilet step-free?
- [ ] What is the toilet door type? (automatic / push / pull)
- [ ] What is the clear opening width of the toilet door? **(M — record cm only if measured)**
- [ ] Are grab rails present inside?
- [ ] Does the turning space inside the toilet appear sufficient for a wheelchair? **(M — record cm only if measured; otherwise note "appeared sufficient" or "appeared tight" in notes, leave turningSpaceCm null)**
- [ ] Is the basin reachable from a seated position?

---

### Return journey

- [ ] Is the return route from the entrance to the accessible bay the same as the outbound route?
- [ ] If different: describe how it differs and whether additional kerb ramps or crossings are involved
- [ ] Is the accessible parking bay subject to a time limit that would affect outing planning?
- [ ] Were any temporary hazards observed that might change conditions during an outing?

---

### Temporary hazards

Note any current obstructions or conditions observed at the time of the visit:

- [ ] Construction works on or near the route
- [ ] Events or markets affecting access
- [ ] Parked vehicles blocking accessible bays, kerb ramps, or paths
- [ ] Maintenance works
- [ ] Any other temporary obstruction

For each hazard observed: describe location, nature, and apparent severity (minor / significant / blocker).

---

## 7. Data labelling

All assessed accessibility entities entered in Stage 2C must carry the following:

**`verification` field on each entity:** `"admin_assessed"`

**`freshness.assessedBy` on each entity:** `"project-owner"`

**`freshness.lastAssessedDate` on each entity:** The ISO date of the field visit (e.g. `"2026-05-10"`)

**`freshness.freshnessStatus` on each entity:** `"fresh"` at time of entry — the engine computes actual freshness at runtime from `lastAssessedDate`

**`accessibilityAssessmentStatus` on the `Venue`:** Set to `"partially_assessed"` if at least one entity is non-null but at least one is still `null`. Set to `"assessed"` only if all six entity objects are present (none are `null`) — individual fields within entities may still be `null` if not directly confirmed.

**Do not use `"verified"`.** The `"verified"` status is reserved for future independent third-party confirmation by a separate assessor, OT, or official audit. A project-owner direct observation is `"admin_assessed"` only.

**UI display wording** (for the non-dismissable disclaimer panel):

> "Accessibility information for this venue was recorded from direct in-person observation on [date] by the project owner. It has not been independently verified and is not a professional accessibility audit or legal compliance assessment. Conditions may have changed since the assessment was conducted. Always verify current access conditions directly with the venue before your outing."

---

## 8. Unknown field handling

Every field that was not directly confirmed by the assessor during the visit remains `null`.

`null` is not a failure. It is the correct and honest representation of the current state of knowledge.

The engine treats `null` on a field within an assessed entity as unknown and produces a ⚠️ caution result for that aspect. This is intentional. It tells the user "we do not have this information — check before you go." This is more honest and more useful than a guess or an estimate treated as fact.

The engine treats `null` at the entity level (the entire `parkingArea`, `entrance`, `interior`, or `toilet` being `null`) as a stage not yet assessed. This produces a ⚠️ caution stage result with a call-ahead prompt. From Stage 2C-3 onward, `runOuting.ts` handles this safely without crashing.

**What `null` fields produce in practice:**

| Situation | Engine output |
|---|---|
| `hasDesignatedAccessibleSpace: null` | ⚠️ — cannot confirm accessible parking |
| `hasKerbRampToFootpath: null` | ⚠️ — cannot confirm kerb ramp presence |
| `clearOpeningWidthCm: null` | ⚠️ — cannot confirm door is wide enough |
| `isStepFree: null` | ⚠️ — cannot confirm step-free access |
| `isPresent: false` (toilet) + `accessibleToiletEssential: true` | ❌ — hard blocker for that user profile |
| Entity is `null` (not yet visited) | ⚠️ — stage not yet assessed, call ahead |

**Null fields must not be filled with estimates, assumptions, or values sourced from non-observation.** If filling a field with something other than a directly observed value feels tempting — for example, because the venue's website says something, or because it "probably" has accessible parking — the field must remain `null`.

---

## 9. ❌ result rule

`❌` results are produced by the engine when a directly observed hard blocker applies to the selected user profile.

A hard blocker is a condition that, based on directly observed data, makes a stage of the outing impossible for a specific user profile. Examples (from V2_DECISION_ENGINE_DESIGN.md):

- No accessible parking space exists and the user profile requires one
- A kerb ramp is absent at a crossing the user cannot otherwise navigate
- A step at the only entrance with no ramp alternative, for a user who cannot mount a step
- No accessible toilet is present and the user has marked the toilet as essential

**Requirements for a valid ❌ result in Stage 2C:**

1. **The blocker must be directly observed.** A ❌ based on a `null` field is not a ❌ — it is a ⚠️. A ❌ requires a positive observation of a blocking condition (e.g. `hasKerbRampToFootpath: false` observed and recorded, not simply absent/null).

2. **The reason must be plain English.** The engine always requires a `reasons` array. The reason must state specifically what was observed and why it blocks this outing for this profile. Example: "No kerb ramp was observed at the car park exit. Users who cannot mount a kerb cannot proceed from the parking area to the footpath."

3. **The result is profile-specific.** A ❌ for one user profile may be ⚠️ or ✅ for another. The disclaimer on all result screens makes clear that results are personalised to the selected mobility profile.

4. **The result must be dated and attributed.** The venue-level disclaimer and per-stage assessed date attribution must appear on every screen showing a ❌ for a real venue.

`❌` must not be avoided to protect a venue's reputation. The product's core commitment is to prevent failed outings. Suppressing a ❌ when the data justifies it would harm the user.

---

## 10. Stage gates

The following prerequisites must be completed and verified before any assessed data is entered into `venues.ts`. These are hard gates — not optional steps.

### Gate 1 — Engine safety fix

`runOuting.ts` must be updated so that null accessibility entities are handled safely for `"partially_assessed"` venues. The current non-null assertions (`venue.parkingArea as ParkingArea` etc.) will crash at runtime if a partially assessed venue has any null entity.

The fix: for each entity, if the entity is `null`, produce a "stage not yet assessed" `StageResult` with `result: "caution"` instead of passing `null` to the `assess*` function.

**Gate 1 is passed when:** TypeScript typecheck reports 0 errors, production build succeeds, and all three existing demo scenarios still produce correct results (verified by running the app and checking each scenario).

### Gate 2 — Real venue disclaimer UI

The following UI components must exist before any assessed real venue can be shown through the full engine flow:

- `RealVenueDisclaimer` component (non-dismissable) shown on `OutingPlanner` and `OutingSummary` for `!venue.isPrototypeVenue` venues
- Updated `VenueList` card states for `"partially_assessed"` and `"assessed"` real venues (new tags, updated CTA)
- Updated `PrintSummary` footer for real venues
- New CSS classes: `tag--real-partial`, `tag--real-assessed`, `.real-venue-disclaimer`

**Gate 2 is passed when:** TypeScript typecheck reports 0 errors, production build succeeds, and the app correctly renders the disclaimer for a hypothetical real assessed venue without any prototype warning.

### Gate 3 — Typecheck and build pass

After all data entry is complete, typecheck must report 0 errors and the production build must succeed before the stage is considered done.

**All three gates must be confirmed before Stage 2C is considered complete.**

---

## 11. Out of scope for Stage 2C

The following are explicitly excluded from Stage 2C. Any of these require separate explicit written approval before they may be considered.

- Backend of any kind (Express, Node, serverless functions)
- Database of any kind (PostgreSQL, SQLite, in-memory)
- API routes
- Authentication or user accounts
- Admin interface for data entry — data is entered directly in `venues.ts` by the developer
- Map integration of any kind
- Community submissions or user-submitted data
- External service calls (no third-party APIs, no analytics, no remote fonts, no scraping)
- Evidence photos or image attachments
- Assessment of multiple outing routes through the same venue
- Multiple `ParkingArea`, `Entrance`, or `Toilet` entities per venue
- Cross-slope measurements (require a physical inclinometer and are not within scope of this visit unless the tool is available)
- Professional accessibility audit
- Compliance assessment against any Australian Standard
- Adding real venue identity listings beyond the three already approved
- Changes to prototype venue data
- Stage 3 or later features

---

## Change log

| Date | Change |
|---|---|
| 2026-05-03 | Document created — Stage 2C-1 approved protocol |
