import streamlit as st
from backend.utils.api import get_user_orders

st.title("📦 My Orders")

if "token" not in st.session_state or not st.session_state.token:
    st.warning("Please log in to access this page.")
    st.stop()

if "user" not in st.session_state or not st.session_state.user:
    st.warning("Please log in first.")
    st.stop()

orders = get_user_orders(st.session_state.user["id"])

if not orders:
    st.info("You don’t have any orders yet.")
else:
    for order in orders:
        with st.expander(f"🧾 Order #{order['id']} — {order['order_date']}"):
            st.write("### Items")
            for item in order["items"]:
                st.write(
                    f"- {item['product_name']} × {item['quantity']} = {item['item_price']} EGP"
                )
            st.write(f"**Total Price:** {order['total_price']} EGP")
