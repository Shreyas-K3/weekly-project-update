import json
import os

FILE_PATH = "project_status.json"

# ADDED: Missing keys that client.py expects
DEFAULT_DATA = {
    "project_name": "Project Atlas Copco",
    "project_code": "ATLAS2025",
    "allowed_names": [
        "Shreyas",
        "Client User 1",
        "Client User 2"
    ],
    # --- Metrics required by Client Dashboard ---
    "project_completion": 45,
    "project_status_label": "On Track",
    "pending_rfis": 3,
    "rfis_label": "Needs Attention",
    "timeline_days": 4,
    
    # --- Links ---
    "viewer_link": "https://streamlit.io", # Replace with actual link
    "rfi_sheet_link": "https://google.com", # Replace with actual link
    
    # --- Progress Bars ---
    "phe_progress": 100,
    "elec_progress": 90,
    "ff_progress": 45,
    "mech_progress": 30,
    
    # --- Timeline Text ---
    "days_1_2": "Modeling of First Floor",
    "days_1_2_sub": "Focus on HVAC and Cable Trays",
    "days_3_4": "Clash Detection Review",
    "days_3_4_sub": "Coordination with structural team",
    
    # --- Content ---
    "notes_markdown": "Please review the RFI sheet by Friday.",
    "email_body": "This is the full text of the weekly update email..."
}


def load_data():
    """Load project data from JSON; fall back to defaults."""
    if os.path.exists(FILE_PATH):
        try:
            with open(FILE_PATH, "r", encoding="utf-8") as f:
                stored = json.load(f)
        except Exception:
            return DEFAULT_DATA.copy()

        # Merge defaults with stored so new keys don't break
        # This ensures if you add new keys to DEFAULT_DATA, 
        # old JSON files won't crash the app.
        data = DEFAULT_DATA.copy()
        data.update(stored)
        return data

    return DEFAULT_DATA.copy()


def save_data(data: dict):
    """Save project data to JSON."""
    with open(FILE_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
