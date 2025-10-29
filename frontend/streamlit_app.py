import streamlit as st
import sys
import os

# Add backend to path (important for Docker & imports)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.utils.api import signup, login
from frontend.utils.auth import is_admin, logout
# from frontend.utils.admin_api import get_users, delete_user, get_products, delete_product, get_orders

# ------------------- PAGE SETUP -------------------
st.set_page_config(page_title="Store System", page_icon="🛍️")

# Initialize session state
if "user" not in st.session_state:
    st.session_state.user = None
if "token" not in st.session_state:
    st.session_state.token = None

st.title("🛒 Store Management System")


# --- IF LOGGED OUT ---
if not st.session_state.user:
    tab_login, tab_signup = st.tabs(["🔑 Login", "📝 Signup"])

    # LOGIN TAB
    with tab_login:
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            result = login(email, password)
            if result:
                st.session_state.user = result["user"]
                st.session_state.token = result["access_token"]
                st.success("✅ Logged in successfully!")
                st.switch_page("pages/1_Profile.py")
            else:
                st.error("❌ Invalid credentials.")

    # SIGNUP TAB
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
                
                if signup(user_data):
                    st.success("🎉 Account created! Please login.")
                else:
                    st.error("Signup failed. Try again.")
else:
    st.switch_page("pages/1_Profile.py")