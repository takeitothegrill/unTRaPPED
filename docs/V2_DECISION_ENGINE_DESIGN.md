# V2 Decision Engine Design — unTR@PPED Yeppoon

**Status: Stage 0 Planning Draft**

---

## Overview

The V2 decision engine inherits the core principles from the MVP:

- Three result levels only: ✅ / ⚠️ / ❌
- No numerical scores or percentages
- Deterministic, explainable logic
- Results personalised to the user's wheelchair profile
- Unknown data creates caution, not fake confidence

V2 extends the engine to cover the whole outing, not just a single venue check.

---

## Result Levels

| Symbol | Label | Meaning |
|--------|-------|---------|
| ✅ | Works / Likely works | Current verified information indicates this should work for this user's profile. |
| ⚠️ | Check before you go | Information is incomplete, outdated, conflicting, or there are known caution factors. The user should call ahead or check in person. |
| ❌ | No / Likely will not work | Current information indicates a hard blocker exists for this user's profile. |

The engine must never output a ✅ to avoid worrying the user. When in doubt, output ⚠️.

---

## Outing Stages

The engine assesses each stage of the outing independently, then produces an overall result.

Stages:
1. Parking
2. Pathway (parking to entrance)
3. Entrance
4. Interior movement
5. Toilets
6. Return journey

Each stage produces its own ResultLevel with reasons.

The overall result is the worst result across all stages. If any stage is ❌, the overall result is ❌. If no stage is ❌ but any stage is ⚠️, the overall result is ⚠️.

---

## Hard Blockers

A hard blocker is a condition that produces an automatic ❌ result for a specific user profile.

Hard blockers must be explicit, not inferred. The system should explain exactly why the result is blocked.

Examples of hard blockers:

**Parking:**
- No accessible parking space exists and the user requires one
- The parking surface is impassable (e.g. deep gravel, grass) for the user's chair type
- No kerb ramp exists where one is required and the user cannot mount a kerb

**Pathway:**
- A segment has no width measurement and the venue notes narrow aisles (→ ⚠️ not ❌ without confirmation)
- A segment has confirmed width below the user's wheelchair width
- A segment has confirmed slope exceeding the user's maximum ramp gradient tolerance
- A crossing has no dropped kerbs and the user cannot mount a kerb

**Entrance:**
- A step at the only entrance with no ramp alternative and the user cannot mount kerbs
- A door width below the user's wheelchair width

**Interior:**
- No accessible path between entrance and the area the user needs to reach
- No lift where one is required and stairs are the only alternative

**Toilet:**
- No toilet at the venue and the user requires one for outings of this duration (→ flags as ⚠️, user decides)
- Toilet confirmed present but locked and requires MLAK key the user does not have

---

## Caution Items

A caution item produces a ⚠️ result. It does not block the outing but requires the user to check before going.

Caution items include:

- Any required field has no data recorded (unknown)
- Data exists but is outdated (aging or stale)
- Data exists but is community-submitted and not yet verified
- A temporary obstruction has been reported
- A known hazard exists that may affect this user profile
- The user's profile has requirements that are not confirmed (not blocked, just unconfirmed)
- A call-ahead is recommended to confirm a specific condition

---

## Unknown Data Rules

Unknown data must always generate at least a ⚠️ result, never a ✅.

The engine must never assume that absence of negative information means accessibility is fine.

Examples:
- Door width not recorded → ⚠️ (door may be too narrow)
- Kerb ramp not assessed → ⚠️ (ramp may be absent or in poor condition)
- Toilet presence unknown → ⚠️ (user cannot rely on a toilet being available)
- Parking surface unknown → ⚠️ (surface may be impassable)

The engine must communicate what is unknown so the user knows what to check.

---

## Old Data Rules

Data age degrades confidence. The engine applies freshness rules to adjust results.

| Freshness Status | Effect |
|-----------------|--------|
| Fresh (< 12 months) | No penalty. Use result as assessed. |
| Aging (1–2 years) | Add ⚠️ caution flag. Include note: "This information is 1–2 years old — conditions may have changed." |
| Stale (> 2 years) | Downgrade result one level if currently ✅. Downgrade to ⚠️ minimum. Include note: "This information is over 2 years old — please verify before your outing." |
| Unknown age | Treat as stale. |

Old data never automatically produces ❌. It signals to the user they should verify, not that the outing is blocked.

---

## Community-Submitted Data Rules

Community submissions are not treated as verified until reviewed by a moderator.

| Verification Status | Effect |
|---------------------|--------|
| Verified | Trust as normal. Apply freshness rules. |
| Community (unverified) | Maximum result level is ⚠️. Always note: "This is based on a community report that has not been reviewed." |
| Pending review | Same as community unverified. |
| Rejected | Do not use in assessment. Flag that a report was made but found to be inaccurate (only if relevant). |
| Prototype | Never use in live assessments. Display only in prototype/demo mode with clear labelling. |

---

## Temporary Hazard Rules

Temporary hazards affect results for the duration they are active.

- An active temporary hazard that blocks access → ❌ (with note that it may be temporary)
- An active temporary hazard that causes difficulty → ⚠️ with description
- A temporary hazard with an expected resolution date → note the expected date
- A temporary hazard that may be resolved (unconfirmed) → ⚠️ with note to check

Temporary hazard data has a short useful life. If a temporary hazard was reported more than 14 days ago with no update, flag it as potentially stale.

---

## Personalisation Against User Profile

The engine applies the user's mobility profile to each assessment.

Examples:
- Door width 820mm: ✅ for standard manual chair, ⚠️ for heavy powered chair requiring 900mm
- Ramp gradient 1:10: ✅ for assisted user, ⚠️ for unassisted user at this gradient, ❌ for user who stated maximum is 1:14
- Kerb ramp with 20mm lip: ✅ for some powered chairs, ❌ for users who cannot mount any lip
- No MLAK key: toilet requiring MLAK key → ❌ for this specific user despite toilet being present

The engine must not apply a ✅ for a condition that may work for most users but does not work for this specific user.

---

## Clear Reasons

Every result must include plain English reasons.

The reasons must:
- State specifically what was assessed
- State specifically what was found (or not found)
- State specifically why this produced the result
- Avoid jargon

Examples:

Good reason: "The entrance has a step with no ramp alternative. This venue is not wheelchair accessible from the main entrance."

Bad reason: "Entrance non-compliant."

Good reason: "The toilet is present but the door width has not been measured. It may be too narrow for some wheelchairs — check before you go."

Bad reason: "Toilet data incomplete."

---

## Call-Ahead Prompts

Where information is unknown or uncertain, the engine generates specific call-ahead prompts.

Call-ahead prompts are plain English questions the user can ask the venue by phone.

Examples:
- "Is the accessible toilet currently unlocked and in use?"
- "Is there accessible parking directly outside the venue?"
- "Is the rear accessible entrance currently open?"
- "Has the construction on Main Street affected access to the venue?"
- "Are there any temporary changes to the entrance?"

Call-ahead prompts should only be generated where they would genuinely help resolve uncertainty. Do not generate prompts for hard blockers (the user already knows not to go).

---

## Stage-by-Stage Assessment Logic

### Getting There (Parking + Pathway)

1. For each parking area: assess accessible space, surface, kerb ramp, distance
2. For each path segment: assess width, surface, slope, obstacles
3. For each kerb ramp on route: assess presence, condition, gradient, lip
4. For each crossing on route: assess dropped kerbs, signals, safety
5. Aggregate: any hard blocker → ❌, any caution → ⚠️, all clear → ✅

### Getting In (Entrance)

1. Assess step-free access (or ramp)
2. Assess door width and type
3. Assess intercom if required
4. Aggregate as above

### Using the Venue (Interior + Toilets)

1. Assess internal movement path
2. Assess floor surfaces
3. Assess toilet presence and features
4. Aggregate as above

### Returning

1. Flag any time-limited parking
2. Flag any temporary hazards that may change during the outing
3. Note if return route is the same as outbound or different
4. Generally mirrors the Getting There result unless conditions are likely to change

---

## What the Engine Must Not Do

- Must not output a numerical score (e.g. "73% accessible")
- Must not output percentage confidence
- Must not blend unknown data into a ✅ result
- Must not state a venue "is accessible" without qualification
- Must not assume a venue meets a standard unless specifically verified
- Must not treat sample or prototype data as real data in live mode
- Must not produce a result without an explanation
- Must not produce a result that contradicts its own evidence
