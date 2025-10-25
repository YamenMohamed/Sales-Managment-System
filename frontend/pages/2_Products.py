import streamlit as st
import datetime
from backend.utils.api import get_products, create_order

st.title("🛍️ Products")

# Ensure user is logged in
if "user" not in st.session_state or not st.session_state.user:
    st.warning("Please log in first.")
    st.stop()

if "token" not in st.session_state or not st.session_state.token:
    st.warning("Please log in to access this page.")
    st.stop()


# Initialize cart in session
if "cart" not in st.session_state:
    st.session_state.cart = []

products = get_products()

if not products:
    st.info("No products available.")
else:
    st.subheader("🛒 Add Products to Cart")

    for product in products:
        with st.container(border=True):
            st.write(f"### {product['name']}")
            st.write(f"💰 Price: {product['price']} EGP")
            st.write(f"📦 In Stock: {product['stock_quantity']}")

            qty = st.number_input(
                f"Quantity for {product['name']}", 1, 10, 1, key=f"qty_{product['id']}"
            )

            if st.button("➕ Add to Cart", key=f"add_{product['id']}"):
                # Add or update item in cart
                found = False
                for item in st.session_state.cart:
                    if item["product_id"] == product["id"]:
                        item["quantity"] += qty
                        found = True
                        break
                if not found:
                    st.session_state.cart.append(
                        {
                            "product_id": product["id"],
                            "product_name": product["name"],
                            "price": product["price"],
                            "quantity": qty,
                        }
                    )
                st.success(f"Added {qty} × {product['name']} to cart!")

# --- CART SECTION ---
st.divider()
st.subheader("🧺 Your Cart")

if not st.session_state.cart:
    st.info("Your cart is empty.")
else:
    total = 0
    for item in st.session_state.cart:
        item_total = item["price"] * item["quantity"]
        total += item_total
        st.write(
            f"- {item['product_name']} × {item['quantity']} = {item_total} EGP"
        )

    st.write(f"### 💵 Total: {total} EGP")

    if st.button("✅ Place Order"):
        order_data = {
            "user_id": st.session_state.user["id"],
            "order_date": datetime.datetime.now().isoformat(),
            "items": [
                {"product_id": item["product_id"], "quantity": item["quantity"]}
                for item in st.session_state.cart
            ],
        }

        order = create_order(order_data)

        if order:
            st.success(f"Order created successfully! Total: {order['total_price']} EGP")
            st.session_state.cart = []  # clear cart
        else:
            st.error("Failed to create order.")
