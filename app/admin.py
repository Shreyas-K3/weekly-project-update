import streamlit as st
import pandas as pd
import time
from app.db import upsert_project, get_project_by_code, list_project_codes, list_comments
from app.utils import load_css

def app():
    load_css("app/style.css")
    st.title("Admin Panel 🛠️")
    st.markdown("---")

    # --- Select Project ---
    existing_codes = list_project_codes()
    
    st.subheader("Manage Projects")
    mode = st.radio("Action", ["Edit Existing Project", "Create New Project"], horizontal=True)
    
    selected_code = None
    project_data = {}

    if mode == "Edit Existing Project":
        if not existing_codes:
            st.warning("No projects found. Please create one.")
            mode = "Create New Project"
        else:
            # Use the existing code list to select
            selected_code = st.selectbox("Select Project Code to Edit", existing_codes)
            if selected_code:
                # Load existing data
                p_obj = get_project_by_code(selected_code)
                if p_obj:
                    project_data = p_obj.__dict__
    
    # --- Project Form ---
    with st.form("project_form"):
        st.subheader(f"Project Details: {'New Project' if mode == 'Create New Project' else selected_code}")
        
        c1, c2 = st.columns(2)
        # Project Code is the identifier for upserting
        p_code = c1.text_input("Project Code (Client Login Secret)", 
                               value=project_data.get("project_code", ""), 
                               help="This is the unique, plain-text secret for client login.")
        p_name = c2.text_input("Project Name", value=project_data.get("project_name", ""))
        
        title = st.text_input("Title (Dashboard Header)", value=project_data.get("title", "Weekly Project Update"))
        
        # NEW FIELD
        logo_url = st.text_input("Project Logo/Image URL (Optional)", value=project_data.get("project_logo_url", ""), help="A direct URL to a logo or image to display on the client dashboard.")
        
        st.markdown("---")
        st.subheader("Metrics and Links")
        c3, c4, c5 = st.columns(3)
        prog = c3.slider("Progress (%)", 0, 100, value=project_data.get("project_progress", 0))
        rfi = c4.number_input("Pending RFI", value=project_data.get("pending_rfi", 0), min_value=0)
        days = c5.number_input("Days Spent", value=project_data.get("days_spent", 0), min_value=0)
        
        link1 = st.text_input("Model Review Link (URL)", value=project_data.get("model_review_link", ""))
        link2 = st.text_input("RFI Sheet Link (URL)", value=project_data.get("rfi_sheet_link", ""))
        
        alert = st.text_input("Alert Note (Max 100 chars)", value=project_data.get("alert_note", ""))
        
        st.markdown("---")
        st.subheader("Narrative Content")
        curr_prog = st.text_area("Current Progress", value=project_data.get("current_progress", ""), height=150)
        next_plan = st.text_area("Next Week Plan", value=project_data.get("next_week_plan", ""), height=150)

        submitted = st.form_submit_button("Submit/Update Project Data")

        if submitted:
            if not p_code or not p_name:
                st.error("Project Code and Name are required.")
            else:
                data = {
                    "project_code": p_code,
                    "project_name": p_name,
                    "title": title,
                    "project_progress": prog,
                    "pending_rfi": rfi,
                    "days_spent": days,
                    "model_review_link": link1,
                    "rfi_sheet_link": link2,
                    "alert_note": alert,
                    "current_progress": curr_prog,
                    "next_week_plan": next_plan,
                    "project_logo_url": logo_url # New Field
                }
                
                # If we are editing an existing project, we need to track if the code changed
                # The upsert logic handles the update based on the *new* code
                
                upsert_project(data)
                st.success(f"Project '{p_name}' saved successfully with code: {p_code}!")
                time.sleep(1)
                st.rerun()

    # --- Live Comments View ---
    if selected_code:
        st.markdown("---")
        st.subheader(f"Live Comments for: {selected_code}")
        
        # Auto-refresh mechanism (Polling)
        st.caption("New comments from clients will appear here automatically.")
        if st.toggle("Enable Live Refresh (10s interval)", value=True):
            time.sleep(10)
            st.rerun()

        comments = list_comments(selected_code)
        if comments:
            df = pd.DataFrame(comments)
            # Use st.dataframe for better interactivity/sorting
            st.dataframe(df, use_container_width=True, height=300) 
        else:
            st.info("No comments yet for this project.")
