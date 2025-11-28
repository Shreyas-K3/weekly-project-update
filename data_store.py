import json
import os

FILE_PATH = "project_status.json"

DEFAULT_DATA = {
    "project_name": "Project Atlas Copco",
    "project_code": "ATLAS2025",  # default, can be changed from server

    # Pre-approved names who can log into the client dashboard
    "allowed_names": [
        "Shreyas",
        "Client User 1",
        "Client User 2"
    ],
}


def load_data():
    """Load project data from JSON; fall back to defaults."""
    if os.path.exists(FILE_PATH):
        try:
            with open(FILE_PATH, "r", encoding="utf-8") as f:
                stored = json.load(f)
        except Exception:
            # If file is corrupted / unreadable, just use defaults
            return DEFAULT_DATA.copy()

        # Merge defaults with stored so new keys don't break
        data = DEFAULT_DATA.copy()
        data.update(stored)
        return data

    # No file -> return defaults
    return DEFAULT_DATA.copy()


def save_data(data: dict):
    """Save project data to JSON."""
    with open(FILE_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
