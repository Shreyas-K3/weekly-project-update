import streamlit as st
import app.client as client
import app.admin as admin
import app.db as db

# Page Config
st.set_page_config(
    page_title="Weekly Project Update",
    page_icon="🏗️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Initialize DB (Creates tables if not exist)
db.init_db()

# Navigation
# Hidden sidebar navigation for security through obscurity/simplicity
# In a real app, you might want a password on the admin route, 
# but per specs, Admin page is open.
page = st.sidebar.radio("Navigate", ["Client View", "Admin Panel"])

if page == "Client View":
    client.app()
elif page == "Admin Panel":
    admin.app()
