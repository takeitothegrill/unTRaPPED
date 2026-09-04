#!/usr/bin/env python3
"""unTRaPPED V2 — local photo pipeline.

Reads locations.csv (the master, human-edited list of locations). For each
row whose location_id has a matching folder under incoming/, this script:

  1. Finds the hero photo (earliest capture time; first-imported photo of
     the batch determines the pin's position).
  2. Fills in latitude/longitude from the hero photo's EXIF GPS, unless the
     human already pre-filled them (a manual override for indoor shots or
     bad auto-GPS — see STATUS.md for why this exists).
  3. Converts every photo (HEIC or otherwise) to JPEG, preserving EXIF.
  4. Burns in a visible watermark + capture-date stamp (anti-theft, and a
     human-readable date on the image itself).
  5. Writes the processed photos to processed/<location_id>/, ready to be
     uploaded to Google Photos/Drive by a later (not-yet-built) step.
  6. Writes locations.csv back with any backfilled lat/lon.

This script does NOT talk to Google Maps or Drive, and does NOT touch the
`status` / `synced_photos` columns — those belong to the browser-automation
step that actually pushes to My Maps, which is separate, later work. This
script is safe to re-run any time; it only ever fills blank lat/lon cells
and regenerates processed output, it never overwrites human-entered text.

Usage:
    python process_locations.py
"""
import csv
import io
import os
import shutil
import sys
from datetime import datetime
from pathlib import Path

from PIL import Image, ExifTags
import pillow_heif

pillow_heif.register_heif_opener()

from categories import normalize_category, normalize_rating

ROOT = Path(__file__).resolve().parent.parent  # .../untrapped v2
LOCATIONS_CSV = ROOT / "locations.csv"
INCOMING_DIR = ROOT / "incoming"
PROCESSED_DIR = ROOT / "processed"

RASTER_EXTS = {".jpg", ".jpeg", ".png", ".heic", ".heif", ".tif", ".tiff", ".bmp"}
VIDEO_EXTS = {".mov", ".mp4", ".m4v", ".avi"}

WATERMARK_TEXT = "unTRaPPED.au"
FONT_PATH = r"C:\Windows\Fonts\arial.ttf"
FONT_PATH_BOLD = r"C:\Windows\Fonts\arialbd.ttf"

CSV_FIELDS = [
    "location_id", "name", "description", "category", "rating",
    "latitude", "longitude", "status", "synced_photos",
]


def load_locations():
    if not LOCATIONS_CSV.exists():
        print(f"ERROR: {LOCATIONS_CSV} not found.")
        sys.exit(1)
    with open(LOCATIONS_CSV, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        fieldnames = reader.fieldnames or CSV_FIELDS
    return rows, fieldnames


def save_locations(rows, fieldnames):
    with open(LOCATIONS_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def list_photo_files(folder: Path):
    photos, videos = [], []
    for p in sorted(folder.iterdir()):
        if not p.is_file():
            continue
        ext = p.suffix.lower()
        if ext in RASTER_EXTS:
            photos.append(p)
        elif ext in VIDEO_EXTS:
            videos.append(p)
    return photos, videos


def _rational_to_float(v):
    try:
        return float(v)
    except Exception:
        try:
            return v[0] / v[1]
        except Exception:
            return None


def read_exif(path: Path):
    """Return (capture_datetime_or_None, lat_or_None, lon_or_None)."""
    try:
        img = Image.open(path)
        exif = img.getexif()
        base = {ExifTags.TAGS.get(k, k): v for k, v in exif.items()}
        try:
            ex = exif.get_ifd(ExifTags.IFD.Exif)
            for k, v in ex.items():
                base[ExifTags.TAGS.get(k, k)] = v
        except Exception:
            pass
        dt = None
        for tag in ("DateTimeOriginal", "DateTimeDigitized", "DateTime"):
            if base.get(tag):
                try:
                    dt = datetime.strptime(str(base[tag]), "%Y:%m:%d %H:%M:%S")
                except Exception:
                    pass
                break
        lat = lon = None
        try:
            gi = exif.get_ifd(ExifTags.IFD.GPSInfo)
            gps = {ExifTags.GPSTAGS.get(k, k): v for k, v in gi.items()}
            glat, glon = gps.get("GPSLatitude"), gps.get("GPSLongitude")
            if glat and glon:
                d, m, s = (_rational_to_float(x) for x in glat)
                lat = d + m / 60 + s / 3600
                if str(gps.get("GPSLatitudeRef", "N")).upper().startswith("S"):
                    lat = -lat
                d, m, s = (_rational_to_float(x) for x in glon)
                lon = d + m / 60 + s / 3600
                if str(gps.get("GPSLongitudeRef", "E")).upper().startswith("W"):
                    lon = -lon
        except Exception:
            pass
        return dt, (round(lat, 6) if lat is not None else None), (round(lon, 6) if lon is not None else None)
    except Exception as e:
        print(f"    WARNING: could not read EXIF from {path.name}: {e}")
        return None, None, None


def pick_hero(photos):
    """Hero = earliest capture time; falls back to filename order if no dates."""
    dated = []
    for p in photos:
        dt, lat, lon = read_exif(p)
        dated.append((dt, p, lat, lon))
    with_date = [d for d in dated if d[0] is not None]
    if with_date:
        with_date.sort(key=lambda d: d[0])
        return with_date[0][1], with_date[0][2], with_date[0][3]
    # no EXIF dates anywhere: fall back to first file alphabetically
    p = photos[0]
    _, lat, lon = read_exif(p)
    return p, lat, lon


def load_font(size, bold=False):
    path = FONT_PATH_BOLD if bold else FONT_PATH
    try:
        from PIL import ImageFont
        return ImageFont.truetype(path, size)
    except Exception:
        from PIL import ImageFont
        return ImageFont.load_default()


def watermark_and_save(src: Path, dst: Path, capture_dt):
    from PIL import ImageDraw, ImageOps

    img = Image.open(src)
    # Bake EXIF orientation into the actual pixels (many viewers, including
    # web <img> tags, ignore the Orientation tag and show raw pixels) and
    # reset the tag so we don't get double-rotated on save. GPS/other EXIF
    # fields are untouched.
    img = ImageOps.exif_transpose(img)
    exif_bytes = img.info.get("exif")
    img = img.convert("RGB")

    overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)

    font_size = max(14, round(img.height * 0.028))
    font = load_font(font_size, bold=True)
    date_font = load_font(max(12, round(font_size * 0.75)))

    margin = round(img.height * 0.02)
    brand_text = WATERMARK_TEXT
    date_text = capture_dt.strftime("%d %b %Y") if capture_dt else ""

    def draw_with_shadow(xy, text, f):
        x, y = xy
        draw.text((x + 1, y + 1), text, font=f, fill=(0, 0, 0, 140))
        draw.text((x, y), text, font=f, fill=(255, 255, 255, 200))

    brand_bbox = draw.textbbox((0, 0), brand_text, font=font)
    bw, bh = brand_bbox[2] - brand_bbox[0], brand_bbox[3] - brand_bbox[1]
    draw_with_shadow((img.width - bw - margin, img.height - bh - margin - 2), brand_text, font)

    if date_text:
        date_bbox = draw.textbbox((0, 0), date_text, font=date_font)
        dh = date_bbox[3] - date_bbox[1]
        draw_with_shadow((margin, img.height - dh - margin - 2), date_text, date_font)

    watermarked = Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")
    dst.parent.mkdir(parents=True, exist_ok=True)
    save_kwargs = {"quality": 88}
    if exif_bytes:
        save_kwargs["exif"] = exif_bytes
    watermarked.save(dst, "JPEG", **save_kwargs)


def process_location(row):
    loc_id = row["location_id"].strip()
    folder = INCOMING_DIR / loc_id
    if not folder.is_dir():
        return None  # nothing to do — no incoming folder for this row

    print(f"\n[{loc_id}] {row.get('name', '')}")

    cat_id, cat_name = normalize_category(row.get("category"))
    if cat_id is None:
        print(f"    WARNING: category '{row.get('category')}' not recognized (won't block processing)")
    rating = normalize_rating(row.get("rating"))
    if rating is None:
        print(f"    WARNING: rating '{row.get('rating')}' not recognized (won't block processing)")

    photos, videos = list_photo_files(folder)
    if videos:
        print(f"    NOTE: skipping {len(videos)} video file(s) — not usable for map pins")
    if not photos:
        print(f"    WARNING: no photo files found in {folder} — skipping")
        return row

    lat_str, lon_str = row.get("latitude", "").strip(), row.get("longitude", "").strip()
    has_override = bool(lat_str and lon_str)

    hero, hero_lat, hero_lon = pick_hero(photos)
    print(f"    hero photo: {hero.name}")

    if has_override:
        lat, lon = lat_str, lon_str
        print(f"    using human-provided override position: {lat}, {lon}")
    elif hero_lat is not None and hero_lon is not None:
        lat, lon = hero_lat, hero_lon
        row["latitude"], row["longitude"] = str(lat), str(lon)
        print(f"    position from hero photo EXIF: {lat}, {lon}")
    else:
        print(f"    NEEDS POSITION: hero photo has no GPS and no override is set in locations.csv.")
        print(f"    Fill latitude/longitude for '{loc_id}' manually, or retake with GPS enabled. Skipping.")
        return row

    out_folder = PROCESSED_DIR / loc_id
    for photo in photos:
        dt, _, _ = read_exif(photo)
        dst = out_folder / (photo.stem + ".jpg")
        try:
            watermark_and_save(photo, dst, dt)
            print(f"    processed: {photo.name} -> {dst.relative_to(ROOT)}")
        except Exception as e:
            print(f"    ERROR processing {photo.name}: {e}")

    return row


def main():
    INCOMING_DIR.mkdir(exist_ok=True)
    PROCESSED_DIR.mkdir(exist_ok=True)

    rows, fieldnames = load_locations()
    if not rows:
        print(f"{LOCATIONS_CSV} has no rows yet. Add a row per location and re-run.")
        return

    updated = []
    needs_position, processed_ok = [], []
    for row in rows:
        result = process_location(row)
        if result is None:
            updated.append(row)  # no incoming folder — leave untouched
            continue
        updated.append(result)
        if not result.get("latitude") and not row.get("latitude"):
            needs_position.append(result["location_id"])
        else:
            processed_ok.append(result["location_id"])

    save_locations(updated, fieldnames)

    print("\n" + "=" * 60)
    print(f"Processed OK: {len(processed_ok)}  {processed_ok}")
    if needs_position:
        print(f"NEEDS POSITION (skipped): {len(needs_position)}  {needs_position}")
    print(f"locations.csv updated: {LOCATIONS_CSV}")
    print("=" * 60)


if __name__ == "__main__":
    main()
