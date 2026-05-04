# V2 Data Model Draft — unTR@PPED Yeppoon

**Status: Stage 0 Planning Draft**

This document uses plain English descriptions and TypeScript-like pseudocode.
This is NOT production code. Types may change significantly before implementation.
No database schema. No migrations. No imports.

---

## Shared Types

```
type ResultLevel = "ok" | "caution" | "blocked"
// ✅ ok = Works / Likely works
// ⚠️ caution = Check before you go
// ❌ blocked = No / Likely will not work

type VerificationStatus = 
  | "verified"           // Reviewed and confirmed by a trusted admin
  | "community"          // Submitted by a community user, not yet reviewed
  | "pending_review"     // Submitted, in the review queue
  | "rejected"           // Reviewed and rejected as inaccurate
  | "prototype"          // Sample data for development/demonstration only

type DataFreshness = {
  lastAssessedDate: date | null
  assessedBy: string | null         // "admin", "community", or name/ID
  freshnessStatus: "fresh" | "aging" | "stale" | "unknown"
  // fresh: within 12 months
  // aging: 1-2 years
  // stale: over 2 years
  // unknown: no date recorded
}
```

---

## UserMobilityProfile

Captures the individual's wheelchair needs. Outing results are personalised against this.

```
type UserMobilityProfile = {
  wheelchairType: "manual" | "powered" | "heavy_powered"
  
  // Physical dimensions
  widthCm: number | null           // Chair width in cm
  lengthCm: number | null          // Chair length in cm
  turningCircleCm: number | null   // Turning circle diameter in cm
  
  // Capability
  maxRampGradient: "1:14" | "1:12" | "1:8" | "assisted_only"
  canOpenHeavyDoors: boolean
  canMountKerb: boolean            // Small kerbs only
  requiresHoist: boolean
  mlakKeyHolder: boolean           // Has an MLAK accessible toilet key
  
  // Travel context
  hasCarer: boolean
  comfortableCallingAhead: boolean
}
```

---

## Venue

A place the user wants to visit.

```
type Venue = {
  id: string
  name: string
  address: string
  suburb: string
  lat: number
  lng: number
  venueType: "cafe" | "restaurant" | "shop" | "park" | "medical" | "beach" | "government" | "other"
  
  // Associated entities
  parkingAreas: ParkingArea[]
  entrances: Entrance[]
  toilets: Toilet[]
  pathSegments: PathSegment[]      // Segments from nearest accessible parking to entrance
  
  // Data quality
  verification: VerificationStatus
  freshness: DataFreshness
  notes: string | null
  evidencePhotos: EvidencePhoto[]
  temporaryObstructions: TemporaryObstruction[]
}
```

---

## ParkingArea

A specific parking location associated with a venue.

```
type ParkingArea = {
  id: string
  venueId: string
  label: string                    // e.g. "Main Street carpark", "On-street outside venue"
  
  hasDesignatedAccessibleSpace: boolean | null
  numberOfAccessibleSpaces: number | null
  accessibleSpaceWidthCm: number | null   // Width of accessible bay
  
  surfaceType: "sealed" | "gravel" | "grass" | "mixed" | null
  surfaceCondition: "good" | "fair" | "poor" | null
  
  hasKerbRampToFootpath: boolean | null
  distanceToEntranceMetres: number | null  // Approximate walking distance to venue entrance
  
  // Restrictions
  timeLimit: string | null         // e.g. "2 hour limit", "No limit"
  cost: string | null              // e.g. "Free", "Pay and display"
  
  notes: string | null
  verification: VerificationStatus
  freshness: DataFreshness
  evidencePhotos: EvidencePhoto[]
}
```

---

## PathSegment

A single continuous segment of path between two points on the outing route.

```
type PathSegment = {
  id: string
  venueId: string
  
  fromLabel: string                // Human description of start point
  toLabel: string                  // Human description of end point
  sequenceOrder: number            // Order in the route
  
  widthCm: number | null
  surfaceType: "concrete" | "asphalt" | "pavers" | "gravel" | "grass" | "mixed" | null
  surfaceCondition: "good" | "fair" | "poor" | null
  runningSlopePercent: number | null   // % gradient along direction of travel
  crossSlopePercent: number | null     // % gradient across direction of travel
  
  hasObstacles: boolean | null
  obstacleNotes: string | null
  
  isCovered: boolean | null
  
  notes: string | null
  verification: VerificationStatus
  freshness: DataFreshness
  evidencePhotos: EvidencePhoto[]
}
```

---

## KerbRamp

A kerb ramp or dropped kerb at the junction between a path and a road.

```
type KerbRamp = {
  id: string
  pathSegmentId: string | null
  venueId: string | null
  
  isPresent: boolean | null
  widthCm: number | null
  gradientPercent: number | null
  hasLipOrRaisedEdge: boolean | null
  isFlushWithRoad: boolean | null
  condition: "good" | "fair" | "poor" | null
  isCurrentlyObstructed: boolean | null
  obstructionNotes: string | null
  
  notes: string | null
  verification: VerificationStatus
  freshness: DataFreshness
  evidencePhotos: EvidencePhoto[]
}
```

---

## Crossing

A pedestrian crossing point on the outing route.

```
type Crossing = {
  id: string
  pathSegmentId: string | null
  venueId: string | null
  
  crossingType: "signalised" | "marked_unsignalised" | "unmarked" | null
  hasDroppedKerbs: boolean | null   // Both sides
  hasAudibleSignal: boolean | null
  hasMedianIsland: boolean | null
  medianIslandAccessible: boolean | null
  roadWidthMetres: number | null
  condition: "good" | "fair" | "poor" | null
  
  notes: string | null
  verification: VerificationStatus
  freshness: DataFreshness
  evidencePhotos: EvidencePhoto[]
}
```

---

## Entrance

A way into a venue. A venue may have multiple entrances.

```
type Entrance = {
  id: string
  venueId: string
  label: string                    // e.g. "Main entrance", "Rear accessible entrance"
  
  isStepFree: boolean | null
  hasRamp: boolean | null
  rampGradientPercent: number | null
  isMainEntrance: boolean
  isSignedAsAccessible: boolean | null
  requiresIntercom: boolean | null
  intercomReachableFromWheelchair: boolean | null
  
  // Door at entrance
  door: Door | null
  
  notes: string | null
  verification: VerificationStatus
  freshness: DataFreshness
  evidencePhotos: EvidencePhoto[]
}
```

---

## Door

A door that may block or allow access. Used for entrance doors and interior doors.

```
type Door = {
  id: string
  label: string                    // e.g. "Main entrance door", "Toilet door"
  
  clearOpeningWidthCm: number | null
  doorType: "automatic" | "push" | "pull" | "sliding" | "double" | null
  isHeavy: boolean | null
  requiresTwoHands: boolean | null
  handleType: "lever" | "knob" | "push_plate" | "none" | null
  isCurrentlyPropOpen: boolean | null
  
  notes: string | null
  verification: VerificationStatus
  freshness: DataFreshness
  evidencePhotos: EvidencePhoto[]
}
```

---

## Toilet

An accessible toilet at or near the venue.

```
type Toilet = {
  id: string
  venueId: string
  label: string                    // e.g. "Accessible toilet, ground floor"
  
  isPresent: boolean
  isDedicatedAccessible: boolean | null   // Not shared with ambulant/general use
  requiresMlakKey: boolean | null
  isCurrentlyAccessible: boolean | null   // May be locked, out of order, etc.
  
  // Features
  doorWidthCm: number | null
  turningSpaceCm: number | null
  hasGrabRails: boolean | null
  grabRailPosition: string | null   // e.g. "both sides", "left only"
  panHeightCm: number | null
  hasAccessibleBasin: boolean | null
  basinClearanceUnderCm: number | null
  hasHoist: boolean | null
  
  // Location
  isOnAccessibleRoute: boolean | null
  locationNotes: string | null
  
  notes: string | null
  verification: VerificationStatus
  freshness: DataFreshness
  evidencePhotos: EvidencePhoto[]
}
```

---

## Hazard

An ongoing known hazard on the outing route.

```
type Hazard = {
  id: string
  venueId: string
  
  hazardType: "step" | "narrow_path" | "poor_surface" | "steep_slope" | "obstacle" | "other"
  location: string                 // Plain English description of location
  description: string
  severity: "minor" | "significant" | "blocker"
  isOngoing: boolean               // True = permanent, False = temporary (use TemporaryObstruction)
  
  notes: string | null
  verification: VerificationStatus
  freshness: DataFreshness
  evidencePhotos: EvidencePhoto[]
}
```

---

## TemporaryObstruction

A time-limited obstruction that may affect the outing.

```
type TemporaryObstruction = {
  id: string
  venueId: string
  
  obstructionType: "construction" | "event" | "parked_vehicle" | "maintenance" | "market" | "weather" | "other"
  location: string
  description: string
  
  reportedDate: date
  expectedEndDate: date | null
  isConfirmedResolved: boolean
  resolvedDate: date | null
  
  severity: "minor" | "significant" | "blocker"
  
  verification: VerificationStatus
  evidencePhotos: EvidencePhoto[]
  submittedBy: string | null
}
```

---

## EvidencePhoto

A photo attached to any entity as supporting evidence.

```
type EvidencePhoto = {
  id: string
  attachedToEntityType: string   // "venue" | "toilet" | "entrance" | "path_segment" | etc.
  attachedToEntityId: string
  
  url: string                    // Storage URL
  caption: string | null
  dateTaken: date | null
  submittedBy: string | null
  
  verification: VerificationStatus
  submittedDate: date
}
```

---

## CommunityReport

A report submitted by a community user about any aspect of a venue or route.

```
type CommunityReport = {
  id: string
  venueId: string | null
  
  reportType: "new_information" | "correction" | "temporary_hazard" | "resolved_hazard" | "general"
  affectedEntityType: string | null   // What entity this report is about
  affectedEntityId: string | null
  
  description: string
  submittedDate: date
  submitterContact: string | null   // Optional — for follow-up only
  
  verificationStatus: "pending_review" | "verified" | "rejected"
  reviewedBy: string | null
  reviewedDate: date | null
  reviewNotes: string | null
  
  evidencePhotos: EvidencePhoto[]
}
```

---

## OutingPlan

A planned outing for a specific user profile to a specific venue.

```
type OutingPlan = {
  id: string
  venueId: string
  userProfile: UserMobilityProfile
  
  selectedParkingAreaId: string | null
  selectedEntranceId: string | null
  pathSegmentIds: string[]
  
  createdDate: date
  notes: string | null
}
```

---

## OutingResult

The computed result of assessing an outing plan.

```
type OutingResult = {
  outingPlanId: string
  
  overallResult: ResultLevel
  
  // Stage results
  parkingResult: StageResult
  pathwayResult: StageResult
  entranceResult: StageResult
  interiorResult: StageResult
  toiletResult: StageResult
  returnJourneyResult: StageResult
  
  // What to check before going
  callAheadPrompts: string[]
  
  // Summary
  summaryText: string
  unknowns: string[]             // List of things not known
  staleDateWarnings: string[]    // List of data that is outdated
  temporaryHazardWarnings: string[]
  
  computedAt: datetime
}

type StageResult = {
  stage: "parking" | "pathway" | "entrance" | "interior" | "toilet" | "return"
  result: ResultLevel
  reasons: string[]              // Plain English reasons for the result
  unknownFactors: string[]       // What is not known
  callAheadPrompts: string[]     // What to ask if calling ahead
}
```
