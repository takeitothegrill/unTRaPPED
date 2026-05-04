# V2 Research Questions — unTR@PPED Yeppoon

**Status: Stage 0 Planning Draft**

These are open questions that should be answered before or during Stage 1 development. Some require user research. Some require expert consultation. Some require local knowledge.

Questions are grouped by area.

---

## User Research Questions

These questions need input from wheelchair users in Yeppoon.

### Outing Planning
1. What is the most common reason a planned outing fails or is abandoned?
2. What information do wheelchair users currently check before going to a new venue?
3. What sources do they currently use? (Phone call to venue, Google, Facebook, word of mouth, past experience)
4. What information is consistently missing or unreliable?
5. How far in advance do users typically plan an outing?
6. Do users plan outings alone or with others (carers, family)?

### Parking
6. How important is designated accessible parking vs general parking close to the venue?
7. Do users travel with vehicles that require ramp/hoist deployment? What bay width do they need?
8. How far is "too far" to travel from parking to a venue entrance?

### Pathway
9. What pathway features cause the most problems? (Surface, slope, kerb ramps, crossings, obstructions)
10. How do users currently assess whether a path is usable? (Memory, photos, asking others)

### Toilets
11. How often does toilet availability affect whether a user will go on an outing?
12. Do most users carry a MLAK key? Is MLAK key availability a significant barrier?
13. What toilet features are most important? (Turning space, grab rails, door width, pan height)

### Technology and Comfort
14. What devices do users use to access accessibility information? (Phone, tablet, desktop)
15. Are users comfortable using apps while on an outing? Or is it mostly used for pre-planning?
16. Do users want to contribute information? What would make them comfortable submitting reports?
17. What makes an accessibility app trustworthy vs untrustworthy?

---

## Local Knowledge Questions

These questions require knowledge of Yeppoon specifically.

### Venues
18. Which are the most commonly visited venues by wheelchair users in Yeppoon?
19. Which venues are known to be difficult or impossible to access?
20. Which venues have made recent accessibility improvements?

### Infrastructure
21. Are there known problem kerb ramps or crossings in central Yeppoon?
22. Are there any ongoing or planned construction works affecting accessibility routes?
23. Which carparks have designated accessible spaces and in what condition are they?

### Local Resources
24. Is there a local disability access advocacy group or council committee in Livingstone Shire?
25. Has Livingstone Shire Council conducted any accessibility audits? Are those publicly available?
26. Are there existing datasets of Yeppoon venue accessibility? (Council, tourism, disability groups)

---

## Data Model Questions

These questions affect how the data model is designed.

### Measurements and Thresholds
27. What is the minimum door width for different wheelchair types? (To confirm values in model)
28. What gradient thresholds should be used for different user profiles?
29. How is "turning space" measured in practice? (Diameter of turning circle?)
30. What MLAK lock types exist in Yeppoon? Are all keys interchangeable?

### Freshness
31. What is the right threshold for "fresh" vs "aging" vs "stale" data?
    - Does it differ by data type? (A ramp gradient changes slowly; a temporary obstruction changes daily)
32. Should freshness thresholds be configurable? Or fixed in the system?

### Verification
33. Who should be a trusted verifier? (Council staff, disability access consultants, OT, admin)
34. What is the minimum evidence required to upgrade community data to verified?
35. Should photo evidence count as partial verification? Or is it still unverified?

---

## Decision Engine Questions

These questions affect how the decision engine is designed.

### Gradients
36. At what gradient should a ramp move from ✅ to ⚠️ for an unassisted manual wheelchair user?
37. At what gradient should it move from ⚠️ to ❌?
38. Does this differ by surface? (Wet concrete vs dry concrete vs pavers)

### Door Width
39. What is the minimum clear opening width for:
    - Standard manual wheelchair?
    - Standard powered wheelchair?
    - Heavy powered wheelchair?
40. Should these be user-configurable or fixed?

### Unknown Data
41. If 80% of data is known and 20% is unknown, should the result be ⚠️ or ❌?
42. Are there specific fields whose absence alone should trigger ❌ rather than ⚠️?

### Profile Matching
43. If data was assessed for a "typical" wheelchair but the user has a non-standard chair, how should results be qualified?
44. Should the system ask for wheelchair dimensions, or use general categories (manual/standard powered/heavy powered)?

---

## Community and Moderation Questions

45. What is the moderation capacity? (Who reviews submissions and how often?)
46. Should anonymous submissions be allowed? What are the risks?
47. Should submitters be notified when their report is reviewed?
48. What happens when a verified record is contradicted by a community report?
49. How should disputes between community reports be handled?
50. Should venues be able to submit information about their own accessibility? How should this be labelled?

---

## Legal and Ethical Questions

51. Does publishing accessibility information create any legal liability if the information is incorrect?
52. Should the system include a disclaimer? What should it say?
53. Are there any privacy considerations for evidence photos? (People may appear in photos)
54. What are the implications of displaying ❌ for a venue? Could a business object?
55. Should venue owners be notified before a ❌ result is published?

---

## Priority

Questions to prioritise before Stage 1:

- Questions 1–5 (what fails outings, what information is needed)
- Questions 36–43 (gradient and door width thresholds for decision engine)
- Questions 18–20 (which Yeppoon venues to use for sample data)
- Questions 27–30 (measurements and thresholds for data model)
