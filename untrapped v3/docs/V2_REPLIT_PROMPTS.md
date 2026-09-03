# V2 Replit Prompts — unTR@PPED Yeppoon

**Status: Stage 0 Planning Draft**

This file contains prompts for resuming work in Replit Agent after a session ends or a crash occurs.
Copy and paste the relevant prompt to pick up work where it left off.

---

## Recovery Prompt (General)

Use this if the Agent has crashed or lost context and you need to re-orient it.

```
You are working on the unTR@PPED Yeppoon V2 project.

This is Stage 0 planning only. No app implementation has started.
Do not build the app. Do not scaffold React. Do not create database, API routes, auth, or map integration.

Read the following files to understand the project before doing anything:
- README.md
- docs/V2_PRODUCT_SPEC.md
- docs/V2_WHOLE_OUTING_MODEL.md
- docs/V2_DATA_MODEL_DRAFT.md
- docs/V2_DECISION_ENGINE_DESIGN.md
- docs/V2_ROADMAP.md

Then confirm you have read them and what stage we are currently in.
Do not make any changes until I give you a specific instruction.
```

---

## Stage 0 Completion Check Prompt

Use this to verify all planning documents are present and correct.

```
Check that the following planning files exist and are not empty:
- README.md
- docs/V2_PRODUCT_SPEC.md
- docs/V2_WHOLE_OUTING_MODEL.md
- docs/V2_DATA_MODEL_DRAFT.md
- docs/V2_DECISION_ENGINE_DESIGN.md
- docs/V2_ROADMAP.md
- docs/V2_RESEARCH_QUESTIONS.md
- docs/V2_REPLIT_PROMPTS.md
- docs/REFERENCE_INDEX.md

Report which files exist and which are missing or empty.
Do not create or modify anything until I confirm what to do.
```

---

## Stage 0 → Stage 1 Transition Prompt

Use this when planning is complete and you are ready to begin the static prototype.

```
We are moving from Stage 0 (planning) to Stage 1 (static whole-outing prototype) of unTR@PPED Yeppoon V2.

Before starting, read:
- docs/V2_PRODUCT_SPEC.md
- docs/V2_WHOLE_OUTING_MODEL.md
- docs/V2_DATA_MODEL_DRAFT.md
- docs/V2_DECISION_ENGINE_DESIGN.md
- docs/V2_ROADMAP.md

Stage 1 goal: A static, mobile-first prototype with hardcoded sample data for 2-3 Yeppoon venues.
No database. No backend. No real data. All data must be clearly labelled as prototype/sample.

Constraints:
- Mobile-first design (primary use case is a phone screen)
- Three result levels only: ✅ / ⚠️ / ❌
- No numerical scores
- Results must include plain English reasons
- Decision engine must follow docs/V2_DECISION_ENGINE_DESIGN.md rules
- Unknown data must produce ⚠️, not ✅
- Prototype data must be clearly labelled

Before writing any code, propose:
1. The tech stack and file structure
2. The sample venues you will use
3. The sample data structure
4. The UI screens/pages

Wait for my approval before starting.
```

---

## Planning Doc Update Prompt

Use this if you need to update a specific planning document.

```
I need to update [FILE NAME] in the docs/ folder.

The current content is in that file. Read it first.

The changes I want to make are:
[Describe the changes]

Do not change anything else. Only update the file I specified.
After making the change, show me a summary of what changed.
```

---

## Research Questions Session Prompt

Use this for a session focused on working through research questions.

```
We are working through the V2 research questions for unTR@PPED Yeppoon.

Read docs/V2_RESEARCH_QUESTIONS.md to understand all the open questions.

I want to work through [SPECIFIC QUESTION NUMBERS OR TOPIC AREA] today.

I will provide answers and context. Your job is to:
1. Help me think through each question
2. Record the decisions we reach
3. Update docs/V2_RESEARCH_QUESTIONS.md with answers or notes
4. Flag if any answer requires a change to another planning document

Start by reading the research questions file and confirming which questions we are working on.
```

---

## Data Model Review Prompt

Use this for a focused session on the data model.

```
We are reviewing and refining the V2 data model for unTR@PPED Yeppoon.

Read docs/V2_DATA_MODEL_DRAFT.md to understand the current draft.

I want to discuss [SPECIFIC ENTITY OR ASPECT].

Do not change the file unless I explicitly ask you to.
Focus on identifying any gaps, contradictions, or missing fields based on:
- docs/V2_WHOLE_OUTING_MODEL.md
- docs/V2_DECISION_ENGINE_DESIGN.md

After we discuss, I will tell you what to update.
```

---

## Decision Engine Review Prompt

Use this for a focused session on the decision engine.

```
We are reviewing and refining the V2 decision engine design for unTR@PPED Yeppoon.

Read docs/V2_DECISION_ENGINE_DESIGN.md to understand the current design.

I want to discuss [SPECIFIC ASPECT — e.g. gradient thresholds, unknown data rules, community data rules].

Do not change the file unless I explicitly ask you to.
Identify any gaps, edge cases, or unclear rules.
After we discuss, I will tell you what to update.
```

---

## Notes for Using These Prompts

- Always read the relevant docs before doing any work. Do not rely on memory from a previous session.
- If in doubt about what stage we are in, ask. Do not assume.
- If something seems to contradict the planning docs, flag it before proceeding.
- Do not expand scope beyond what the current stage requires.
- Do not start implementation work from a planning prompt.
