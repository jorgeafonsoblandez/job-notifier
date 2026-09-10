"""
Tracks which job listings have already been notified about, so the same
job isn't sent again on the next run. Stored as a plain JSON file that the
GitHub Actions workflow commits back to the repo after each run.
"""

import json
import os

STATE_FILE = "seen_jobs.json"


def load_seen() -> dict:
    """Returns {"it": [ids...], "temp": [ids...]}"""
    if not os.path.exists(STATE_FILE):
        return {"it": [], "temp": []}
    with open(STATE_FILE, encoding="utf-8") as f:
        return json.load(f)


def save_seen(state: dict):
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2)
