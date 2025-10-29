import streamlit as st
from frontend.utils.auth import is_admin, logout
from backend.utils.api import get_user, update_user
st.title("👤 My Profile")

if "user" not in st.session_state or not st.session_state.user:
    st.switch_page("streamlit_app.py")


if "token" not in st.session_state or not st.session_state.token:
    st.warning("Please log in to access this page.")
    st.stop()

if st.sidebar.button("Logout"):
    logout()


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

# st.sidebar.markdown("---")

# # Admin or User Navigation
# user = st.session_state.get("user")

# # --- Sidebar content ---
# st.sidebar.title("Navigation")
# st.sidebar.page_link("streamlit_app.py", label="Profile")
# st.sidebar.page_link("pages/2_Products.py", label="Products")
# st.sidebar.page_link("pages/3_Orders.py", label="Orders")

# # ✅ Show admin dashboard ONLY if admin
# if user and user.get("role") == "admin":
#     st.sidebar.markdown("---")
#     st.sidebar.subheader("👑 Admin Dashboard")
#     st.sidebar.page_link("pages/4_ManageUsers.py", label="Manage Users")
#     st.sidebar.page_link("pages/5_ManageProducts.py", label="Manage Products")
#     st.sidebar.page_link("pages/6_ManageOrders.py", label="Manage Orders")