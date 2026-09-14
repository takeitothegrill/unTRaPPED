#!/usr/bin/env python3
"""Prepare a local, human-uploadable unTRAPPED photo batch.

This tool deliberately performs no Drive, My Maps, or CSV write operations.
"""

from __future__ import annotations

import csv
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
from datetime import date
from pathlib import Path

from PIL import Image, ImageEnhance, ImageOps


ROOT = Path(__file__).resolve().parents[1]
CSV_PATH = ROOT / "locations-from-v1-map.csv"
INCOMING = ROOT / "incoming"
CONFIG_PATH = ROOT / "config" / "watermark-settings.json"
ICON_MAP_PATH = ROOT / "config" / "icon-map.csv"
ICON_DIRECTORY = ROOT / "icons" / "final"
SUPPORTED = {".jpg", ".jpeg", ".png", ".heic", ".heif"}
PLACEMENTS = {"top-left", "top-right", "bottom-left", "bottom-right"}


class PreparationError(Exception):
    """A clear, location-specific preparation failure."""


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def read_settings() -> tuple[dict, Path]:
    try:
        settings = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise PreparationError(f"Watermark settings cannot be read: {error}") from error

    required = {
        "schema_version", "logo_path", "placement", "margin_pixels", "width_ratio",
        "opacity", "correct_orientation_before_watermark", "preserve_aspect_ratio",
        "date_stamp_enabled",
    }
    missing = sorted(required - settings.keys())
    if missing:
        raise PreparationError("Watermark settings are missing: " + ", ".join(missing))
    if settings["placement"] not in PLACEMENTS:
        raise PreparationError("Watermark placement is unsupported.")
    if not isinstance(settings["margin_pixels"], int) or settings["margin_pixels"] < 0:
        raise PreparationError("Watermark margin_pixels must be zero or greater.")
    for field in ("width_ratio", "opacity"):
        value = settings[field]
        if not isinstance(value, (int, float)) or isinstance(value, bool) or not 0 < value <= 1:
            raise PreparationError(f"Watermark {field} must be greater than zero and no more than one.")
    logo = (CONFIG_PATH.parent / settings["logo_path"]).resolve()
    if not logo.is_file():
        raise PreparationError("Approved watermark logo is missing.")
    return settings, logo


def read_icon_map() -> dict[tuple[str, str], str]:
    with ICON_MAP_PATH.open(newline="", encoding="utf-8-sig") as stream:
        rows = csv.DictReader(stream)
        required = {"category", "rating", "icon_filename"}
        if not rows.fieldnames or not required.issubset(rows.fieldnames):
            raise PreparationError("Icon map has an invalid header.")
        mapping = {(row["category"].strip(), row["rating"].strip()): row["icon_filename"].strip()
                   for row in rows}
    return mapping


def synced_names(value: str | None) -> set[str]:
    if not value:
        return set()
    return {name.strip().casefold() for name in value.replace(";", ",").replace("\n", ",").split(",") if name.strip()}


def derivative_name(source: Path) -> str:
    return f"{source.stem}.jpg" if source.suffix.casefold() in {".heic", ".heif"} else source.name


def batch_directory() -> Path:
    base = ROOT / "batches" / f"{date.today().isoformat()}-upload-batch"
    candidate, suffix = base, 2
    while candidate.exists():
        candidate = ROOT / "batches" / f"{base.name}-{suffix}"
        suffix += 1
    return candidate


def open_source_image(source: Path) -> Image.Image:
    if source.suffix.casefold() not in {".heic", ".heif"}:
        with Image.open(source) as image:
            return image.copy()
    ffmpeg = shutil.which("ffmpeg")
    if not ffmpeg:
        raise PreparationError("HEIC photo needs ffmpeg, which is not available on this computer.")
    with tempfile.TemporaryDirectory(prefix="untrapped-heic-") as temporary:
        converted = Path(temporary) / "converted.jpg"
        completed = subprocess.run(
            [ffmpeg, "-v", "error", "-y", "-i", str(source), "-frames:v", "1", str(converted)],
            capture_output=True,
            text=True,
            check=False,
        )
        if completed.returncode or not converted.is_file():
            detail = completed.stderr.strip() or "the file could not be decoded"
            raise PreparationError(f"HEIC conversion failed: {detail}")
        with Image.open(converted) as image:
            return image.copy()


def watermark(source: Path, destination: Path, settings: dict, logo_path: Path) -> dict:
    image = open_source_image(source)
    if settings["correct_orientation_before_watermark"]:
        image = ImageOps.exif_transpose(image)
    image = image.convert("RGBA")
    with Image.open(logo_path) as logo_image:
        logo = logo_image.convert("RGBA")
    width = max(1, round(image.width * settings["width_ratio"]))
    height = max(1, round(logo.height * width / logo.width))
    logo = logo.resize((width, height), Image.Resampling.LANCZOS)
    alpha = logo.getchannel("A")
    alpha = ImageEnhance.Brightness(alpha).enhance(settings["opacity"])
    logo.putalpha(alpha)
    margin = settings["margin_pixels"]
    positions = {
        "top-left": (margin, margin),
        "top-right": (image.width - width - margin, margin),
        "bottom-left": (margin, image.height - height - margin),
        "bottom-right": (image.width - width - margin, image.height - height - margin),
    }
    x, y = positions[settings["placement"]]
    if x < 0 or y < 0:
        raise PreparationError("Watermark is larger than the photo after applying the configured margin.")
    image.alpha_composite(logo, (x, y))
    destination.parent.mkdir(parents=True, exist_ok=True)
    if destination.suffix.casefold() in {".jpg", ".jpeg"}:
        image.convert("RGB").save(destination, quality=95, optimize=True)
    else:
        image.save(destination)
    return {
        "source_dimensions": [image.width, image.height],
        "watermark_dimensions": [width, height],
        "watermark_position_xy": [x, y],
    }


def main() -> int:
    try:
        settings, logo_path = read_settings()
        icon_map = read_icon_map()
    except PreparationError as error:
        print(f"Cannot start: {error}")
        return 2

    with CSV_PATH.open(newline="", encoding="utf-8-sig") as stream:
        rows = list(csv.DictReader(stream))
    required_columns = {"location_id", "name", "status", "category", "rating", "synced_photos"}
    if not rows or not required_columns.issubset(rows[0]):
        print("Cannot start: locations-from-v1-map.csv has an invalid header.")
        return 2

    selected = [row for row in rows if row.get("status", "").strip() in {"ready", "update"}]
    ids = [row["location_id"].strip() for row in selected]
    duplicates = {item for item in ids if item and ids.count(item) > 1}
    batch = batch_directory()
    upload_root = batch / "upload"
    results: list[dict] = []

    for row in selected:
        location_id = row["location_id"].strip()
        entry = {
            "location_id": location_id,
            "original_status": row["status"].strip(),
            "name": row["name"].strip(),
            "approved_icon_filename": None,
            "source_folder": f"incoming/{location_id}",
            "prepared_photos": [],
            "advisories": [],
            "blockers": [],
            "outcome": "BLOCKED",
        }
        results.append(entry)
        if not location_id:
            entry["blockers"].append("location_id is missing.")
            continue
        if location_id in duplicates:
            entry["blockers"].append("location_id is duplicated among actionable rows.")
            continue
        if not entry["name"]:
            entry["blockers"].append("Location name is missing.")
            continue
        icon = icon_map.get((row["category"].strip(), row["rating"].strip()))
        if not icon or not (ICON_DIRECTORY / icon).is_file():
            entry["blockers"].append("Approved icon cannot be resolved from config/icon-map.csv.")
            continue
        entry["approved_icon_filename"] = icon
        folder = INCOMING / location_id
        if not folder.is_dir():
            entry["blockers"].append("Matching incoming photo folder is missing.")
            continue
        sources = sorted((item for item in folder.iterdir() if item.is_file() and item.suffix.casefold() in SUPPORTED), key=lambda item: item.name.casefold())
        ignored = sorted(item.name for item in folder.iterdir() if item.is_file() and item.suffix.casefold() not in SUPPORTED)
        if ignored:
            entry["advisories"].append("Ignored unsupported files: " + ", ".join(ignored))
        if not sources:
            entry["advisories"].append("No supported photos were supplied.")
            entry["outcome"] = "READY_WITH_NO_NEW_PHOTOS"
            continue
        names = [derivative_name(source).casefold() for source in sources]
        if len(names) != len(set(names)):
            entry["blockers"].append("Two source photos would produce the same upload filename.")
            continue
        existing = synced_names(row.get("synced_photos")) if entry["original_status"] == "update" else set()
        new_sources = [source for source in sources if derivative_name(source).casefold() not in existing]
        if not new_sources:
            entry["outcome"] = "READY_WITH_NO_NEW_PHOTOS"
            entry["advisories"].append("All supported photos are already listed in synced_photos.")
            continue
        try:
            for source in new_sources:
                output_name = derivative_name(source)
                destination = upload_root / location_id / output_name
                details = watermark(source, destination, settings, logo_path)
                entry["prepared_photos"].append({
                    "source_filename": source.name,
                    "source_sha256": sha256(source),
                    "upload_filename": output_name,
                    "upload_relative_path": str(destination.relative_to(batch)).replace("\\", "/"),
                    "upload_sha256": sha256(destination),
                    **details,
                })
            entry["outcome"] = "PREPARED"
        except (OSError, PreparationError) as error:
            location_upload_folder = upload_root / location_id
            if location_upload_folder.exists():
                shutil.rmtree(location_upload_folder)
            entry["prepared_photos"] = []
            entry["blockers"].append(str(error))
            entry["outcome"] = "BLOCKED"

    manifest = {
        "schema_version": 1,
        "batch_id": batch.name,
        "purpose": "Local preparation only; manual Google Drive upload is required.",
        "authoritative_csv": "locations-from-v1-map.csv",
        "csv_sha256": sha256(CSV_PATH),
        "watermark_settings_path": "config/watermark-settings.json",
        "watermark_settings_sha256": sha256(CONFIG_PATH),
        "watermark_settings": settings,
        "approved_logo_path": str(logo_path.relative_to(ROOT)).replace("\\", "/"),
        "approved_logo_sha256": sha256(logo_path),
        "csv_modified": False,
        "external_uploads_performed": False,
        "locations": results,
    }
    batch.mkdir(parents=True, exist_ok=True)
    (batch / "batch-manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    prepared = sum(len(entry["prepared_photos"]) for entry in results)
    blocked = [entry for entry in results if entry["blockers"]]
    lines = [
        "unTRAPPED local upload preparation",
        f"Batch: {batch.name}",
        f"Actionable locations checked: {len(selected)}",
        f"New watermarked photos prepared: {prepared}",
        "CSV and external systems were not changed.",
        "",
    ]
    if prepared:
        lines += [f"Upload this folder manually to Google Drive: {upload_root}", ""]
    if not selected:
        lines += ["Nothing to prepare: no CSV rows currently have status ready or update.", ""]
    for entry in results:
        lines.append(f"{entry['location_id']}: {entry['outcome']}")
        lines += [f"  Prepared: {photo['upload_filename']}" for photo in entry["prepared_photos"]]
        lines += [f"  Attention: {message}" for message in entry["advisories"] + entry["blockers"]]
    (batch / "RESULTS.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))
    print(f"\nManifest: {batch / 'batch-manifest.json'}")
    return 1 if blocked else 0


if __name__ == "__main__":
    sys.exit(main())
