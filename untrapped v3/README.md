# unTR@PPED Yeppoon V2

**Status: Stage 0 — Planning Only**

No app implementation has started. No React scaffold. No database. No API routes. No frontend components.

---
# unTR@PPED

This project is branded as **unTR@PPED**.

The GitHub repository and local development folder use **unTRaPPED** because `@` can create avoidable issues in URLs, scripts, and development tooling.

---

## What is unTR@PPED?

unTR@PPED is a wheelchair accessibility planning tool for Yeppoon, Queensland, Australia.

The name is an acronym:

| Letter | Meaning |
|--------|---------|
| T | Toilets |
| R | Ramps |
| @ | Accessibility (the @ replaces the A and is part of the brand identity) |
| P | Pathway |
| P | Parking |
| E | Entrances |
| D | Doors |

---

## This Repo vs the MVP

This is V2 — a **separate repo** from the submitted MVP.

The MVP is **frozen**. Do not modify it, continue it, or copy from it without explicit instruction.

V2 starts fresh from this planning stage. The MVP serves as reference material only.

---

## V2 Direction

V2 moves from a "venue accessibility checker" to a **whole-outing accessibility planner**.

The core question V2 is designed to answer:

> "Can I get there, get in, and use it — without surprises?"

---

## Planning Documents

All canonical planning lives in `/docs`:

| File | Purpose |
|------|---------|
| `docs/V2_PRODUCT_SPEC.md` | Vision, problem, scope, principles |
| `docs/V2_WHOLE_OUTING_MODEL.md` | How a whole outing is modelled |
| `docs/V2_DATA_MODEL_DRAFT.md` | Draft data structures (pseudocode only) |
| `docs/V2_DECISION_ENGINE_DESIGN.md` | How the decision engine should evolve |
| `docs/V2_ROADMAP.md` | Staged build plan |
| `docs/V2_RESEARCH_QUESTIONS.md` | Open questions to resolve before building |
| `docs/V2_REPLIT_PROMPTS.md` | Prompts for resuming work in Replit Agent |
| `docs/REFERENCE_INDEX.md` | Index of all reference material |

---

## Primary User

Wheelchair users in Yeppoon, Queensland, Australia.

---

## Key Principles

- Do not overclaim accessibility.
- Three result levels only: ✅ Works / Likely works — ⚠️ Check before you go — ❌ No / Likely will not work.
- No numerical accessibility scores.
- Unknown data creates caution, not fake confidence.
- Old data reduces confidence.
- Community-submitted data is not treated as verified until reviewed.
- Logic must be deterministic and explainable.
- Mobile-first design.
