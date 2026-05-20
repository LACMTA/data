"""
Applies WC-specific transformations to the unzipped current events GTFS routes.

Transformations applied to gtfs-unzipped/current/gtfs_events/routes.txt:
  - Clears route_short_name (leaves only route_long_name populated)
  - Sets route_color to 5949a7
  - Sets route_text_color to 000000

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
ROUTE_TEXT_COLOR = "000000"

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

df.to_csv(ROUTES_FILE, index=False)
print(f"[wc-events] Updated {ROUTES_FILE.relative_to(PROJECT_ROOT)}")

print("Done.")
