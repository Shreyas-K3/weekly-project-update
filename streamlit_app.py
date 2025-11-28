import streamlit as st
import app.client as client
import app.admin as admin
import app.db as db

# --- Configuration & Initialization ---

# Set a hardcoded Admin Access Code. 
# IN PRODUCTION: Use st.secrets or environment variable for this value!
ADMIN_ACCESS_CODE = "k3masteraccess"

st.set_page_config(
    page_title="Weekly Project Update",
    page_icon="🏗️",
    layout="wide", # Changed to wide for better meter display
    initial_sidebar_state="collapsed"
)

# Initialize DB (Creates tables if not exist)
db.init_db()

# --- Navigation and Routing ---

# Initialize session state for admin auth
if "admin_authenticated" not in st.session_state:
    st.session_state.admin_authenticated = False

page = st.sidebar.radio("Navigate", ["Client View", "Admin Panel"])

if page == "Client View":
    client.app()

elif page == "Admin Panel":
    st.sidebar.markdown("---")
    st.sidebar.subheader("Admin Authentication")

    if st.session_state.admin_authenticated:
        st.sidebar.success("Authenticated.")
        admin.app()
    else:
        # Authentication Form
        with st.sidebar.form("admin_login_form"):
            admin_code = st.text_input("Admin Access Code", type="password", key="admin_code_input")
            auth_button = st.form_submit_button("Login")

            if auth_button:
                if admin_code == ADMIN_ACCESS_CODE:
                    st.session_state.admin_authenticated = True
                    st.rerun()
                else:
                    st.error("Invalid Admin Code.")
        
        if not st.session_state.admin_authenticated:
            st.warning("Access Denied. Please log in as an Admin in the sidebar.")
