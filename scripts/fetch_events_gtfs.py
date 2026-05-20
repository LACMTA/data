"""
Downloads the events GTFS zip file from the URL defined in .env.

Saves the file to gtfs/current/gtfs_events.zip, overwriting any existing file.

Usage: python scripts/fetch_events_gtfs.py

Requires EVENTS_GTFS_URL to be set in .env.
"""

import os
import urllib.request
from pathlib import Path

from dotenv import load_dotenv

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

PROJECT_ROOT = Path(__file__).parent.parent

load_dotenv(PROJECT_ROOT / ".env")

EVENTS_GTFS_URL = os.getenv("EVENTS_GTFS_URL")
if not EVENTS_GTFS_URL:
    raise OSError("EVENTS_GTFS_URL is not set in .env")

# ---------------------------------------------------------------------------
# Download
# ---------------------------------------------------------------------------

CURRENT_DIR = PROJECT_ROOT / "gtfs" / "current"
CURRENT_DIR.mkdir(parents=True, exist_ok=True)

dest = CURRENT_DIR / "gtfs_events.zip"
print(f"[events] Downloading {EVENTS_GTFS_URL} ...")
urllib.request.urlretrieve(EVENTS_GTFS_URL, dest)
print(f"[events] Saved to {dest.relative_to(PROJECT_ROOT)}")

print("Done.")
