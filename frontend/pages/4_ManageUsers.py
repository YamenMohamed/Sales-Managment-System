import streamlit as st
import pandas as pd
from frontend.utils.admin_api import get_users, delete_user
from frontend.utils.auth import is_admin, logout

st.set_page_config(page_title="Manage Users", page_icon="👥")

if "user" not in st.session_state or not st.session_state.user:
    st.switch_page("streamlit_app.py")

if not is_admin():
    st.error("🚫 Access denied. Admins only.")
    st.stop()

user = st.session_state.user
st.sidebar.success(f"Logged in as: {user['name']} ({user['role']})")

if st.sidebar.button("Logout"):
    logout()

st.title("👥 Manage Users")

users = get_users()


if not users:
    st.info("No users found.")
else:
    df = pd.DataFrame(users)
    
    # Search
    search = st.text_input("🔍 Search users by name, email, or role")
    if search:
        df = df[df.apply(lambda row: search.lower() in str(row).lower(), axis=1)]

    # Sort
    sort_by = st.selectbox("Sort by", df.columns, index=list(df.columns).index("id") if "id" in df.columns else 0)
    df = df.sort_values(by=sort_by)

    # Paginate
    page_size = 100
    total_pages = (len(df) // page_size) + 1
    page = st.number_input("Page", min_value=1, max_value=total_pages, step=1)
    start, end = (page - 1) * page_size, page * page_size
    st.dataframe(df.iloc[start:end], use_container_width=True)

    # Delete user
    selected_user = st.selectbox("Select user to delete", df["name"])
    if st.button("🗑️ Delete Selected User"):
        user_row = df[df["name"] == selected_user].iloc[0]
        delete_user(user_row["id"])
        st.success(f"✅ Deleted {user_row['name']}")
        st.rerun()
