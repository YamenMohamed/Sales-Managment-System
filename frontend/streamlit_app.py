import streamlit as st
import sys
import os

# Add the parent directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.utils.api import signup, login

st.set_page_config(page_title="Store System", page_icon="🛍️")

if "user" not in st.session_state:
    st.session_state.user = None

st.title("🛒 Welcome to Store Management System")

if st.session_state.user:
    st.success(f"Welcome back, {st.session_state.user['name']}!")
    st.page_link("pages/1_Profile.py", label="Go to Profile →")
else:
    tab_login, tab_signup = st.tabs(["🔑 Login", "📝 Signup"])

    with tab_login:
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            user = login(email, password)
            if user:
                st.session_state.user = user
                st.success("Logged in successfully!")
                st.rerun()
            else:
                st.error("Invalid email or password")

    with tab_signup:
        with st.form("signup_form"):
            name = st.text_input("Full Name")
            email = st.text_input("Email")
            phone = st.text_input("Phone")
            address = st.text_input("Address")
            password = st.text_input("Password", type="password")

            if st.form_submit_button("Create Account"):
                user_data = {
                    "name": name,
                    "email": email,
                    "phone": phone,
                    "address": address,
                    "password": password,
                    "role": "user"
                }
                res = signup(user_data)
                if res:
                    st.success("Account created! Please login.")
                else:
                    st.error("Signup failed.")
