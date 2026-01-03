import streamlit as st
from api import login, signup


def auth_screen():
    st.title("🔐 MacroMind Login")

    tab1, tab2 = st.tabs(["Login", "Sign Up"])

    with tab1:
        name = st.text_input("Name", key="login_name")
        password = st.text_input("Password", type="password", key="login_pass")

        if st.button("Login"):
            res = login(name, password)

            if res.status_code == 200:
                data = res.json()
                st.session_state.token = data["access_token"]
                st.success("Logged in successfully")
                st.rerun()
            else:
                st.error("Invalid credentials")

    with tab2:
        name = st.text_input("Name", key="signup_name")
        password = st.text_input("Password", type="password", key="signup_pass")

        if st.button("Create Account"):
            res = signup(name, password)

            if res.status_code == 200:
                st.success("Account created — now login")
            else:
                st.error(res.text)
