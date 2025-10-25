import streamlit as st
from backend.utils.api import get_user, update_user

st.title("👤 My Profile")

if "user" not in st.session_state or not st.session_state.user:
    st.warning("Please log in first.")
    st.stop()

if "token" not in st.session_state or not st.session_state.token:
    st.warning("Please log in to access this page.")
    st.stop()



user = st.session_state.user
profile = get_user(user["id"])

st.write(f"### Welcome, {profile['name']}!")
st.write(f"📧 Email: {profile['email']}")
st.write(f"📞 Phone: {profile['phone']}")
st.write(f"🏠 Address: {profile['address']}")
st.write(f"🧾 Role: {profile['role']}")

st.divider()

with st.expander("✏️ Update Profile"):
    name = st.text_input("Name", profile["name"])
    address = st.text_input("Address", profile["address"])
    phone = st.text_input("Phone", profile["phone"])

    if st.button("Update"):
        updated = update_user(user["id"], {"name": name, "address": address, "phone": phone})
        if updated:
            st.session_state.user = updated
            st.success("Profile updated successfully!")
            st.rerun()
