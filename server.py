import streamlit as st
from data_store import load_data, save_data

st.set_page_config(
    page_title="Atlas Copco - Admin Panel",
    page_icon="🛠️",
    layout="wide"
)

st.title("🛠️ Project Atlas Copco – Admin / Server")
st.caption("Change values here. Viewer app will reflect updates.")

data = load_data()

with st.form("edit_form"):
    st.subheader("Basic Info")
    col1, col2 = st.columns(2)
    with col1:
        data["project_name"] = st.text_input("Project Name", value=data["project_name"])
        data["project_code"] = st.text_input("Project Access Code (for client login)", value=data["project_code"])
    with col2:
        data["project_completion"] = st.number_input(
            "Project Completion (%)",
            min_value=0, max_value=100,
            value=int(data["project_completion"])
        )
        data["project_status_label"] = st.text_input("Project Status Label", value=data["project_status_label"])

    st.markdown("---")

    st.subheader("RFIs & Timeline")
    col3, col4, col5 = st.columns(3)
    with col3:
        data["pending_rfis"] = st.number_input(
            "Pending RFIs (count)",
            min_value=0,
            value=int(data["pending_rfis"])
        )
    with col4:
        data["rfis_label"] = st.text_input("RFI Criticality Label", value=data["rfis_label"])
    with col5:
        data["timeline_days"] = st.number_input(
            "Timeline (days in plan)",
            min_value=0,
            value=int(data["timeline_days"])
        )

    st.markdown("---")

    st.subheader("Links")
    data["viewer_link"] = st.text_input("Viewer Link URL", value=data["viewer_link"])
    data["rfi_sheet_link"] = st.text_input("RFI Sheet URL", value=data["rfi_sheet_link"])

    st.markdown("---")

    st.subheader("Model Progress (%)")
    col6, col7 = st.columns(2)
    with col6:
        data["phe_progress"] = st.slider(
            "PHE Model Progress (%)",
            min_value=0, max_value=100,
            value=int(data["phe_progress"])
        )
        data["elec_progress"] = st.slider(
            "ELEC Model Progress (%)",
            min_value=0, max_value=100,
            value=int(data["elec_progress"])
        )
    with col7:
        data["ff_progress"] = st.slider(
            "FF Model Progress (%)",
            min_value=0, max_value=100,
            value=int(data["ff_progress"])
        )
        data["mech_progress"] = st.slider(
            "MECH Model Progress (%)",
            min_value=0, max_value=100,
            value=int(data["mech_progress"])
        )

    st.markdown("---")

    st.subheader("Notes (Markdown)")
    data["notes_markdown"] = st.text_area(
        "Important Notes (Markdown allowed)",
        value=data["notes_markdown"],
        height=180
    )

    st.markdown("---")

    st.subheader("Next Steps (4-Day Plan)")
    col8, col9 = st.columns(2)
    with col8:
        data["days_1_2"] = st.text_input("Days 1–2 Main Text", value=data["days_1_2"])
        data["days_1_2_sub"] = st.text_input("Days 1–2 Sub Text", value=data["days_1_2_sub"])
    with col9:
        data["days_3_4"] = st.text_input("Days 3–4 Main Text", value=data["days_3_4"])
        data["days_3_4_sub"] = st.text_input("Days 3–4 Sub Text", value=data["days_3_4_sub"])

    st.markdown("---")

    st.subheader("Email Body (Shown in Expander on Client)")
    data["email_body"] = st.text_area(
        "Email Body (Markdown)",
        value=data["email_body"],
        height=200
    )

    submitted = st.form_submit_button("💾 Save Changes")

if submitted:
    save_data(data)
    st.success("✅ Data saved! Client viewer will now show updated values.")
