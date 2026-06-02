"""
Applies WC-specific transformations to the unzipped current events GTFS routes.

Transformations applied to gtfs-unzipped/current/gtfs_events/routes.txt:
  - Clears route_short_name (leaves only route_long_name populated)
  - Sets route_color to 5949a7
  - Sets route_text_color to 000000
  - Prepends a two-letter prefix to route_long_name based on route_id

Usage: python scripts/process_wc_events_gtfs.py
"""

from pathlib import Path

import pandas as pd

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

PROJECT_ROOT = Path(__file__).parent.parent

ROUTES_FILE = PROJECT_ROOT / "gtfs-unzipped" / "current" / "gtfs_events" / "routes.txt"

ROUTE_COLOR = "5949a7"
ROUTE_TEXT_COLOR = "ffffff"

# Maps route_id -> two-letter prefix to prepend to route_long_name
ROUTE_PREFIX = {
    "1":  "R1",
    "2":  "R2",
    "3":  "R3",
    "4":  "R4",
    "5":  "R5",
    "6":  "R6",
    "7":  "R7",
    "8":  "S8",
    "9":  "S9",
    "10": "S10",
    "11": "S11",
    "12": "S12",
    "13": "T13",
    "14": "T14",
    "15": "T15",
}

# ---------------------------------------------------------------------------
# Transform
# ---------------------------------------------------------------------------

if not ROUTES_FILE.exists():
    raise FileNotFoundError(
        f"{ROUTES_FILE.relative_to(PROJECT_ROOT)} not found. "
        "Run `uv run poe unzip` first."
    )

print(f"[wc-events] Reading {ROUTES_FILE.relative_to(PROJECT_ROOT)}")
df = pd.read_csv(ROUTES_FILE, dtype=str, keep_default_na=False)

df["route_short_name"] = ""
df["route_color"] = ROUTE_COLOR
df["route_text_color"] = ROUTE_TEXT_COLOR

unknown_ids = set(df["route_id"]) - set(ROUTE_PREFIX)
if unknown_ids:
    print(
        f"[wc-events] WARNING: route_id(s) not found in ROUTE_PREFIX lookup "
        f"— route_long_name left unchanged: {sorted(unknown_ids)}"
    )

df["route_long_name"] = (
    df["route_id"].map(ROUTE_PREFIX).fillna("") + " " + df["route_long_name"]
).str.strip()

df.to_csv(ROUTES_FILE, index=False)
print(f"[wc-events] Updated {ROUTES_FILE.relative_to(PROJECT_ROOT)}")

print("Done.")
