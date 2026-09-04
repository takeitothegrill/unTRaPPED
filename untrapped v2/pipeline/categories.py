"""Shared category/rating vocabulary for the unTRaPPED V2 pipeline.

Category numbers match the original TRAPPED acronym ordering used across
this project's canon docs and My Maps testing. Kept as a small, editable
table on purpose: adding or renaming a category is a one-line change here,
not a schema migration (My Maps' "Categories" style mode picks up new
values automatically the first time they appear in an uploaded batch).
"""

CATEGORIES = {
    1: "Toilets",
    2: "Ramps",
    3: "Accessibility",
    4: "Pathway",
    5: "Parking",
    6: "Elevators",
    7: "Doors",
}
CATEGORY_NAME_TO_ID = {name.lower(): num for num, name in CATEGORIES.items()}

RATINGS = ["green", "orange", "red"]


def normalize_category(raw):
    """Return (category_id, canonical_name) or (None, None) if unrecognized."""
    key = (raw or "").strip().lower()
    num = CATEGORY_NAME_TO_ID.get(key)
    if num is None:
        return None, None
    return num, CATEGORIES[num]


def normalize_rating(raw):
    """Return canonical lowercase rating or None if unrecognized."""
    key = (raw or "").strip().lower()
    return key if key in RATINGS else None
