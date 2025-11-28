import streamlit as st
import pandas as pd
import time
import json
from app.db import upsert_project, get_project_by_code, list_project_codes, list_comments
from app.utils import load_css, get_base64_image_data, kshitij_logo_svg
import os

def app():
    # Load custom CSS for the dark theme and styling
    load_css("app/style.css")
    
    # --- Header with Kshitij Logo (Top Right) ---
    col_title, col_logo = st.columns([4, 1])
    with col_title:
        st.title("Admin Panel 🛠️")
    with col_logo:
        # Kshitij logo display in the top right corner
        if st.session_state.get('kshitij_logo_base64'):
            # If logo is uploaded, display it
            st.image(st.session_state['kshitij_logo_base64'], width=80)
        else:
            # Otherwise, display the SVG fallback
            st.markdown(kshitij_logo_svg(size='80'), unsafe_allow_html=True)
            
    st.markdown("---")

    # --- Global Logo Uploads (Store in Session State for persistence across forms) ---
    st.subheader("Global Asset Management")
    col_logo_client, col_logo_kshitij = st.columns(2)

    with col_logo_client:
        st.caption("Upload Client Logo (Used in Client View)")
        uploaded_client_logo = st.file_uploader("Client Logo", type=['png', 'jpg', 'jpeg'], key="client_logo_uploader")
        if uploaded_client_logo:
            st.session_state['client_logo_base64'] = get_base64_image_data(uploaded_client_logo)
            st.image(st.session_state['client_logo_base64'], width=50, caption="Client Logo Preview")
        elif 'client_logo_base64' not in st.session_state:
             # Initialize state key if not present and no file uploaded
             st.session_state['client_logo_base64'] = None

    with col_logo_kshitij:
        st.caption("Upload Kshitij Logo (Used in Client View)")
        uploaded_kshitij_logo = st.file_uploader("Kshitij Logo", type=['png', 'jpg', 'jpeg'], key="kshitij_logo_uploader")
        if uploaded_kshitij_logo:
            st.session_state['kshitij_logo_base64'] = get_base64_image_data(uploaded_kshitij_logo)
            st.image(st.session_state['kshitij_logo_base64'], width=50, caption="Kshitij Logo Preview")
        elif 'kshitij_logo_base64' not in st.session_state:
             # Initialize state key if not present and no file uploaded
             st.session_state['kshitij_logo_base64'] = None

    st.markdown("---")
    
    # --- Project Selection ---
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
            selected_code = st.selectbox("Select Project Code to Edit", existing_codes)
            if selected_code:
                p_obj = get_project_by_code(selected_code)
                if p_obj:
                    project_data = p_obj
                
                # Load existing logos/carousel from DB into session state if not already set by global uploaders
                # This ensures the form shows the current state from the DB
                if project_data.get('client_logo_base64') and 'client_logo_base64' not in st.session_state:
                    st.session_state['client_logo_base64'] = project_data['client_logo_base64']
                if project_data.get('kshitij_logo_base64') and 'kshitij_logo_base64' not in st.session_state:
                    st.session_state['kshitij_logo_base64'] = project_data['kshitij_logo_base64']
                    
                if project_data.get('carousel_images_json'):
                    st.session_state['current_carousel_images'] = project_data['carousel_images_json']
                else:
                    st.session_state['current_carousel_images'] = []
            
    # Initialize carousel state for new projects
    if mode == "Create New Project" and 'current_carousel_images' not in st.session_state:
        st.session_state['current_carousel_images'] = []
    
    # --- Project Form ---
    with st.form("project_form"):
        st.subheader(f"Project Details: {'New Project' if mode == 'Create New Project' else selected_code}")
        
        c1, c2 = st.columns(2)
        p_code = c1.text_input("Project Code (Client Login Secret)", 
                               value=project_data.get("project_code", ""), 
                               help="This is the unique, plain-text secret for client login.")
        p_name = c2.text_input("Project Name", value=project_data.get("project_name", ""))
        
        title = st.text_input("Title (Dashboard Header)", value=project_data.get("title", "Weekly Project Update"))
        
        st.markdown("---")
        st.subheader("Metrics and Links")
        c3, c4, c5 = st.columns(3)
        prog = c3.slider("Progress (%)", 0, 100, value=project_data.get("project_progress", 0))
        rfi = c4.number_input("Pending RFI", value=project_data.get("pending_rfi", 0), min_value=0)
        days = c5.number_input("Days Spent", value=project_data.get("days_spent", 0), min_value=0)
        
        link1 = st.text_input("Model Review Link (URL)", value=project_data.get("model_review_link", ""))
        link2 = st.text_input("RFI Sheet Link (URL)", value=project_data.get("rfi_sheet_link", ""))
        
        # Text area for the important alert note
        alert = st.text_area("Alert Note (Visible to Client)", value=project_data.get("alert_note", ""), height=100)
        
        st.markdown("---")
        st.subheader("Visual Asset Upload (Carousel)")
        st.caption("Upload images (PNG/JPG) for the image carousel displayed below the Next Week Plan.")
        
        uploaded_carousel_files = st.file_uploader("Add Images to Carousel", type=['png', 'jpg', 'jpeg'], accept_multiple_files=True, key="carousel_uploader")

        if uploaded_carousel_files:
            # Process new uploads and add to session state
            for file in uploaded_carousel_files:
                base64_data = get_base64_image_data(file)
                # Check if image is already added to prevent duplicates
                if base64_data and base64_data not in st.session_state['current_carousel_images']:
                    st.session_state['current_carousel_images'].append(base64_data)
            st.success(f"Added {len(uploaded_carousel_files)} images.")

        # Display current carousel images and allow removal
        # This section was MOVED OUTSIDE the form to fix the StreamlitAPIException.
        
        st.markdown("---")
        st.subheader("Narrative Content")
        curr_prog = st.text_area("Current Progress", value=project_data.get("current_progress", ""), height=150)
        next_plan = st.text_area("Next Week Plan", value=project_data.get("next_week_plan", ""), height=150)

        # Added key="project_submit_button" for robustness
        submitted = st.form_submit_button("Submit/Update Project Data", key="project_submit_button")

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
                    # Logos and Carousel are pulled from session state
                    "client_logo_base64": st.session_state.get('client_logo_base64'),
                    "kshitij_logo_base64": st.session_state.get('kshitij_logo_base64'),
                    "carousel_images_json": st.session_state.get('current_carousel_images', [])
                }
                
                upsert_project(data)
                st.success(f"Project '{p_name}' saved successfully with code: {p_code}!")
                time.sleep(1)
                st.rerun()
    
    # --- Carousel Removal Section (Moved Outside the Form) ---
    # Display current carousel images and allow removal
    if st.session_state.get('current_carousel_images'):
        st.markdown("##### Current Carousel Images:")
        st.caption("Click 'Remove' to delete an image immediately. Don't forget to click 'Submit/Update Project Data' above to save the updated image list to the database.")
        # Use columns for a grid-like view
        cols = st.columns(4)
        # Create a temporary copy to iterate over
        carousel_copy = st.session_state['current_carousel_images'][:] 
        
        for i, img_data in enumerate(carousel_copy):
            with cols[i % 4]:
                st.image(img_data, use_column_width=True)
                # Button to remove the image (NOW OUTSIDE THE FORM)
                if st.button(f"Remove {i+1}", key=f"remove_img_{i}"):
                    try:
                        # Remove the image from the actual session state list
                        st.session_state['current_carousel_images'].pop(i)
                        st.rerun() # Rerun to refresh the list display
                    except IndexError:
                        pass # Should not happen with correct indexing

    st.markdown("---")
    # --- Live Comments View ---
    if selected_code:
        st.markdown("---")
        st.subheader(f"Live Comments for: {selected_code}")
        
        st.caption("New comments from clients will appear here automatically.")
        # Automatic refresh for live updates
        if st.toggle("Enable Live Refresh (10s interval)", value=True):
            time.sleep(10)
            st.rerun()

        comments = list_comments(selected_code)
        if comments:
            df = pd.DataFrame(comments)
            st.dataframe(df, use_container_width=True, height=300) 
        else:
            st.info("No comments yet for this project.")
