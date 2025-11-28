import json
import os

FILE_PATH = "project_status.json"

DEFAULT_DATA = {
    "project_name": "Project Atlas Copco",
    "project_code": "ATLAS2025",

    "project_completion": 83,      # %
    "project_status_label": "On Track",

    "pending_rfis": 6,
    "rfis_label": "Non-Critical",

    "timeline_days": 4,

    "viewer_link": "https://autode.sk/4rgD3cG",
    "rfi_sheet_link": "https://docs.google.com/spreadsheets/d/1RDRCvOWoVXIMcnYJCmDs8JvboJvep7j-/edit?usp=drive_link&ouid=101341274280914933041&rtpof=true&sd=true",

    "phe_progress": 100,  # %
    "elec_progress": 100, # %
    "ff_progress": 80,    # %
    "mech_progress": 80,  # %

    "notes_markdown": """**Action Required:**
- ⏰ **6 non-critical RFIs** are awaiting responses
- 🔍 Please review the model viewer and provide feedback
- ✍️ Update the RFI sheet to maintain project momentum
""",

    "days_1_2": "Complete FF and MECH models",
    "days_1_2_sub": "Target: 100% completion of remaining models",

    "days_3_4": "Initiate coordination phase",
    "days_3_4_sub": "Begin cross-discipline integration",

    "email_body": """**Team,**

Below is this week's status update for **Project Atlas Copco**.  
Progress remains steady and we are tracking toward the upcoming milestone.

All metrics and links are provided above in the dashboard format for easy access and tracking."""
}


def load_data():
    """Load project data from JSON; fall back to defaults."""
    if os.path.exists(FILE_PATH):
        try:
            with open(FILE_PATH, "r", encoding="utf-8") as f:
                stored = json.load(f)
        except Exception:
            # If corrupted, just use defaults
            return DEFAULT_DATA.copy()

        # Merge with defaults so new keys don't break older files
        data = DEFAULT_DATA.copy()
        data.update(stored)
        return data

    # No file yet → use defaults
    return DEFAULT_DATA.copy()


def save_data(data: dict):
    """Save project data to JSON."""
    with open(FILE_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
