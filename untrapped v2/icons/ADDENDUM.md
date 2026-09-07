# unTRaPPED icon set — addendum: the remaining 11

**Date:** 7 September 2026  ·  **Read with:** `unTRaPPED-designer-brief.pdf` (full rationale)

---

## 1. The parking icon is approved — build the rest to match it

We measured the file off the live map (not the artboard) and it passes. Use it as the
reference for everything else: one white outline, flat colour, two-layer rating dot, long
stem, artwork filling the canvas.

Two things you do **not** need to change: the border weight is slightly under spec but we
tested it and the gain is not worth a round on its own, and the letterform proportions are
yours to keep — they work.

---

## 2. Two changes since the brief you were working from

**These are the important ones. Everything else is unchanged.**

### 2.1 Venues are no longer blue

Blue is now reserved for the two things people *scan the map hunting for* — Parking and
Toilets. Venues and Routes are things you assess once you already know where you're going,
so they take the rating colour as the whole shape.

| Family | Icons | Body colour | Rating shown by |
|---|---|---|---|
| Facilities you hunt for | Parking, Toilets | **always blue** | small dot, bottom-right |
| Things you assess | Routes, Venues | **green / orange / red** | the whole shape — **no dot** |

**So only six of the twelve carry a rating dot.** Routes and Venues have none at all.

### 2.2 The rating dot moved to the BOTTOM-right

It was top-right. It has to move, and the reason is the "T": a **T's crossbar occupies the
entire top of the letter**, so a top-right dot lands on the end of the crossbar and eats
it — at 18px it reads closer to an "F". Bottom-right is the only corner genuinely empty in
both "P" and "T".

---

## 3. The remaining 11

| # | Icon | Shape | Body | Glyph | Dot |
|---|---|---|---|---|---|
| 1 | Toilet – good | Pin | Blue | White **T** | Green, bottom-right |
| 2 | Toilet – caution | Pin | Blue | White **T** | Orange, bottom-right |
| 3 | Toilet – barriers | Pin | Blue | White **T** | Red, bottom-right |
| 4 | Parking – good | Pin | Blue | White **P** | Green, bottom-right |
| 5 | Parking – barriers | Pin | Blue | White **P** | Red, bottom-right |
| 6 | Route – good | Circle | **Green** | White moving wheelchair | none |
| 7 | Route – caution | Circle | **Orange** | White moving wheelchair | none |
| 8 | Route – barriers | Circle | **Red** | White moving wheelchair | none |
| 9 | Venue – good | Square | **Green** | White wheelchair | none |
| 10 | Venue – caution | Square | **Orange** | White wheelchair | none |
| 11 | Venue – barriers | Square | **Red** | White wheelchair | none |

*(Parking – caution is the approved sample, already delivered.)*

---

## 4. Colours — one palette does both jobs

| Rating | Hex |
|---|---|
| Green | `#00E676` |
| Orange | `#FF9100` |
| Red | `#FF1744` |

These are the **dot** colours on Parking and Toilets **and** the **body** colours on Routes
and Venues. Same values both places, so a red venue and a red parking dot are unmistakably
the same red.

---

## 5. The two icons most likely to give trouble

### 5.1 The "T" — watch the crossbar

The T is top-heavy and its crossbar runs the full width of the letter. It has no enclosed
counter, so it can go **larger than the P** — up to about 0.74 of the pin-head width. Keep
the dot clear of the crossbar's right arm; bottom-right does this, top-right does not.

### 5.2 The wheelchair — the riskiest shape in the set

It is the only glyph with real internal detail, and it appears on **six** icons. A standard
system wheelchair symbol turns to mud at 18px — we tested one and it is unreadable.

- Draw a **simplified, heavier** wheelchair, not a traced accessibility symbol.
- The **head, back and wheel arc** are what make it recognisable. Footplates, spokes, arm
  detail and gaps under 1.5px on screen are not — drop them.
- It is white on a saturated colour, so you have full contrast to work with. Use it.

---

## 6. The rule that governs all of it

**Every element has a minimum surviving size, and the enclosed holes fail first.**

Icons display at **18 × 18 px** — always, at every zoom. Google re-encodes your 512px file
to 128px first, so check every glyph by downscaling **512 → 128 → 18**, not in one step,
and never judge it on the artboard.

Concretely: **keep any enclosed counter or gap at least ~40px on the 512 canvas** — about
10px at 128, about 1.5px on screen. Below that it fills in and the shape becomes a blob.
This is what sets the limit on the P's stem, and it is what will decide whether the
wheelchair works.

---

## 7. Delivery

- **PNG, transparent background, 512 × 512**, artwork filling the canvas edge to edge
- Individual files, not a combined sheet
- Plus the **editable source** (AI / SVG / Figma)
- Naming by rating colour:

```
toilet-green.png    parking-green.png    route-green.png    venue-green.png
toilet-orange.png   parking-red.png      route-orange.png   venue-orange.png
toilet-red.png                           route-red.png      venue-red.png
```
