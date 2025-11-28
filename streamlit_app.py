import streamlit as st
import time
from app.db import get_project_by_code, add_comment
from app.utils import load_css, create_circular_meter, roadmap_svg

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
                    project = get_project_by_code(code_input)
                    if project:
                        st.session_state.logged_in = True
                        st.session_state.client_name = name_input
                        st.session_state.project_code = code_input
                        st.rerun()
                    else:
                        st.error("Invalid Project Code.")
                else:
                    st.warning("Please enter name and code.")
        return

    # --- Dashboard ---
    # Refresh data on load
    project = get_project_by_code(st.session_state.project_code)
    
    # Session cleanup if project code changed by admin
    if not project:
        st.error("Project not found. The project code may have been updated or deleted.")
        if st.button("Back to Login"):
            st.session_state.logged_in = False
            st.rerun()
        return

    # Header and Logo
    col_img, col_text = st.columns([1, 4])
    with col_img:
        if project.project_logo_url:
            st.image(project.project_logo_url, width=100, use_column_width="auto", output_format="PNG")
        else:
            # Fallback icon/placeholder
            st.markdown(f'<div style="height:100px; width:100px; background:#111; border: 2px solid #FF0000; border-radius:10px; display:flex; justify-content:center; align-items:center; font-size: 2em;">🏗️</div>', unsafe_allow_html=True)
    with col_text:
        st.title(project.project_name)
        st.header(project.title)

    st.markdown("---")

    # --- Metrics Row (Meters & RFI) ---
    st.subheader("Key Project Health Indicators")
    col_prog, col_days, col_rfi = st.columns([1.5, 1.5, 1])

    # 1. Progress Meter (Green)
    with col_prog:
        meter_html = create_circular_meter(
            label="Overall Progress", 
            value=project.project_progress, 
            max_value=100, 
            color="#00C853" # Bright Green
        )
        st.markdown(meter_html, unsafe_allow_html=True)

    # 2. Days Spent Meter (Red)
    with col_days:
        meter_html = create_circular_meter(
            label="Days Spent", 
            value=project.days_spent, 
            max_value=project.days_spent if project.days_spent > 0 else 100, # Max value is dynamic, so meter shows 100% of current days spent vs self
            color="#FF0000" # Red
        )
        st.markdown(meter_html, unsafe_allow_html=True)

    # 3. Pending RFI Metric (Card)
    with col_rfi:
        st.markdown("<br><br><br>", unsafe_allow_html=True) # Vertical alignment spacer
        st.metric("Pending RFI", project.pending_rfi)

    st.markdown("<br>", unsafe_allow_html=True) 

    # --- Action Buttons (Larger and Styled) ---
    st.subheader("Quick Access Links")
    l1, l2 = st.columns(2)
    with l1:
        if project.model_review_link:
            st.link_button("✨ Review Model", project.model_review_link, help="Open external model viewer link", use_container_width=True)
    with l2:
        if project.rfi_sheet_link:
            st.link_button("📋 RFI Sheet", project.rfi_sheet_link, help="Open external RFI tracking sheet", use_container_width=True)

    # Alert Note
    if project.alert_note:
        st.markdown(f"""
        <div class="alert-box">
            🔔 {project.alert_note}
        </div>
        """, unsafe_allow_html=True)

    # --- Text Content with Roadmap Icon ---
    
    st.subheader(f"{roadmap_svg(size='32')} Current Progress", unsafe_allow_html=True)
    st.info(project.current_progress or "No updates yet.")

    st.subheader(f"{roadmap_svg(size='32')} Next Week Plan", unsafe_allow_html=True)
    st.info(project.next_week_plan or "No updates yet.")

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
                        project.project_code,
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
