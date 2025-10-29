import streamlit as st
import pandas as pd
from frontend.utils.admin_api import (
    get_products, delete_product, add_product, update_product,
    get_categories, add_category
)
from frontend.utils.auth import is_admin, logout

st.set_page_config(page_title="Manage Products", page_icon="📦")

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
if st.sidebar.button("Manage Orders"):
    st.switch_page("pages/6_ManageOrders.py")

# --- Main Page ---
st.header("📦 Manage Products")

products = get_products()
categories = get_categories()
category_names = [c["name"] for c in categories]

if not products:
    st.info("No products available.")
else:
    df = pd.DataFrame(products)
    st.dataframe(df, width="stretch")

    # --- Delete ---
    selected_id = st.selectbox("Select Product ID to Delete", [p["id"] for p in products])
    if st.button("🗑️ Delete Product"):
        delete_product(selected_id)
        st.success(f"✅ Deleted product with ID {selected_id}")
        st.rerun()

# ============================
# 🚀 ADD PRODUCT SECTION
# ============================
st.divider()
st.subheader("➕ Add New Product")

with st.form("add_product_form"):
    name = st.text_input("Product Name")
    price = st.number_input("Price (EGP)", min_value=0.0, step=0.01)
    stock = st.number_input("Stock Quantity", min_value=0, step=1)
    category_option = st.selectbox("Select Category", ["-- New Category --"] + category_names)
    new_category_name = st.text_input("If New Category, Enter Name")

    submitted = st.form_submit_button("Add Product")
    if submitted:
        # Determine category_id
        if category_option != "-- New Category --":
            selected_cat = next((c for c in categories if c["name"] == category_option), None)
        elif new_category_name.strip():
            added_category = add_category(new_category_name.strip())
            selected_cat = added_category
        else:
            selected_cat = None

        category_id = selected_cat["id"] if selected_cat else None

        product_data = {
            "name": name,
            "price": price,
            "stock_quantity": stock,
            "category_id": category_id
        }

        result = add_product(product_data)
        if result:
            st.success("✅ Product added successfully!")
            st.rerun()
        else:
            st.error("❌ Failed to add product.")

# ============================
# ✏️ UPDATE PRODUCT SECTION
# ============================
st.divider()
st.subheader("✏️ Update Existing Product")

if products:
    product_ids = [p["id"] for p in products]
    selected_id = st.selectbox("Select Product ID to Update", product_ids)

    selected_product = next(p for p in products if p["id"] == selected_id)
    with st.form("update_product_form"):
        new_name = st.text_input("New Name", selected_product["name"])
        new_price = st.number_input("New Price (EGP)", min_value=0.0, step=0.01, value=float(selected_product["price"]))
        new_stock = st.number_input("New Stock Quantity", min_value=0, step=1, value=int(selected_product["stock_quantity"]))
        category_option = st.selectbox("Select New Category", ["-- New Category --"] + category_names)
        new_category_name = st.text_input("If New Category, Enter Name")

        update_submitted = st.form_submit_button("Update Product")
        if update_submitted:
            if category_option != "-- New Category --":
                selected_cat = next((c for c in categories if c["name"] == category_option), None)
            elif new_category_name.strip():
                added_category = add_category(new_category_name.strip())
                selected_cat = added_category
            else:
                selected_cat = None

            category_id = selected_cat["id"] if selected_cat else None

            product_data = {
                "name": new_name,
                "price": new_price,
                "stock_quantity": new_stock,
                "category_id": category_id
            }

            result = update_product(selected_product["id"], product_data)
            if result:
                st.success("✅ Product updated successfully!")
                st.rerun()
            else:
                st.error("❌ Failed to update product.")
