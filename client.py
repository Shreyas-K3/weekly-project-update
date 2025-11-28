import streamlit as st
from datetime import datetime
from data_store import load_data

# Load shared data from server
data = load_data()
VALID_PROJECT_CODE = data.get("project_code", "ATLAS2025")
ALLOWED_NAMES = data.get("allowed_names", [])

# Page config
st.set_page_config(
    page_title=f"{data.get('project_name', 'Project')} - Status Update",
    page_icon="🚀",
    layout="wide"
)

# Initialize session state
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'user_name' not in st.session_state:
    st.session_state.user_name = ""

# Custom CSS (Kept same as your original)
st.markdown("""
    <style>
    .main { padding: 2rem; }
    .login-container { max-width: 500px; margin: 5rem auto; padding: 3rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 20px; box-shadow: 0 10px 40px rgba(0,0,0,0.2); }
    .login-header { text-align: center; color: white; margin-bottom: 2rem; }
    .stAlert { padding: 1rem; border-radius: 10px; }
    .metric-card { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 2rem; border-radius: 15px; color: white; text-align: center; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
    .progress-text { font-size: 3rem; font-weight: bold; margin: 0; }
    .section-header { background: linear-gradient(90deg, #667eea 0%, #764ba2 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-size: 1.5rem; font-weight: bold; margin-top: 2rem; }
    .link-button { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 0.75rem 1.5rem; border-radius: 10px; text-decoration: none; display: inline-block; margin: 0.5rem; transition: transform 0.2s; }
    .link-button:hover { transform: translateY(-2px); box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4); }
    .info-box { background: #f0f2f6; padding: 1.5rem; border-radius: 10px; border-left: 4px solid #667eea; margin: 1rem 0; }
    .timeline-item { padding: 1rem; margin: 0.5rem 0; border-left: 3px solid #667eea; padding-left: 1.5rem; }
    .welcome-banner { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 1rem 2rem; border-radius: 10px; margin-bottom: 2rem; display: flex; justify-content: space-between; align-items: center; }
    </style>
""", unsafe_allow_html=True)

# Authentication Page
if not st.session_state.authenticated:
    st.markdown("""
        <div class="login-container">
            <div class="login-header">
                <h1>🔐 Project Access</h1>
                <p>Enter your credentials to view the status dashboard</p>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("### 👤 Authentication Required")
        
        name = st.text_input("Full Name", placeholder="Enter your full name", key="name_input")
        project_code = st.text_input("Project Code", placeholder="Enter project access code", type="password", key="code_input")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        if st.button("🚀 Access Dashboard", type="primary", use_container_width=True):
            name_clean = name.strip()

            if name_clean == "":
                st.error("❌ Please enter your name")
            elif project_code.strip() == "":
                st.error("❌ Please enter the project code")
            else:
                # Check pre-approved names (case-insensitive)
                allowed_lower = [n.strip().lower() for n in ALLOWED_NAMES]
                if name_clean.lower() not in allowed_lower:
                    st.error("❌ Name is not pre-approved. Please contact the project admin.")
                elif project_code != VALID_PROJECT_CODE:
                    st.error("❌ Invalid project code. Access denied.")
                else:
                    st.session_state.authenticated = True
                    st.session_state.user_name = name_clean
                    st.rerun()
        
        st.markdown("<br>", unsafe_allow_html=True)
        st.info("💡 Access is restricted to pre-approved names and a valid project code.")

# Main Dashboard (shown after authentication)
else:
    col1, col2 = st.columns([4, 1])
    with col1:
        st.markdown(f"""
            <div class="welcome-banner">
                <div>
                    <h2 style="margin:0;">👋 Welcome, {st.session_state.user_name}</h2>
                    <p style="margin:0; opacity:0.9;">{data.get('project_name', 'Project')} Dashboard</p>
                </div>
            </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🚪 Logout", type="secondary"):
            st.session_state.authenticated = False
            st.session_state.user_name = ""
            st.rerun()
    
    col1, col2 = st.columns([3, 1])
    with col1:
        st.title(f"🚀 {data.get('project_name', 'Atlas Copco')}")
        st.subheader("Weekly Status Update")
    with col2:
        st.metric("Week", f"{datetime.now().strftime('%W')}", "Current")

    st.markdown("---")

    col1, col2, col3 = st.columns(3)

    # Note: Using .get() ensures the app doesn't crash if a key is missing from JSON
    with col1:
        st.markdown(f"""
            <div class="metric-card">
                <p style="margin:0; font-size:1.2rem;">Project Completion</p>
                <p class="progress-text">{int(data.get('project_completion', 0))}%</p>
                <p style="margin:0;">✅ {data.get('project_status_label', 'N/A')}</p>
            </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
            <div class="metric-card" style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);">
                <p style="margin:0; font-size:1.2rem;">Pending RFIs</p>
                <p class="progress-text">{int(data.get('pending_rfis', 0))}</p>
                <p style="margin:0;">⚠️ {data.get('rfis_label', 'N/A')}</p>
            </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
            <div class="metric-card" style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);">
                <p style="margin:0; font-size:1.2rem;">Timeline</p>
                <p class="progress-text">{int(data.get('timeline_days', 0))}</p>
                <p style="margin:0;">📅 Days Plan</p>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown('<p class="section-header">🔗 Quick Access Links</p>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""
            <a href="{data.get('viewer_link', '#')}" target="_blank" class="link-button">
                📊 Open Viewer Link
            </a>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
            <a href="{data.get('rfi_sheet_link', '#')}" target="_blank" class="link-button">
                ❓ RFI Response Sheet
            </a>
        """, unsafe_allow_html=True)

    st.markdown('<p class="section-header">📝 Important Notes</p>', unsafe_allow_html=True)
    st.info(data.get("notes_markdown", "No notes for this week."))

    st.markdown('<p class="section-header">📈 Current Progress Breakdown</p>', unsafe_allow_html=True)

    progress_col1, progress_col2 = st.columns(2)

    with progress_col1:
        st.markdown("### Completed / Main Models")
        
        phe = int(data.get('phe_progress', 0))
        st.success(f"**PHE Model** ✅ {phe}%")
        st.progress(phe / 100.0)

        elec = int(data.get('elec_progress', 0))
        st.success(f"**ELEC Model** ✅ {elec}%")
        st.progress(elec / 100.0)

        st.markdown("<small>🔧 Minor clashes resolved (screenshots attached)</small>", unsafe_allow_html=True)

    with progress_col2:
        st.markdown("### In Progress Models")

        ff = int(data.get('ff_progress', 0))
        st.warning(f"**FF Model** 🔄 {ff}% Complete")
        st.progress(ff / 100.0)

        mech = int(data.get('mech_progress', 0))
        st.warning(f"**MECH Model** 🔄 {mech}% Complete")
        st.progress(mech / 100.0)

    st.markdown('<p class="section-header">🗓 Next Steps - 4-Day Plan</p>', unsafe_allow_html=True)

    timeline_col1, timeline_col2 = st.columns([1, 3])

    with timeline_col2:
        st.markdown(f"""
            <div class="timeline-item">
                <strong>Days 1-2:</strong> {data.get('days_1_2', '')}<br>
                <small style="color: #666;">{data.get('days_1_2_sub', '')}</small>
            </div>
            <div class="timeline-item">
                <strong>Days 3-4:</strong> {data.get('days_3_4', '')}<br>
                <small style="color: #666;">{data.get('days_3_4_sub', '')}</small>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("""
        <div class="info-box">
            <strong>💬 Feedback Welcome</strong><br>
            For clarifications, additional details, or any questions, please reach out to the project team.
        </div>
    """, unsafe_allow_html=True)

    with st.expander("📎 View Full Email Content"):
        st.markdown(data.get("email_body", "No email content."))

    if st.button("📥 Export Status Report", type="primary"):
        st.balloons()
        st.success("Status report exported successfully! (Demo feature)")
