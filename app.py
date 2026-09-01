
import streamlit as st
import pandas as pd
from datetime import datetime
import io

# Page configuration
st.set_page_config(page_title="Machine Check Sheet", page_icon="⚙️", layout="centered")

st.title("⚙️ Machine Daily Inspection Sheet")
st.caption("Live capture mode enabled • File upload disabled")

# --- Form Section ---
with st.form("machine_check_form", clear_on_submit=False):
    
    # 1. General Info
    st.subheader("1. General Information")
    col1, col2 = st.columns(2)
    with col1:
        inspector_name = st.text_input("Inspector Name *")
        machine_id = st.selectbox("Machine / Equipment ID", ["CNC-001", "PRESS-04", "LATHE-02", "PUMP-01"])
    with col2:
        check_date = st.date_input("Date", value=datetime.today())
        shift = st.selectbox("Shift", ["Morning", "Afternoon", "Night"])

    st.markdown("---")

    # 2. Check Items
    st.subheader("2. Check Items")
    c1 = st.radio("Lubrication / Oil Level", ["Normal", "Low / Needs Refill", "Critical"], horizontal=True)
    c2 = st.radio("Operating Pressure & Temperature", ["Normal", "Abnormal"], horizontal=True)
    c3 = st.radio("Unusual Noise / Vibration", ["None (Normal)", "Minor Noise", "Heavy Vibration"], horizontal=True)
    c4 = st.radio("Emergency Stop & Safety Guards", ["Functional", "Defective"], horizontal=True)
    c5 = st.radio("Cleanliness & Debris", ["Clean", "Needs Cleaning"], horizontal=True)

    remarks = st.text_area("Observations / Action Items")

    st.markdown("---")

    # 3. Live Photo Capture (No Import Allowed)
    st.subheader("3. Live Machine Condition Photo")
    st.info("Take a live photo using the device camera. File browsing is disabled.")
    
    # st.camera_input only allows live camera capture
    captured_image = st.camera_input("Capture live photo")

    st.markdown("---")
    submitted = st.form_submit_button("Submit Inspection Report", use_container_width=True)

# --- Submission Handling ---
if submitted:
    if not inspector_name:
        st.error("Please enter the Inspector Name before submitting.")
    elif captured_image is None:
        st.warning("A live photo of the machine is required for verification.")
    else:
        st.success("Inspection submitted successfully!")
        
        # Summary Data
        data = {
            "Inspector": inspector_name,
            "Machine ID": machine_id,
            "Date": str(check_date),
            "Shift": shift,
            "Lubrication": c1,
            "Pressure/Temp": c2,
            "Vibration/Noise": c3,
            "Safety Guards": c4,
            "Cleanliness": c5,
            "Remarks": remarks if remarks else "N/A",
            "Photo Status": "Captured & Verified"
        }
        
        st.dataframe(pd.DataFrame([data]).T, use_container_width=True)