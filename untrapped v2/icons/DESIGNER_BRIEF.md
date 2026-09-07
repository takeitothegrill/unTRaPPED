# unTRaPPED — map icon set: designer brief

**Date:** 7 September 2026

**Context:** Feedback on the first draft icon set. Every constraint below was **measured on
the live Google My Maps platform**, not assumed — including some findings that overturned
our own earlier assumptions.

---

## 1. The thinking has changed (and it's better)

Two things that were previously tangled have been separated:

**The map legend** — kept deliberately simple, because someone scanning a map has very
little attention to spend:

- **Parking**
- **Toilets**
- **Routes**
- **Venues**

**The TRAPPED assessment model** — the detailed data underneath, which is *not* the legend:
**T**oilet, **R**amp, **A**ccessible interior, **P**arking, **P**athway, **E**levator,
**D**oor.

So TRAPPED is how we *assess* a place; it is not what the user has to decode on the map.
The map stays cognitively simple, the rigour lives underneath. **No design work is needed
for the seven TRAPPED categories** — only the four legend types below.

How the assessment data folds into the four map types:

| Assessment (TRAPPED) | Map legend |
|---|---|
| **T** — Toilet | Toilets |
| **P** — Parking | Parking |
| **R** — Ramp | Routes |
| **P** — Pathway | Routes |
| **E** — Elevator | Routes |
| **D** — Door | Routes |
| **A** — Accessible interior | Venues |
| Venue | Venues |

Everything about *getting there and getting through* — ramps, pathways, elevators, doors —
collapses into **Routes**. That's four things a user never has to distinguish while
scanning, but which we still assess and record separately underneath.

---

## 2. The system — three rules

> **Shape = category. Blue = a facility you hunt for. Otherwise, colour = rating.**

There are **two families**, and each has one rule.

**Family 1 — facilities you scan for: Parking and Toilets.** Pin shape, **always blue**,
white letter, and a **small coloured dot at the bottom-right** carrying the rating.

- Blue means "an accessible facility is here". Someone hunting a toilet or a parking bay
  is scanning for that blue, so it must **stay constant across all three ratings** — if
  the body changed colour, the thing they are scanning for would disappear.
- The rating still has to be visible, so it rides in the dot. See §6.5 for its position.

**Family 2 — things you assess rather than hunt for: Routes and Venues.** The **whole
shape takes the rating colour** — green, orange or red. **No dot.**

- You do not scan a map for "a venue" or "a route"; you already know where you are going,
  and the only question is whether you can get in or get through. So colour is free to
  carry the rating entirely, which is far stronger at 18px than any dot.
- A red wheelchair icon tells the story on its own.

**No slashes, crosses or prohibition marks anywhere in the set** — a deliberate principle,
not an omission. See §2.1.

### 2.1 No slashes or prohibition marks — the map informs, it does not adjudicate

**Please do not add slashes, crosses or "no entry" bars to any icon in this set.** Red on
its own carries the message.

The reasoning matters, because it will come up again:

- **People's abilities vary enormously.** A slash effectively says *"not for you"* — but the
  map does not know who is reading it. Someone with a wheelie-walker may manage what a
  powerchair user cannot, and vice versa. That judgement belongs to the person, not the icon.
- **A prohibition mark can do real harm.** Someone in urgent need of a toilet, seeing a
  crossed-out icon, may skip a facility they could actually have used. The map would then
  have failed the exact person it exists to serve.
- **Red already communicates "worst tier".** A red wheelchair icon tells the story without
  dictating the outcome.

Severity and danger are still communicated clearly — just not by the icon. They live in the
**pin title and description**, which are far better instruments for it, because they can be
specific. The existing naming convention already does this well: pins read
`PATHWAY - [DANGEROUS]`, `ACCESS - disability [NO!]`, `TOILET - disabled [BROKEN!!!]`. That
warns precisely, without the icon presuming to rule on anyone's ability.

---

## 3. The icon set — 12 files

| # | Icon | Shape | Body | Glyph | Dot | Meaning |
|---|---|---|---|---|---|---|
| 1 | Parking – good | Pin | Blue | White **P** | Green | Accessible parking, usable |
| 2 | Parking – caution | Pin | Blue | White **P** | Orange | Usable with difficulty |
| 3 | Parking – barriers | Pin | Blue | White **P** | Red | Poor — read the details |
| 4 | Toilet – good | Pin | Blue | White **T** | Green | Accessible toilet, usable |
| 5 | Toilet – caution | Pin | Blue | White **T** | Orange | Usable with difficulty |
| 6 | Toilet – barriers | Pin | Blue | White **T** | Red | Poor — read the details |
| 7 | Route – good | Circle | **Green** | White moving wheelchair | — | Accessible route |
| 8 | Route – caution | Circle | **Orange** | White moving wheelchair | — | Difficult route |
| 9 | Route – barriers | Circle | **Red** | White moving wheelchair | — | Poor — read the details |
| 10 | Venue – good | Square | **Green** | White wheelchair | — | Accessible venue |
| 11 | Venue – caution | Square | **Orange** | White wheelchair | — | Partly accessible |
| 12 | Venue – barriers | Square | **Red** | White wheelchair | — | Poor — read the details |

**Note the consistency:** within each family the glyph never changes — only the colour does.
Routes and Venues keep the same white wheelchair glyph and recolour the whole body;
Parking and Toilets keep the same white **P** / **T** on blue and change only the dot.
Nothing is crossed out, ever.

**Only six of the twelve icons carry a rating dot** — the three Parking and the three
Toilets. Routes and Venues have no dot at all.

---

## 4. Hard constraints — measured, not assumed

These should drive the design more than anything else.

### 4.1 Icons render at about 18 pixels. That's the whole budget.

Measured in the live public viewer's DOM: a 128×128 source displays at **18×18 px**.
Critically, we tested this at **zoom 18 and zoom 22 — identical both times.** Zooming in
spreads pins apart but **never makes them bigger**. There is no size control anywhere in
Google My Maps; we checked every style panel.

**Also note: the editing view lies.** It renders markers at **32px** while the public sees
**18px**. Anything judged while editing looks ~1.8× better than what users actually get.

See `_size_reality_check.png` — the old toilet icon at true size and magnified. At 18px it
is an unreadable smudge. Detail only holds together from ~48px, and we never get 48px.

### 4.2 Google adds nothing. Your artwork is exactly what appears.

We initially believed Google wrapped uploads in its own pin frame. **That was wrong and
we've corrected it.** Google renders the uploaded PNG as-is.

- **Draw the full shape yourself** (pin / circle / square) — nothing is added.
- **Every transparent pixel of margin is wasted map real-estate.** At an 18px budget, a 20%
  margin costs nearly 4 of your only 18 pixels. **Fill the canvas edge to edge.**

### 4.3 On sharpness — what is and isn't fixable

Google **re-encodes uploaded icons down to about 128px**, so you cannot supply a
"retina-sharp" asset; and Google's own map icons look crisper because they are rendered
server-side into the map tiles at exactly the right size each time. That pipeline isn't
available to custom icons.

**We tested SVG specifically, because vector artwork would have solved this outright.**
An SVG uploaded via Google Photos *is* accepted and renders correctly on the map — but we
inspected what the map actually serves, and it is a **128×128 PNG**, not a vector. Google
rasterises the SVG on ingest. We confirmed the pin on the map was genuinely the
SVG-derived file (its rating dot sits at a different position from our PNG version, and
that offset matched precisely). So SVG is a valid *delivery* format, but it gains nothing:
it hits the same 128px ceiling as a PNG.

**Conclusion: vector is not an escape route. There is no way to get more than ~128px
into the map.**

The good news: at normal 100% browser zoom the icon is *downscaled* (128 → 18), which is
inherently sharp. **What actually causes visible mushiness is fine detail, not resolution.**
Bold, simple, high-contrast shapes downsample cleanly; small internal details do not.
So the fix is design, not file size.

---

## 5. Design decisions already tested — please follow these

Each of these was rendered at true 18px and compared before deciding.

- **The wheelchair symbol is removed from Parking and Toilets.** On a map where everything
  is about accessibility, it's redundant — it was consuming half the available pixels
  restating what the map already says. One bold glyph, not two competing symbols.
  *(It stays on Venues, where it's the only glyph, not a second one.)*
- **Rating goes in a coloured dot, not a coloured glyph.** We tested colouring the P/WC
  letterform itself. It works, but costs twice: the glyph loses crispness (white on blue is
  maximum contrast), and it **fails in greyscale** — green, orange and red letterforms are
  near-identical to a red-green colour-blind user. A solid dot survives downscaling far
  better than a coloured letter shape, and keeps the glyph white. See
  `_glyph_colour_test.png`.
- **"WC" does not work — use "T".** Two letters cannot fit legibly in 18px; "WC" renders as
  mush. A toilet-bowl silhouette was also tested and collapses into an ambiguous blob at
  actual size. Bold **"T"** reads cleanly. See `_toilet_glyph_test.png`.
  *Noted honestly: "P" for parking is universal signage; "T" for toilet is not a learned
  convention, so the map legend carries that meaning.*
- **The colour band around the pin edge is dropped.** Tested at maximum zoom: it renders as
  a 1–2 pixel sliver and is not readable as a rating signal.
- **Routes and Venues take green / orange / red as the whole shape.** Neither has a *type*
  the user is hunting for, so colour is free to carry the rating entirely — and a fully
  coloured shape is a far stronger signal at 18px than a 4px dot. Green/amber/red is also a
  very strong existing convention. This is a deliberate asymmetry with the blue facilities,
  accepted knowingly: the differing shapes (circle, square, pin) keep it learnable, and the
  blue is reserved for exactly the two things people scan the map hunting for.
- **~~Routes icons are the strongest work in the set~~ — this no longer holds.** It was
  true of the *first* draft, whose route icon was a simple bold wheelchair. The redrawn
  version added a racing pose and speed lines and **fails at 18px**. See §6.10. Use the
  **Parking and Toilet** icons as the quality reference instead.

---

## 6. Treatment — border, colour and glyph weight

Four changes requested after seeing the draft on a live map. All four were rendered through
the **real** pipeline before answering — 512px artwork → 128px (Google's re-encode) → 18px
(display) — because a treatment that looks right on the artboard can vanish entirely by the
time it reaches the map.

### 6.1 Add a white border. Yes — and here is the exact weight.

Confirmed: the icons need the outline that makes Google's own markers sit *on* the map
rather than *in* it. Without one, a blue pin over dark-green satellite imagery loses its
edge completely.

- **Border colour: white.** A dark outline was tested and is worse — it defines the shape
  nicely on the pale map background but muddies badly against satellite, and it makes the
  whole set look heavier and more dated.
- **Border weight: about 1px as displayed** = **28px on a 512px canvas** (~5.5% of width).
- **Half that (14px / ~0.5px displayed) does almost nothing** — it disappears in the
  downsample. **Double it (42px / ~1.5px) and the blue body is visibly eaten away** for no
  extra separation. 28 is the sweet spot, not a rough guess.
- **The border must come out of the shape, not be added around it.** The outer silhouette
  still fills the canvas edge-to-edge; the blue body is inset by the border width. Growing
  the icon outward to make room for a border is not possible — there is no room.

### 6.2 The drop shadow — tested, and it does not survive. Recommend leaving it off.

This was tested carefully because it was specifically asked for, and the request is sound:
Google's markers *do* carry a soft shadow, and it is part of why they read as crisp.

**But it does not transfer to a custom icon, for two measurable reasons:**

1. **A shadow needs margin to fall into, and margin is size.** Reserving 8% of the canvas
   for the shadow shrinks the visible pin by roughly 2 of its only 18 pixels — a real,
   visible loss of size (see Fig 5, rows C and D against row A).
2. **At 18px the shadow renders as a faint grey smudge under the pin** — on satellite it is
   effectively invisible, and on the pale map background it slightly dirties the lower edge
   rather than lifting the icon.

**The important part: the white border already does the job the shadow was wanted for.**
Separation from the background is the actual goal, and a 1px white ring achieves it at a
fraction of the cost. Google can afford both because their icons are composited server-side
into the tile at native size; we are shipping one small raster and cannot.

*This is a recommendation, not a veto — if you try a shadow and it holds up at 18px, we'll
look. But please judge it at 18px, never on the artboard.*

### 6.3 Rating colours — go fluro. Exact values below.

Confirmed: the current green is too dark. Against a mid-blue pin it reads as a muddy blob
rather than a signal. The fluro set is dramatically stronger at actual size (Fig 6, row 2
against row 1) — and the whole point of the dot is that it must survive being 4px across.

| Rating | Old | **New (fluro)** |
|---|---|---|
| Green | `#228B3C` | **`#00E676`** |
| Orange | `#F08214` | **`#FF9100`** |
| Red | `#D02626` | **`#FF1744`** |

Orange and red were brightened to match. This matters: if only the green were lifted, it
would out-shout the other two, and a set where "good" is the loudest signal misleads at a
glance. All three must carry equal weight — the dot's job is to be *read*, not to rank.

Keep the white ring around the dot. It is what stops the fluro colours bleeding into the
blue body at 18px.

**These same three values coloured the whole body of the Route circles and Venue squares.**
One palette does both jobs, so a red venue and a red parking dot are unmistakably the same
red — which is what makes the rating readable across the set rather than per-icon.

### 6.4 The glyph — heavier and larger, up to a limit

- **Weight: use a black/heavy weight, not bold.** Arial Black vs Arial Bold was compared at
  actual size and the heavier cut is clearly more legible (Fig 6, last two rows).
- **Size: about 0.66 of the pin-head width** — noticeably larger than the current draft.
- **Do not go past ~0.66 for the "P".** At 0.74 the enclosed counter (the hole in the P)
  starts closing up in the downsample, and it crowds the rating dot. It looks bigger on the
  artboard and reads *worse* on the map.
- **The "T" can go larger — to ~0.74** — because it has no enclosed counter to fill in. The
  ceiling is set by the letterform, not by a single rule, so please check each glyph at 18px
  rather than applying one number to both.

### 6.5 Rating dot position — move it to the BOTTOM-right

The dot currently sits top-right, hard against the shoulder of the "P". It is too close,
and it breaks down completely on the "T". Moving it to the **bottom-right** fixes both.

This is a letterform problem, not a taste one:

- **"P"** carries its mass in the upper half — the stem up the left, the bowl to the
  upper-right. Its **lower-right is empty space.**
- **"T"** is worse: the crossbar occupies the **entire top of the letter.** A dot at
  top-right lands directly on the end of that crossbar and eats it. At 18px the result
  reads closer to an "F" than a "T" (see Fig 7, top row).
- Bottom-left is no better — that is where the "P" puts its stem.

**So the only corner that is genuinely empty in both letters is the bottom-right.** With
the dot there, both glyphs keep their full shape and there is clear blue between letter
and dot at actual size.

**This only affects six icons**, and conveniently they are the only two glyphs involved:
the three Parking and the three Toilets. Routes and Venues carry no dot at all (§2), so
there is no third letterform to compromise for — bottom-right can simply be right.

### 6.6 Review of the first orange-P sample — three things to change

The first sample is **close**, and the two big calls in it are right: the dot is at the
bottom-right, and the P is bold and well-sized. Three things are costing it at 18px
(Fig 8 — the sample rebuilt and run through the real pipeline, against the same design
with these three fixed).

**1. There are two outlines. Use one.** The sample has a blue outer stroke *and* a white
ring inside it. At 18px the outer blue stroke merges with the blue body, so the white ring
stops reading as separation and instead reads as a pale gap eating into the middle of the
shape. The whole icon comes out washed-out and low-contrast. **One white border, 28px on
the 512 canvas, and nothing outside it.**

**2. The rating dot has three layers. Use two.** The sample builds it as an outer orange
ring, then a white ring, then an orange core. The dot is only about **4px across on the
map** — three concentric bands cannot possibly resolve at that size, and they blur into a
soft orange smudge with a pale halo. **Solid orange fill, one white ring, nothing else.**

**3. There is roughly 6% dead margin.** The artwork does not reach the edge of the canvas.
We measured the delivered file on the map: its content occupies **104 of the 128 pixels**
of width, so about a fifth of the width is transparent padding. At an 18px budget that is
close to **3 pixels of visible icon thrown away**. **Fill the canvas edge to edge** (§4.2).

**Also, minor:** the body has a subtle vertical gradient. It is invisible at 18px and it
slightly *lowers* contrast with the white P where the blue is lightest. Flat colour is
marginally better and never worse.

The colours themselves are good — the orange is very close to the specified `#FF9100`.

### 6.7 Second sample, measured on the live map — nearly there

The revised parking icon is applied and working, and it is a clear step up: the **"P" now
reads cleanly at 18px** and the orange dot registers. Compare it against the earlier
P-plus-wheelchair icon at the same size and the difference is obvious — one bold glyph
beats two competing ones every time.

We pulled the actual file off the map and scanned a line across the pin head. In 128px
units, left edge inwards:

```
.9      9px transparent margin
B4      blue outer stroke
W2      white ring        <- only 2px
...     blue body and the P
W3 B3   white ring, then blue stroke again
.10     10px transparent margin
```

Three refinements left, all pulling the same way:

- **Remove the outer blue stroke.** The white ring must be the **outermost** thing on the
  icon. Anything outside it merges with the blue body at 18px and softens the edge, which
  is what is still making the outline look slightly fuzzy.
- **Thicken the white ring — this is the highest-value fix.** It is currently 2–3px in a
  128px file. The spec is 28px on a 512 canvas, which is **7px at 128** — so it is running
  at under half weight. That is why the edge reads soft rather than crisp.
- **Close the remaining margin.** 9px left + 10px right = **15% of the width still empty.**
  Better than the 19% in the first sample, but not gone.

**These compound.** Drop the outer stroke, fill the canvas, and bring the white ring to
full weight, and the blue body grows from roughly 96px to roughly 114px of the 128 —
about **19% more icon**, with room for the "P" to grow with it.

### 6.8 The "P" needs a longer stem — agreed, and here is how far it can go

Correct, and it is worth doing: a longer stem makes the letter read more like standard
parking signage and gives it a more distinctive silhouette at 18px. A font "P" — including
the Arial Black we originally specced — has a deep bowl and a stubby stem, and it looks
squat on the pin.

**The limit is set by the counter — the enclosed hole in the bowl — not by taste.** As the
bowl gets shallower to lengthen the stem, the counter is squeezed between the top and
bottom strokes and closes up. Once it closes, the bowl downsamples into a solid blob and
the letter stops reading as a "P" at all (Fig 9, bottom row).

Expressing the bowl height as a fraction of cap height:

| Bowl | Result at 18px |
|---|---|
| ~0.64 (font default) | Reads, but squat — the stem barely shows |
| 0.58 | Good, comfortable counter |
| **0.52** | **Best — clearly longer stem, counter still open. Use this.** |
| 0.46 | **Fails** — counter closed, bowl is a blob |

**The rule to design by, which generalises past this one letter:** *lengthen the stem until
the counter is about to close, then stop.* Concretely, **keep the counter at least ~40px on
the 512 canvas** — that is roughly 10px once Google re-encodes to 128, and about 1.5px on
screen. Below that it fills in.

**Bonus:** a longer stem lifts the bowl away from the bottom-right rating dot, so the two
elements crowd each other slightly less than in the current sample.

### 6.9 Third sample — measured on the live map, and passing

Measured off the file Google is actually serving, not the artboard:

| | 1st sample | 2nd | **3rd (current)** |
|---|---|---|---|
| Canvas width used | 81% | 86% | **91%** |
| Outlines | 2 (blue outside white) | 2 | **1 — white only** |
| White border @128 | 2px | 2–3px | 3px *(spec is 7px)* |
| Rating dot layers | 3 | 2 | **2** |
| "P" counter | — | — | **~20px @128 = 2.8px on screen** |

Scanline across the pin head reads `.8 W3 B27 ... B23 W3 .8` — one white run at each
edge with nothing outside it. **The outer blue stroke is gone.** The longer stem worked:
the stem measures 71 of 128 vertically and the counter is running at nearly twice the
~1.5px floor, so it holds at 18px comfortably.

**On the white border, we are revising our own advice down.** It has been raised in three
consecutive rounds, so it was tested to see whether it still earns another one:

- **On the road map the difference is invisible** — white on a cream background does nothing.
- **On satellite there is a visible but modest gain.**

At 3px it renders as roughly 0.42px on screen, so it reads as a soft fringe rather than a
ring. But the blue is saturated enough to hold its own edge. **Fold the border to full
weight into a future round if one happens anyway; it does not justify a round on its own.**

**This sample is approved.** The three things that mattered — the double outline, the
three-layer dot, and the dead margin — are fixed. Please build the remaining icons to
match it, applying §6.3 (colours), §6.5 (dot bottom-right, Parking and Toilets only) and
§6.8 (stem length, counter floor).

### 6.10 Full set reviewed at 18px — Routes need rework, everything else passes

All eleven were sliced out of the delivered sheet and run through the real pipeline, on
road-map and satellite grounds (Fig 10).

**Toilets and Parking — approved.** Both letters read cleanly on both backgrounds, all
three dot colours register. Consistent with the two already signed off.

**Venues — approved, and we were wrong to doubt them.** We expected the wheelchair to turn
to mud and built two simplified alternatives to replace it. **Both were worse than what you
delivered** (Fig 11). The ISO wheelchair survives downscaling better than our simplifications
because it is a symbol people already know — partial cues are enough to trigger recognition,
where a novel simplified shape has no familiarity to fall back on. A solid-wheel version
reads as a blob; a ring-wheel version reads as a magnifying glass. **Keep the venues as
drawn.** This is a genuine exception to "simplify everything", and worth remembering:
*a highly-learned symbol degrades more gracefully than a novel one.*

**Routes — these fail, and need redrawing.** At 18px the racing wheelchair is an
unreadable jumble; you cannot tell it is a wheelchair. Three problems compound:

1. **The speed lines are thin strokes** that merge into the figure and into each other.
2. **The wheel's counter fills in**, so the wheel stops reading as a wheel.
3. **The dynamic "racing" pose is not a widely-learned shape** — so unlike the Venue
   wheelchair, there is no familiarity to carry it through the degradation.

**Recommendation: drop the wheelchair from Routes and use an arrow.** The reasoning is
already established in §5 — *on a map where everything is about accessibility, a wheelchair
is redundant*, which is exactly why it was removed from Parking and Toilets. It applies
equally here. Routes mean **getting there and getting through**, so direction is the natural
metaphor, an arrow is unmistakable at 18px (Fig 11), and it keeps the wheelchair meaningful
as specifically *"a destination you can get into"* on Venues.

*Honest caveat:* an arrow on a Google map may read as "get directions". A double chevron
avoids that association but is slightly less legible. Either beats the current version.

#### Is removing the speed lines enough on its own?

Tested directly, since it is the smaller change (Fig 12). **It is a real improvement but
not sufficient.** With the lines gone the clutter goes and the wheel and figure separate
into a cleaner mark — but it still does not read as a *wheelchair*. It reads as an abstract
shape: a circle with a diagonal stroke and a dot above it.

This is the Venue finding pointing the other way. The ISO wheelchair survives because it is
already learned; the racing pose has no familiarity to fall back on, so once detail is lost
there is nothing holding it together. Removing the lines takes away noise but adds no
recognition.

**So the speed lines must go either way. The open question is only whether the wheelchair
goes with them**, and that is a legitimate design choice:

- **If the glyph should carry meaning → use the arrow.** Readable, and it says "getting
  there and getting through", which is what Routes are.
- **If shape and colour carry the meaning → the de-lined wheelchair is defensible.**
  Circles are already distinct from pins and squares, colour already carries the rating,
  and the legend teaches what a circle means. The glyph then only needs to be a clean,
  distinct mark — which, with the lines gone, it is.

**One thing not to do: reuse the ISO wheelchair from Venues on Routes.** It would read, but
Routes and Venues would then differ only by circle-vs-square — too weak a distinction at
18px. The arrow keeps them genuinely separate and lets the wheelchair mean something
specific on Venues: *a destination you can get into*.

### 6.11 Routes redrawn — approved. Set complete. Arrow recommendation withdrawn.

The redrawn route icons (512x512 RGBA, canvas filled 100%) pass at 18px. The figure was
enlarged and thickened and the speed lines removed; critically, **the wheel's hub now
survives the downscale**, which is the specific feature that failed before. It reads as a
structured, deliberate mark on both road map and satellite.

**We withdraw the arrow recommendation from §6.10.** We concluded the racing wheelchair
could not work at 18px and that the metaphor had to change. That was wrong: the problem was
**size and weight, not the symbol**. Enlarging and boldening fixed it. The general lesson
holds — detail below the surviving-size threshold fails — but we jumped to replacing the
glyph when scaling it up was sufficient. Worth recording, because the same reflex would have
cost the set its visual identity for no reason.

**No white border on Routes or Venues.** It was tested specifically on the weakest pairing
in the set — green on green vegetation (Fig 13). A border does separate better on grass and
canopy, **but it costs glyph clarity**, because the artwork must shrink to make room and the
wheelchair visibly softens. The fluro green is far brighter than any natural vegetation
green, so separation is already adequate. **Pins keep their border; circles and squares do
not need one.** This asymmetry is deliberate.

**Status: all 12 approved.**

| Family | Icons | State |
|---|---|---|
| Parking | 3 | Approved |
| Toilets | 3 | Approved |
| Routes | 3 | Approved |
| Venues | 3 | Approved |

Remaining optional item, for a future round only: the white border on the pins is running at
2–3px in a 128px file against a 7px spec. Tested and judged not worth a round on its own
(§6.9).

## 7. File specifications

- **Format:** PNG, transparent background (alpha channel)
- **Canvas:** square, **512 × 512 px** — supplied high-res so Google's downsample is clean.
  It will *display* at ~18px; design accordingly.
- **Artwork:** fills the canvas edge-to-edge, no dead margin
- **White border: 28px on the 512 canvas**, taken out of the shape (see §6.1)
- **No drop shadows** (see §6.2), **no thin outlines and no fine internal detail** — the
  1px border is the one exception, and it only works because it is deliberately heavy
- **Check every concept at 18px before finalising** — and check it downsampled *twice*
  (512 → 128 → 18), not once. This is the single most useful thing you can do.
- **Naming** — by rating colour. This is now accurate as well as simple: on facilities the
  *dot* really is that colour, and it matches the `rating` values in our data exactly, so no
  translation is needed anywhere.

```
parking-green.png    toilet-green.png     route-green.png     venue-green.png
parking-orange.png   toilet-orange.png    route-orange.png    venue-orange.png
parking-red.png      toilet-red.png       route-red.png       venue-red.png
```

- **Delivery:** individual PNG files — not a combined reference sheet. Usable assets can't
  be extracted from a flattened composite.
- Please also supply the **editable source** (AI / SVG / Figma). The current V1 icon set
  exists only as flat PNGs with no source, which is exactly why it can't be adjusted now.

---

## 8. The rating scale — settled

One scale, applied consistently across all four types:

| | Meaning |
|---|---|
| **GREEN** | Works / accessible |
| **ORANGE** | Check before you go — difficult |
| **RED** | **Barriers** — read the details before deciding |

Red spans a genuine range: a usable-but-unpleasant toilet, and a venue up a flight of stairs
with no lift. The icon deliberately does not try to separate those — the **description**
does, and it can be specific in a way an 18px icon never could.

This honours the project's existing house rule from the V2/V3 planning docs — *do not
overclaim accessibility; unknown data creates caution, not fake confidence* — and extends
the same discipline in the other direction: **do not over-prohibit either.** The map informs
the decision; the person makes it.
