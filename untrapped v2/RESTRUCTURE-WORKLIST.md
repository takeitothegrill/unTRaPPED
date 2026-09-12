# V1 working copy — restructure worklist

Map: `unTRaPPED Livingstone - V1 working copy 260906`
`https://www.google.com/maps/d/edit?mid=1GsgVncG-IYRalSk_u7ZmuDQluhPQmpQ`

State at audit: **7 layers, 88 pins, 254 photos.**

**Do this work IN THE MAP, by hand.** Photo attachments cannot be re-imported
from a CSV (tested 2026-09-06 — `gx_media_links` imports as plain text, not as
attachments). Exporting, fixing and re-importing would destroy all 254 photos.

---

## Step 1 — rename layers, don't create new ones

You are at 7 of a maximum 10 layers. Renaming gets you the target shape without
spending any:

| current layer | becomes | pins |
|---|---|---|
| `Car Park (disability)` | **Parking** | 16 |
| `Toilets` | **Toilets** | 26 |
| `PATHWAY ACCESS - disability` | **Routes** | 25 |
| `VENUE ACCESS` | **Venues** | 15 |
| `YEPPOON CBD` | keep as town locator | 3 |
| `EMU PARK CBD` | keep as town locator | 1 |
| `AMENITIES adapted for disabled` | empty it, then delete | 2 |

Result: 4 feature layers + 2 town locators = **6 layers**, leaving 4 spare for
more towns.

⚠ The legend order may be INVERTED against the map's z-order. Observed once on v7
(the layer at the BOTTOM of the list drew on TOP of the map), never deliberately
tested. Decide which matters more before you settle the order.

---

## Step 2 — move these 19 pins to the right layer

Drag the pin between layers in the editor panel.

### → move to PARKING (12 pins — the biggest problem by far)

From **Toilets**:
- [ ] PARKING - disabled [OKAY]
- [ ] PARKING - disabled [GOOD]
- [ ] PARKING - disabled [GOOD]
- [ ] PARKING - disabled [OKAY]
- [ ] PARKING - disabled [EXCELLENT]

From **PATHWAY ACCESS**:
- [ ] PARKING - disabled [GOOD]
- [ ] PARKING - disability [OKAY]
- [ ] PARKING - disability [EXCELLENT]

From **VENUE ACCESS**:
- [ ] PARKING - disability [EXCELLENT]
- [ ] PARKING [GOOD]
- [ ] PARKING disability [EXCELLENT]
- [ ] PARKING - disability [EXCELLENT]

### → move to TOILETS (3 pins)

From **PATHWAY ACCESS**:
- [ ] TOILET - disabled [POOR]
- [ ] TOILET - NO disabled toilet here

From **VENUE ACCESS**:
- [ ] TOILET - disabled [GOOD]

### → move to ROUTES (2 pins)

From **Toilets**:
- [ ] PEDESTRIAN CROSSING - disabled [EXCELLENT]

From **VENUE ACCESS**:
- [ ] PATHWAY [POOR]

### → move to VENUES (2 pins)

From **Toilets**:
- [ ] Keppel Bay Plaza [excellent]
- [ ] VENUE - aquatic centre [EXCELLENT]

---

## Step 3 — 12 pins need your eyes

These could not be classified from their names. Only you know what they are:

- `YEPPOON CBD` layer: 1 pin
- `Toilets` layer: 3 pins
- `AMENITIES adapted for disabled`: 2 pins
- `PATHWAY ACCESS`: 1 pin
- `VENUE ACCESS`: 5 pins

---

## Step 4 — naming, once pins are in the right layers

Settled convention: `TOWNSHIP | TYPE - Place [RATING]`, e.g.
`YEPPOON | PARKING - James St 1 [OKAY]`. Number multiples at one site.

- `disabled` → `disability` for Parking and Toilets
- Routes state the SURFACE (`grass`, `concrete`)
- Venues state the VENUE TYPE (`playground`, `cafe`, `plaza`)
- Keep names under ~40 characters — the legend truncates with an ellipsis and
  the END is what is lost, so never put the rating last on a long name.

**Also put the searchable location line at the top of each description:**
`[place name], <address>, <township>`. The public viewer's search matches
description text and surfaces this map's pins first, so everything at one site
(e.g. "Lioness Park") surfaces together. This matters more than the legend.

---

## Step 5 — once tidy

Set the map's default view (map ⋮ → Set default view) to the main town, then
publish via Share → "Anyone with this link can view". Leave the second toggle
("let others search for and find this map") OFF unless you want it publicly
discoverable.
