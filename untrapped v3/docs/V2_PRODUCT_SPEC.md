# V2 Product Specification — unTR@PPED Yeppoon

**Status: Stage 0 Planning Draft**

---

## Product Vision

unTR@PPED Yeppoon V2 is a whole-outing accessibility planner for wheelchair users in Yeppoon, Queensland, Australia.

It gives wheelchair users the confidence to plan and complete real outings by providing honest, structured, explainable accessibility information — from leaving home to returning safely.

The product does not just check if a venue is accessible. It checks whether a complete outing is possible: getting to the venue, entering it, using it, and getting back.

---

## Problem Statement

Wheelchair users in Yeppoon face failed outings because accessibility information is:

- Scattered across multiple sources
- Incomplete or missing entirely
- Inconsistent or contradictory
- Outdated and no longer reliable
- Not personalised to individual wheelchair requirements
- Overconfident where it should be cautious

A failed outing — arriving somewhere and discovering you cannot get in, cannot find accessible parking, or cannot reach the entrance — has real consequences: wasted effort, physical exhaustion, loss of independence, and erosion of confidence.

The product must help users make informed decisions before they leave, not discover problems on arrival.

---

## Primary User

**Wheelchair users in Yeppoon, Queensland, Australia.**

Specifically:
- People who use manual or powered wheelchairs
- People with varying levels of upper body strength and reach
- People who may travel alone or with a carer
- People who may be unfamiliar with a venue they want to visit

Secondary users (considered but not the primary focus):
- Carers and support workers planning outings
- Venue owners wanting to understand and improve their accessibility
- Moderators reviewing community submissions

---

## Core Use Cases

### UC1 — Plan a whole outing
A user wants to visit a specific venue. They want to know:
- Can I park near enough?
- Can I get from the car to the entrance?
- Can I get into the venue?
- Can I move around and use the facilities?
- Are there accessible toilets?
- Can I get back to my car?

### UC2 — Check a specific concern
A user wants to know about one aspect of a venue:
- "Does this place have step-free entry?"
- "Is there accessible parking nearby?"
- "Are there accessible toilets?"

### UC3 — Report a change or submit new information
A user knows something has changed at a venue (e.g. a ramp is now blocked, a new accessible entrance has opened). They want to submit that information for review.

### UC4 — Check if a venue is worth calling ahead
A user is planning an outing but some information is unknown or uncertain. The system should identify what they should call the venue to confirm before going.

---

## V2 Scope

V2 will eventually cover:

- Venues (cafes, shops, parks, medical centres, etc.)
- Parking areas (designated accessible spaces, proximity, surface)
- Pathways (segments from parking to entrance)
- Kerb ramps (presence, quality, condition)
- Crossings (pedestrian crossings, signals, dropped kerbs)
- Slope (gradient of paths and surfaces)
- Surface condition (smooth, rough, cracked, gravel, wet)
- Temporary obstructions (construction, events, parked vehicles)
- Hazards (ongoing obstacles)
- Entrances (step-free, ramp, automatic door, manual door, intercom)
- Doors (width, weight, handle type, automatic or manual)
- Interior movement (internal ramps, lifts, floor surfaces)
- Toilets (dedicated accessible toilet with correct features)
- Evidence and photos (supporting claims with visual evidence)
- Community reports (user-submitted information)
- Verification and moderation (distinguishing verified vs unverified)
- Data freshness (how old is the information?)
- Confidence and uncertainty (what is known vs unknown)

---

## Non-Goals for V2

The following are explicitly out of scope for V2:

- Nationwide or statewide coverage (Yeppoon only for now)
- Real-time live data feeds
- Integration with external accessibility databases (e.g. AccessibleAustralia, Google Maps accessibility data)
- Turn-by-turn navigation
- Voice guidance
- Booking or reservation functionality
- Restaurant menus, opening hours, or general venue information
- Ratings or reviews not related to accessibility
- Social features, comments, or likes
- Automated scoring or AI-generated accessibility ratings
- Gamification

---

## Mobile-First Principles

- The primary experience is on a mobile phone, used on the go.
- UI must work with one hand, on a small screen, in outdoor lighting.
- Text must be large enough to read without zooming.
- Tap targets must be large enough for users with limited dexterity.
- The app must work on slow or intermittent mobile data connections.
- Critical accessibility results must be visible without scrolling.
- The app must not require an account to view accessibility information.

---

## Accessibility Claim Rules

These rules govern what the system may claim and how it must qualify claims.

1. **No overclaiming.** The system must never state something is accessible if the data is incomplete, outdated, or unverified.
2. **Always distinguish data source.** Every claim must be attributable to one of:
   - Verified data (reviewed by a trusted source)
   - User-submitted data (pending review)
   - Outdated data (last verified more than X months/years ago)
   - Unknown data (no information available)
   - Prototype/sample data (for development and demonstration only)
3. **Unknown means caution.** Missing information should produce a ⚠️ result, not a ✅.
4. **Old data degrades confidence.** Data older than a defined threshold should lower the result level or add a caution flag.
5. **Community data is not verified.** User-submitted reports are flagged as unverified until reviewed by a moderator.

---

## Result Language Rules

Three result levels only. No numerical scores. No percentages.

| Symbol | Label | Meaning |
|--------|-------|---------|
| ✅ | Works / Likely works | Based on current verified information, this aspect should work for this user's profile. |
| ⚠️ | Check before you go | Information is incomplete, outdated, uncertain, or there are known caution factors. Call ahead or check in person. |
| ❌ | No / Likely will not work | Based on current information, this aspect is likely to be a blocker for this user's profile. |

Result language must be:
- Plain English
- Specific about why the result was reached
- Honest about what is unknown
- Actionable (what should the user do next?)

---

## Safety and Uncertainty Principles

- A failed outing is a real harm. The system must err on the side of caution.
- When in doubt, output ⚠️ rather than ✅.
- The system must never hide uncertainty to appear more helpful.
- The system must explain its reasoning in plain English.
- The system must identify what a user should verify before going.
- The system must not make the user feel blamed for an inaccessible result.

---

## How V2 Differs from the MVP

| Aspect | MVP | V2 |
|--------|-----|----|
| Scope | Venue accessibility checker | Whole-outing accessibility planner |
| Coverage | Venue entry and use | Parking → pathway → entrance → interior → toilets → return |
| Data model | Simple venue fields | Structured graph of outing components |
| Pathway | Simple getting-there result | Modelled path segments, kerb ramps, crossings, slope, surface |
| Toilets | Single field on venue | Separate toilet entity with full accessibility fields |
| Parking | Simple field | Structured parking area with distance, surface, bay type |
| Data freshness | Not tracked | Explicit freshness and confidence system |
| Community data | localStorage submission form | Structured submission with verification status |
| Evidence | Not supported | Evidence photos attached to claims |
| Moderation | None | Moderation workflow for community data |
| Return journey | Not modelled | Explicit return journey consideration |
