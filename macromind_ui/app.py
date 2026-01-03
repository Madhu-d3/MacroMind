import streamlit as st
from auth import auth_screen
from components import profile_section, daily_log_section

st.set_page_config(page_title="MacroMind", layout="centered")

if "token" not in st.session_state:
    auth_screen()
else:
    st.title("🏋️ MacroMind")

    tab1, tab2 = st.tabs(["📅 Daily Log", "👤 Profile"])

    with tab1:
        daily_log_section()

    with tab2:
        profile_section()

    st.divider()
    if st.button("Logout"):
        st.session_state.clear()
        st.experimental_rerun()
