#!/usr/bin/env python3
"""First-pass icon set for unTRaPPED V2 — 8 categories x 3 ratings.

Draws simple, bold, high-contrast glyphs with Pillow primitives (no external
icon libraries), each composited onto a coloured circle to match the style
of the site's existing icons (icon-toilet-red.png etc). Confirmed via live
testing that Google My Maps auto-wraps a plain circular image like this into
its own pin-drop (teardrop) frame on upload, so no pin shape is drawn here —
just the circle + glyph.

Output: icons/output/<category>-<rating>.png  (24 files: 8 categories x 3)

This is a draft for review, not final art — swap in real designed glyphs
later without touching the pipeline (custom icon upload just needs a PNG).
"""
from pathlib import Path
from PIL import Image, ImageDraw

OUT = Path(__file__).resolve().parent / "output"
OUT.mkdir(exist_ok=True)

SIZE = 240          # canvas
CIRCLE_R = 108       # circle radius, leaves a small margin
CENTER = SIZE // 2
STROKE = 14          # glyph line thickness

RATING_COLORS = {
    "green": (46, 125, 50),
    "orange": (245, 124, 0),
    "red": (211, 47, 47),
}
GLYPH_COLOR = (255, 255, 255, 255)
TRANSPARENT = (0, 0, 0, 0)


def new_canvas():
    return Image.new("RGBA", (SIZE, SIZE), TRANSPARENT)


def circle_bg(color):
    img = new_canvas()
    d = ImageDraw.Draw(img)
    d.ellipse(
        [CENTER - CIRCLE_R, CENTER - CIRCLE_R, CENTER + CIRCLE_R, CENTER + CIRCLE_R],
        fill=color + (255,),
    )
    return img


# ---- glyph drawing functions -------------------------------------------
# Each draws white glyph lines onto the given ImageDraw at canvas center.

def glyph_toilets(d):
    # tank (rounded rect) + bowl (ellipse) + base
    d.rounded_rectangle([CENTER - 26, CENTER - 60, CENTER + 26, CENTER - 30], radius=6,
                         outline=GLYPH_COLOR, width=STROKE)
    d.ellipse([CENTER - 34, CENTER - 15, CENTER + 34, CENTER + 45],
              outline=GLYPH_COLOR, width=STROKE)
    d.line([CENTER - 34, CENTER + 15, CENTER + 34, CENTER + 15], fill=GLYPH_COLOR, width=STROKE - 4)


def glyph_ramps(d):
    # incline triangle + small wheel circle at the base
    pts = [(CENTER - 55, CENTER + 45), (CENTER + 55, CENTER + 45), (CENTER + 55, CENTER - 15)]
    d.line([pts[0], pts[2]], fill=GLYPH_COLOR, width=STROKE)
    d.line([pts[0], pts[1]], fill=GLYPH_COLOR, width=STROKE)
    d.ellipse([CENTER - 62, CENTER + 30, CENTER - 30, CENTER + 62],
              outline=GLYPH_COLOR, width=STROKE - 4)


def _wheelchair(d, cx, cy, scale=1.0):
    r_wheel = 34 * scale
    d.ellipse([cx - r_wheel, cy - r_wheel + 20 * scale, cx + r_wheel, cy + r_wheel + 20 * scale],
              outline=GLYPH_COLOR, width=int(STROKE * 0.75 * scale))
    d.ellipse([cx + 6 * scale, cy - 46 * scale, cx + 22 * scale, cy - 30 * scale],
               fill=GLYPH_COLOR)  # head
    d.line([cx + 10 * scale, cy - 28 * scale, cx + 10 * scale, cy - 4 * scale], fill=GLYPH_COLOR,
           width=int(STROKE * 0.6 * scale))  # torso
    d.line([cx + 10 * scale, cy - 10 * scale, cx - 18 * scale, cy - 10 * scale], fill=GLYPH_COLOR,
           width=int(STROKE * 0.6 * scale))  # arm to pushrim
    d.line([cx + 10 * scale, cy - 4 * scale, cx - 4 * scale, cy + 12 * scale], fill=GLYPH_COLOR,
           width=int(STROKE * 0.6 * scale))  # leg


def glyph_accessibility(d):
    _wheelchair(d, CENTER - 6, CENTER - 4, scale=1.15)


def glyph_venue(d):
    _wheelchair(d, CENTER - 6, CENTER - 4, scale=1.15)


def glyph_pathway(d):
    # two curved footprint dots suggesting a walked path
    for i, (dx, dy) in enumerate([(-40, 30), (-5, -5), (30, -35)]):
        r = 16
        d.ellipse([CENTER + dx - r, CENTER + dy - r, CENTER + dx + r, CENTER + dy + r],
                  fill=GLYPH_COLOR)


def glyph_parking(d):
    d.rectangle([CENTER - 45, CENTER - 55, CENTER + 45, CENTER + 55],
                outline=GLYPH_COLOR, width=STROKE - 2)
    # Bold "P" via simple strokes
    d.line([CENTER - 15, CENTER - 35, CENTER - 15, CENTER + 35], fill=GLYPH_COLOR, width=STROKE)
    d.line([CENTER - 15, CENTER - 35, CENTER + 10, CENTER - 35], fill=GLYPH_COLOR, width=STROKE)
    d.arc([CENTER - 15, CENTER - 35, CENTER + 25, CENTER + 5], start=-90, end=90,
          fill=GLYPH_COLOR, width=STROKE)


def glyph_elevators(d):
    d.rectangle([CENTER - 40, CENTER - 55, CENTER + 40, CENTER + 55],
                outline=GLYPH_COLOR, width=STROKE - 4)
    # up triangle
    d.polygon([(CENTER - 18, CENTER - 5), (CENTER + 18, CENTER - 5), (CENTER, CENTER - 35)],
              fill=GLYPH_COLOR)
    # down triangle
    d.polygon([(CENTER - 18, CENTER + 15), (CENTER + 18, CENTER + 15), (CENTER, CENTER + 45)],
              fill=GLYPH_COLOR)


def glyph_doors(d):
    d.rectangle([CENTER - 35, CENTER - 55, CENTER + 35, CENTER + 55],
                outline=GLYPH_COLOR, width=STROKE)
    d.ellipse([CENTER + 15, CENTER - 8, CENTER + 25, CENTER + 2], fill=GLYPH_COLOR)  # handle


GLYPHS = {
    "toilets": glyph_toilets,
    "ramps": glyph_ramps,
    "accessibility": glyph_accessibility,
    "pathway": glyph_pathway,
    "parking": glyph_parking,
    "elevators": glyph_elevators,
    "doors": glyph_doors,
    "venue": glyph_venue,
}


def main():
    for cat_name, glyph_fn in GLYPHS.items():
        for rating, color in RATING_COLORS.items():
            img = circle_bg(color)
            d = ImageDraw.Draw(img)
            glyph_fn(d)
            out_path = OUT / f"{cat_name}-{rating}.png"
            img.save(out_path)
            print(f"wrote {out_path.relative_to(OUT.parent.parent)}")


if __name__ == "__main__":
    main()
