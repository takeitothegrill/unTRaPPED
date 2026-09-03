# Reference Index — unTR@PPED Yeppoon V2

**Status: Stage 0 Planning Draft**

This file indexes all documents and reference material for the V2 project.

---

## Planning Documents (this repo)

| File | Purpose | Status |
|------|---------|--------|
| `README.md` | Project overview, status, principles, doc index | Stage 0 |
| `docs/V2_PRODUCT_SPEC.md` | Vision, problem, scope, principles, non-goals | Stage 0 |
| `docs/V2_WHOLE_OUTING_MODEL.md` | Full model of a wheelchair outing — all stages | Stage 0 |
| `docs/V2_DATA_MODEL_DRAFT.md` | Draft data structures in plain English + pseudocode | Stage 0 |
| `docs/V2_DECISION_ENGINE_DESIGN.md` | Decision engine logic, rules, and examples | Stage 0 |
| `docs/V2_ROADMAP.md` | Staged build plan from Stage 0 to Stage 6+ | Stage 0 |
| `docs/V2_RESEARCH_QUESTIONS.md` | Open questions to resolve before/during building | Stage 0 |
| `docs/V2_REPLIT_PROMPTS.md` | Prompts for resuming work in Replit Agent | Stage 0 |
| `docs/REFERENCE_INDEX.md` | This file — index of all reference material | Stage 0 |

---

## MVP Reference (separate frozen repo)

The MVP is in a separate repo and must not be modified. It is reference material only.

Key MVP documents for reference:
- `README.md` — MVP overview and build context
- `BUILD_LOG.md` — Chronological build log
- `AI_PROMPTS_LOG.md` — Prompts used during MVP development
- `BUILD_CONTEXT.md` — Technical context and decisions
- `replit.md` — Replit-specific notes

MVP features relevant to V2 reference:
- Wheelchair profile form → V2 UserMobilityProfile
- Venue list and detail page → V2 Venue model
- Getting-there result → V2 Pathway and Parking stages
- Getting-in / using-venue result → V2 Entrance and Interior stages
- Deterministic decision engine → V2 Decision Engine (evolved)
- ✅ / ⚠️ / ❌ result levels → Preserved in V2
- Community submission form → V2 CommunityReport model
- Print / save as PDF outing summary → V2 Stage 1 deliverable
- Share venue link → V2 future consideration
- Google Maps / Apple Maps handoff → V2 Stage 5
- Call-ahead checklist → V2 Decision Engine call-ahead prompts
- Arrival checklist → V2 future consideration

---

## External Reference Standards

Standards and guidelines relevant to accessibility assessment.
These are reference only — V2 does not claim compliance with any standard without specific verification.

### Australian Standards
- **AS 1428.1** — Design for access and mobility: General requirements for access — Buildings
  - Relevant for: door widths, ramp gradients, turning spaces, reach ranges
- **AS 1428.2** — Design for access and mobility: Enhanced and additional requirements
  - Relevant for: accessible toilets, signage, fixtures
- **AS 2890.6** — Parking facilities: Off-street parking for people with disabilities
  - Relevant for: accessible parking bay dimensions and location requirements

### Australian Building Codes
- **National Construction Code (NCC)** — Part D (Access and Egress)
  - Sets minimum requirements for accessible design in new buildings

### Queensland Specific
- **Queensland Development Code (QDC)** — MP 2.1 and related accessibility provisions
- **Disability Discrimination Act 1992 (Cth)** — Legal basis for accessibility requirements
- **Disability Standards for Accessible Public Transport 2002** — If public transport is added

### International Reference
- **WCAG 2.1** — Web Content Accessibility Guidelines — relevant for the app's own accessibility
- **ISO 21542** — Building construction: Accessibility and usability of the built environment

---

## Key Thresholds (Draft — to be confirmed in research)

These are working thresholds used in the V2 decision engine. They are derived from Australian Standards and common practice. They must be validated against research questions in `docs/V2_RESEARCH_QUESTIONS.md`.

| Measurement | Value | Standard Reference | Notes |
|------------|-------|-------------------|-------|
| Minimum door clear width (manual chair) | 820mm | AS 1428.1 | New buildings require 850mm |
| Minimum door clear width (powered chair) | 900mm | Common practice | Varies by chair model |
| Maximum ramp gradient (unassisted) | 1:14 (~7%) | AS 1428.1 | For lengths > 1.5m |
| Maximum ramp gradient (assisted) | 1:8 (~12.5%) | AS 1428.1 | Short ramps only |
| Maximum cross-slope | 1:50 (2%) | AS 1428.1 | |
| Minimum path width | 1000mm | AS 1428.1 | 1200mm preferred |
| Accessible parking bay width | 3800mm (2400mm + 1400mm shared zone) | AS 2890.6 | |
| Turning circle (typical manual chair) | 1500mm diameter | AS 1428.1 | |
| Turning circle (typical powered chair) | 1540–1800mm diameter | Varies by model | |
| Data freshness — aging threshold | 12 months | V2 design decision | To be confirmed |
| Data freshness — stale threshold | 24 months | V2 design decision | To be confirmed |

---

## Accessibility Acronyms and Terms

| Term | Definition |
|------|-----------|
| MLAK | Master Locksmith Access Key — a standard key used to access locked accessible toilets and other facilities across Australia |
| NCC | National Construction Code |
| AS | Australian Standard |
| DDA | Disability Discrimination Act 1992 (Cth) |
| OT | Occupational Therapist |
| Step-free | No steps in the path — does not mean fully accessible |
| Clear opening width | The usable width of a door when fully open (not the door leaf width) |
| Running slope | The slope in the direction of travel |
| Cross-slope | The slope perpendicular to the direction of travel |
| Dropped kerb | A kerb that is lowered to road level, also called a kerb cut or kerb ramp |
| Kerb ramp | A ramp that transitions between footpath and road level |

---

## Change Log

| Date | Change | Author |
|------|--------|--------|
| 2026-05-02 | All Stage 0 planning documents created | Initial planning |
