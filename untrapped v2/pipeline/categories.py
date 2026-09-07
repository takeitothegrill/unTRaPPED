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
    # Not part of the TRAPPED acronym — for whole destinations that don't
    # map to a specific feature type (a playground, a park, a venue as a
    # place). Rated green/orange/red like the others but styled with a
    # plain wheelchair symbol rather than a feature-specific glyph.
    8: "Venue",
    # Amenities share the Venue icon and the Venue map layer on purpose.
    # A park with markets on is an amenity on Monday and a venue on Sunday --
    # if the surveyor cannot reliably tell them apart, a user cannot either,
    # so the map does not split them. The distinction lives in the data (and in
    # the venue TYPE inside the pin name: playground, beach, cafe, plaza...).
    9: "Amenities",
}
CATEGORY_NAME_TO_ID = {name.lower(): num for num, name in CATEGORIES.items()}

RATINGS = ["green", "orange", "red"]


# --- map legend ------------------------------------------------------------
# The map shows FOUR icon families, not the eight assessment categories. The
# TRAPPED categories are how a place is assessed; the legend is what a user has
# to decode at a glance, and it is deliberately smaller. See
# icons/DESIGNER_BRIEF.md section 1.
#
# Everything about getting there and getting through - ramps, pathways,
# elevators, doors - collapses into "route".
MAP_ICON = {
    1: "toilet",    # Toilets
    2: "route",     # Ramps
    3: "venue",     # Accessibility  (TRAPPED's "A - accessible interior")
    4: "route",     # Pathway
    5: "parking",   # Parking
    6: "route",     # Elevators
    7: "route",     # Doors
    8: "venue",     # Venue
    9: "venue",     # Amenities -- same icon, same layer, see CATEGORIES
}

ICON_FAMILIES = ("parking", "toilet", "route", "venue")


def icon_key(raw_category, raw_rating):
    """Return the style key for a row, e.g. "parking-green", or None.

    My Maps can only style a layer by ONE column, but an icon is chosen by
    category AND rating together. So the merge CSV carries this single
    pre-combined column and the layer is styled by it -- 12 values, 12 icons.
    Doing the join here rather than in the browser keeps the mapping in one
    place and out of the hands of whoever is driving the map that day.
    """
    cat_id, _ = normalize_category(raw_category)
    rating = normalize_rating(raw_rating)
    if cat_id is None or rating is None:
        return None
    return f"{MAP_ICON[cat_id]}-{rating}"


def all_icon_keys():
    """The 12 style values, matching the 12 files in icons/final/."""
    return [f"{fam}-{r}" for fam in ICON_FAMILIES for r in RATINGS]


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
