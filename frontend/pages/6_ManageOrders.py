import streamlit as st
from frontend.utils.admin_api import get_orders, delete_order
from frontend.utils.auth import is_admin, logout

st.set_page_config(page_title="Manage Orders", page_icon="🧾")

# --- Auth check ---
if "user" not in st.session_state or not st.session_state.user:
    st.switch_page("streamlit_app.py")

if not is_admin():
    st.error("🚫 Access denied. Admins only.")
    st.stop()

# --- Sidebar ---
user = st.session_state.user
st.sidebar.success(f"Logged in as: {user['name']} ({user['role']})")

if st.sidebar.button("Logout"):
    logout()

st.sidebar.markdown("---")
st.sidebar.subheader("👑 Admin Dashboard")
if st.sidebar.button("Manage Users"):
    st.switch_page("pages/4_ManageUsers.py")
if st.sidebar.button("Manage Products"):
    st.switch_page("pages/5_ManageProducts.py")

# --- Main Page ---
st.header("🧾 Manage Orders")

orders = get_orders()

if not orders:
    st.info("No orders found.")
else:
    for order in orders:
        with st.expander(f"Order #{order['id']} — Total: {order['total_price']} EGP"):
            st.write(f"👤 User ID: {order['user_id']}")
            st.write(f"📅 Date: {order.get('order_date', 'N/A')}")

            items = order.get("items", [])
            if items:
                st.table(items)
            else:
                st.write("No items for this order.")

            col1, col2 = st.columns([1, 3])
            with col1:
                if st.button(f"🗑️ Delete Order #{order['id']}", key=f"delete_{order['id']}"):
                    success = delete_order(order["id"])
                    if success:
                        st.success(f"✅ Order #{order['id']} deleted successfully!")
                        st.rerun()
                    else:
                        st.error(f"❌ Failed to delete Order #{order['id']}")
