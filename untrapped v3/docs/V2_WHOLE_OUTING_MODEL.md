# V2 Whole Outing Model — unTR@PPED Yeppoon

**Status: Stage 0 Planning Draft**

---

## What Is a Whole Outing?

A whole outing is everything a wheelchair user must navigate to successfully visit a destination and return home. It is not just the venue. It begins before arrival and ends after return.

The V2 system models the outing as a sequence of stages, each of which can succeed, require caution, or fail. A single failure in any stage can block or ruin the entire outing.

---

## Outing Stages

### 1. Starting Context

Who is going and what are their needs?

- User's wheelchair type (manual / powered / heavy powered)
- User's turning circle / width requirements
- User's ramp gradient tolerance
- User's ability to open heavy doors
- Whether a carer is present
- Whether the user is comfortable calling ahead

This is captured in the User Mobility Profile (see data model). The outing result is personalised against this profile.

---

### 2. Parking

Can the user park close enough to begin the outing?

Considerations:
- Is there a designated accessible parking space (with the blue wheelchair symbol)?
- Is the space wide enough for the user's vehicle and to deploy a ramp or hoist?
- What is the surface of the parking area? (sealed, unsealed, gravel, grass)
- Is there a kerb between the parking space and the footpath?
- Is there a kerb ramp or cut kerb at the exit point of the parking space?
- How far is the parking space from the venue entrance?
- Is the path between parking and entrance physically possible? (see pathway)
- Is the parking space legally marked and currently available? (unknown — caution)
- Are there temporary obstructions? (delivery vehicles, bins, construction)

Result: ✅ / ⚠️ / ❌ for parking reachability

---

### 3. Pathway Segments

Can the user travel from parking to the venue entrance?

A pathway is broken into segments. Each segment has its own assessment.

Each pathway segment considers:
- Start point and end point
- Surface type (concrete, asphalt, pavers, gravel, grass, mixed)
- Surface condition (smooth, cracked, uneven, potholed, waterlogged)
- Width (is it wide enough for the wheelchair?)
- Slope / gradient (cross-slope and running slope)
- Presence of obstacles (poles, signs, bins, outdoor seating)
- Whether it is covered or exposed (weather consideration)
- Lighting (relevant for low-light outings)
- Data freshness and source

If any segment cannot be traversed, the pathway fails.

---

### 4. Kerb Ramps

At each point where a path meets a road or raised kerb, is there a kerb ramp?

Considerations:
- Is a kerb ramp present?
- Is it in good condition?
- Does it have a lip or raised edge that could catch a wheelchair?
- Is it flush with the road surface?
- Is it wide enough?
- Is it located at the correct position (aligned with the crossing)?
- Is it currently obstructed? (parked cars, construction)

A missing kerb ramp at a crossing point is a hard blocker if the user cannot mount a kerb.

---

### 5. Crossings

Does the user need to cross a road to reach the venue?

Considerations:
- Is there a pedestrian crossing?
- Is it a signalised crossing (with pedestrian lights and audible signals)?
- Are there dropped kerbs at both ends?
- Is the crossing in good condition?
- Is there a median island? If so, is it wheelchair-accessible?
- How wide is the road? (more crossings = more risk)
- Are there vehicles that may not stop?

---

### 6. Slope

Are there gradients along the pathway or ramps that exceed the user's tolerance?

Considerations:
- Running slope (the slope along the direction of travel)
- Cross-slope (the slope across the direction of travel — can cause drift)
- Ramp gradient (if a ramp is present, is the gradient within accessible limits?)
- Is the slope data measured or estimated?
- Does the slope change with weather? (wet conditions make steep surfaces more dangerous)

Standard accessible gradient is generally 1:14 or gentler (approximately 7%) for unassisted access, 1:8 (12.5%) with assistance. These are reference figures; the system should personalise based on user profile.

---

### 7. Surface Condition

Is the surface safe and usable?

Considerations:
- Cracked or broken concrete
- Uneven pavers
- Gravel or loose surface
- Wet or slippery surface
- Mud or waterlogging after rain
- Temporary surfaces (plywood, matting)
- When was this last assessed? (freshness matters)

Surface condition is time-sensitive. Recent community reports may be more accurate than old verified data.

---

### 8. Temporary Hazards

Are there current obstructions or conditions that may affect the outing?

Temporary hazards include:
- Construction works blocking a path or ramp
- Outdoor events that change access routes
- Parked vehicles blocking kerb ramps or accessible spaces
- Markets or street furniture temporarily narrowing paths
- Weather-related hazards (flooding, slippery surfaces)
- Maintenance works (resurfacing, scaffolding)

Temporary hazard data has a short useful life. The system should flag when temporary hazard information may be stale.

---

### 9. Entrance

Can the user enter the venue?

Considerations:
- Is there a step-free entrance?
- If there is a ramp, is the gradient within the user's tolerance?
- Is the entrance door automatic or manual?
- If manual, is it heavy? Does it require two hands?
- Is the entrance clearly signed and easy to find?
- Is there an alternative accessible entrance? (and is it clearly marked and not via a service area?)
- Is the entrance currently available? (some venues lock accessible entrances — caution)
- Is there an intercom required to access the venue?

A step at the entrance with no ramp alternative is a hard blocker for most wheelchair users.

---

### 10. Doors

Can the user operate the internal doors?

Considerations:
- Width (minimum 850mm clear opening for powered chairs; 800mm for manual)
- Type (automatic, push, pull, lever, knob, keypad)
- Weight (heavy fire doors may be impassable without assistance)
- Are doors propped open during opening hours?
- Is there a lobby with two doors in quick succession? (may trap the user)

---

### 11. Interior Movement

Can the user move around inside the venue?

Considerations:
- Floor surface (carpet pile, tiles, timber, uneven flooring)
- Internal ramps or steps between levels
- Lift access if multiple levels (is the lift large enough? Is it currently working?)
- Aisle width (particularly in shops, cafes, medical centres)
- Turning space at key points (counter, seating area, toilet)
- Seating flexibility (can the user remain in their wheelchair at a table?)
- Counter height (can the user reach and see over the counter?)

---

### 12. Toilets

Can the user use an accessible toilet at the venue?

Considerations:
- Is there an accessible toilet?
- Is it a dedicated accessible toilet (not a combined accessible/ambulant/general toilet)?
- Is it currently available and not locked? (some require a MLAK key)
- Does the user have or need a MLAK key?
- Internal layout: grab rail positions, turning space, pan height, basin accessibility
- Is there a hoist? (for users who require one)
- Is the toilet on an accessible path from the main venue area?
- How recently was the toilet information verified?

Accessible toilet data is particularly important and particularly prone to being outdated.

---

### 13. Destination Use

Can the user actually use the venue for its intended purpose?

Considerations vary by venue type:
- Cafe/restaurant: Can the user sit at a table in their wheelchair? Is the counter reachable?
- Shop: Are the aisles wide enough? Can the user reach displays and checkout?
- Park: Are the paths, picnic areas, and facilities accessible?
- Medical centre: Is the waiting room accessible? Is the consultation room accessible?
- Beach: Is there a beach wheelchair? Are the paths to the water accessible?

This stage is venue-type specific and may rely on community knowledge.

---

### 14. Return Journey

Can the user return to their vehicle or transport?

The return journey often has different considerations:
- The user may be more fatigued
- Conditions may have changed (weather, temporary obstructions)
- The route may need to be the same or different to the outbound route

The system should flag return journey considerations where relevant, particularly for:
- Temporary hazards that may change during the outing
- Time-limited parking
- Venues with restricted accessible parking nearby

---

### 15. Unknowns

What is not known about this outing?

The system must explicitly surface what information is missing. Unknowns include:
- Fields with no data recorded
- Fields where data exists but is outdated
- Fields where community data exists but is unverified
- Aspects of the venue that have not been assessed

Unknowns must generate ⚠️ caution results, not ✅ results.

---

### 16. Confidence

How confident is the system in its results?

Confidence is a function of:
- How many fields are known vs unknown
- How recent the data is
- Whether data is verified or community-submitted
- Whether the user profile matches the assessed user profile (if any)

Confidence is expressed in plain English, not as a number or percentage.

Examples:
- "Based on verified information from 2024"
- "Based on community report from 3 months ago — not yet reviewed"
- "Some information is missing — check before you go"
- "This information is over 2 years old — conditions may have changed"

---

### 17. Freshness

How old is the data?

Each piece of information has a recorded date. The system uses freshness thresholds to flag outdated data.

Proposed freshness thresholds (to be confirmed in research):
- Fresh: assessed within the last 12 months
- Aging: assessed 1–2 years ago (add caution flag)
- Stale: assessed more than 2 years ago (lower confidence, add strong caution)
- Unknown: no date recorded (treat as stale)

Freshness thresholds may vary by data type. Physical infrastructure (ramps, door widths) changes slowly. Temporary obstructions change daily.

---

### 18. Evidence and Photos

What evidence supports the claims?

Evidence photos can be attached to:
- Venue features
- Path segments
- Parking areas
- Kerb ramps
- Crossings
- Entrances
- Toilets

Evidence photos have:
- A date taken
- A submitter (verified admin, community user, or anonymous)
- A caption or description
- A verification status

Photos are reference material. They do not automatically verify a claim. They help a user judge for themselves.
