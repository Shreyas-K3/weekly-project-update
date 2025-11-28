import streamlit as st
import time
import json
from app.db import get_project_by_code, add_comment
# Assuming these utilities are available from app/utils.py (as provided in the previous step)
from app.utils import load_css, create_circular_meter, roadmap_svg, kshitij_logo_svg

def app():
    load_css("app/style.css")

    # --- Authentication State ---
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
        st.session_state.project_data = None

    # --- Login Screen ---
    if not st.session_state.logged_in:
        st.title("Client Login")
        st.markdown("---")
        
        with st.form("client_login_form"):
            name_input = st.text_input("Your Name", key="client_name_input")
            code_input = st.text_input("Project Code", type="password", key="client_code_input") 
            submit_button = st.form_submit_button("View Dashboard")

            if submit_button:
                if code_input and name_input:
                    project_data = get_project_by_code(code_input)
                    if project_data:
                        st.session_state.logged_in = True
                        st.session_state.client_name = name_input
                        st.session_state.project_code = code_input
                        st.session_state.project_data = project_data # Store data
                        st.rerun()
                    else:
                        st.error("Invalid Project Code.")
                else:
                    st.warning("Please enter name and code.")
        return

    # --- Dashboard ---
    # Retrieve project data from session state (or refresh if needed, for simplicity we use state here)
    project = st.session_state.project_data
    if project is None:
        project = get_project_by_code(st.session_state.project_code)
        st.session_state.project_data = project # Update state

    if not project:
        st.error("Project not found. The project code may have been updated or deleted.")
        if st.button("Back to Login"):
            st.session_state.logged_in = False
            st.session_state.project_data = None
            st.rerun()
        return

    # --- Header and Logo (Centered Alignment) ---
    col_client_logo, col_center_text, col_kshitij_logo = st.columns([1, 4, 1])

    with col_client_logo:
        # Client Logo (from Base64 in DB)
        if project.get('client_logo_base64'):
            # Use HTML to prevent Streamlit from wrapping the image in an undesired container size
            st.markdown(f'<img src="{project["client_logo_base64"]}" style="width:100px; height:auto; display:block; margin: 0 auto;"/>', unsafe_allow_html=True)
        else:
            # Fallback placeholder
            st.markdown(f'<div style="width:100px; height:100px; background:#111; border: 2px solid #333; border-radius:10px; display:flex; justify-content:center; align-items:center; font-size: 2em; margin: 0 auto;">🏢</div>', unsafe_allow_html=True)
            
    with col_center_text:
        # Center aligned titles using markdown HTML
        st.markdown(f'<h1 style="text-align:center; color:#FF0000; margin-bottom: 0px;">{project["project_name"]}</h1>', unsafe_allow_html=True)
        st.markdown(f'<h2 style="text-align:center; color:#FFFFFF; margin-top: 0px;">{project["title"]}</h2>', unsafe_allow_html=True)

    with col_kshitij_logo:
        # Kshitij Logo (from Base64 in DB or SVG fallback)
        if project.get('kshitij_logo_base64'):
            st.markdown(f'<img src="{project["kshitij_logo_base64"]}" style="width:100px; height:auto; display:block; margin: 0 auto;"/>', unsafe_allow_html=True)
        else:
            st.markdown(kshitij_logo_svg(size='100'), unsafe_allow_html=True)

    st.markdown("---")

    # --- Metrics Row (Progress Gauge, Days Spent, RFI) ---
    st.subheader("Project Health Summary")
    
    col_prog, col_metrics = st.columns([1.5, 1])

    # 1. Overall Progress Gauge (Large and Center Aligned)
    with col_prog:
        meter_html = create_circular_meter(
            label="Overall Progress", 
            value=project["project_progress"], 
            max_value=100, 
            color="#00C853", # Bright Green
            size="250px"
        )
        # Ensure the meter is visually centered within its column
        st.markdown(f'<div style="display:flex; justify-content:center;">{meter_html}</div>', unsafe_allow_html=True)
    
    # 2. Days Spent & Pending RFI (Standard Metrics, grouped)
    with col_metrics:
        # Spacing to visually align with the center of the large gauge
        st.markdown("<br><br><br><br>", unsafe_allow_html=True) 
        st.metric("Days Spent", project["days_spent"])
        st.metric("Pending RFI", project["pending_rfi"])

    st.markdown("<br>", unsafe_allow_html=True) 

    # --- Action Buttons (Transparent Circular) ---
    st.subheader("Key Interactions")
    
    # Check if links exist before creating columns
    links_exist = project.get("model_review_link") or project.get("rfi_sheet_link")
    if links_exist:
        # Distribute buttons centrally
        l1, l2, _ = st.columns([1, 1, 2]) 

        with l1:
            if project.get("model_review_link"):
                st.markdown(f"""
                <div class="transparent-circle-link">
                    <a href="{project['model_review_link']}" target="_blank">
                        <div class="icon">💻</div> 
                        Review Model
                    </a>
                </div>
                """, unsafe_allow_html=True)
        with l2:
            if project.get("rfi_sheet_link"):
                st.markdown(f"""
                <div class="transparent-circle-link">
                    <a href="{project['rfi_sheet_link']}" target="_blank">
                        <div class="icon">🔗</div> 
                        RFI Sheet
                    </a>
                </div>
                """, unsafe_allow_html=True)

    # Alert Note (Emoji only, no red box)
    if project.get("alert_note"):
        st.markdown(f"""
        <div class="alert-box">
            🚨 {project["alert_note"]}
        </div>
        """, unsafe_allow_html=True)

    # --- Narrative Content ---
    st.markdown(f"<h4>{roadmap_svg(size='32')} Current Progress</h4>", unsafe_allow_html=True)
    st.info(project["current_progress"] or "No updates yet.")

    st.markdown(f"<h4>{roadmap_svg(size='32')} Next Week Plan</h4>", unsafe_allow_html=True)
    st.info(project["next_week_plan"] or "No updates yet.")

    # --- Image Carousel ---
    carousel_images = project.get("carousel_images_json", [])
    if carousel_images and len(carousel_images) > 0:
        st.markdown("---")
        st.subheader("Project Visuals")
        
        # Manually create the horizontal scrolling container using custom CSS
        image_html = '<div class="image-carousel">'
        for img_data in carousel_images:
            image_html += f"""
            <div class="carousel-image-wrapper">
                <img src="{img_data}" alt="Project Visual"/>
            </div>
            """
        image_html += '</div>'
        st.markdown(image_html, unsafe_allow_html=True)


    st.markdown("---")
    st.write("Feedback and inputs are welcome. For any clarifications or additional details, feel free to reach out.")

    # Interaction Section
    with st.container(border=True):
        st.subheader("Provide Feedback")
        reviewed = st.checkbox("I have reviewed the model", key="reviewed_checkbox")
        
        # Disable/Enable logic
        if reviewed:
            comment_text = st.text_area("Your Comment (Optional)", key="user_comment")
            if st.button("Submit Feedback", key="submit_comment_btn"):
                if comment_text.strip():
                    add_comment(
                        project["project_code"],
                        st.session_state.client_name,
                        comment_text
                    )
                    st.success("Feedback submitted successfully!")
                    # Clear the text area after submission
                    st.session_state.user_comment = ""
                    st.rerun() # Refresh to show clean state
                else:
                    st.warning("Please write a comment before submitting.")
        else:
            st.text_area("Your Comment", disabled=True, placeholder="Please check 'I have reviewed the model' first.")
            st.button("Submit Feedback", disabled=True)
