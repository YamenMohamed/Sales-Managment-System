import requests
import streamlit as st

API_URL = "http://localhost:8001"

#---------------Users----------------
def get_users():
    token = st.session_state.get("token")
    headers = {"Authorization": f"Bearer {token}"}
    res = requests.get(f"{API_URL}/admin/users/", headers=headers)
    return res.json() if res.status_code == 200 else []

def delete_user(user_id: int):
    token = st.session_state.get("token")
    headers = {"Authorization": f"Bearer {token}"}
    res = requests.delete(f"{API_URL}/admin/users/{user_id}", headers=headers)
    return res.status_code == 200

#---------------Products----------------
def get_categories():
    token = st.session_state.get("token")
    headers = {"Authorization": f"Bearer {token}"}
    res = requests.get(f"{API_URL}/admin/categories/", headers=headers)
    return res.json() if res.status_code == 200 else []

def add_category(name: str):
    token = st.session_state.get("token")
    headers = {"Authorization": f"Bearer {token}"}
    payload = {"name": name}
    res = requests.post(f"{API_URL}/admin/categories/", json=payload, headers=headers)
    if res.status_code == 201:
        return res.json()
    return None

def add_product(product_data):
    token = st.session_state.get("token")
    headers = {"Authorization": f"Bearer {token}"}
    res = requests.post(f"{API_URL}/admin/products", json=product_data, headers=headers)
    return res.json() if res.status_code in (200, 201) else None


def update_product(product_id: int, product_data: dict):
    token = st.session_state.get("token")
    headers = {"Authorization": f"Bearer {token}"}
    res = requests.put(f"{API_URL}/admin/products/{product_id}", headers=headers, json=product_data)
    return res.json() if res.status_code == 200 else None


def get_products():
    token = st.session_state.get("token")
    headers = {"Authorization": f"Bearer {token}"}
    res = requests.get(f"{API_URL}/admin/products/", headers=headers)
    return res.json() if res.status_code == 200 else []

def delete_product(product_id: int):
    token = st.session_state.get("token")
    headers = {"Authorization": f"Bearer {token}"}
    res = requests.delete(f"{API_URL}/admin/products/{product_id}", headers=headers)
    return res.status_code == 200

#---------------Orders----------------
def get_orders():
    token = st.session_state.get("token")
    headers = {"Authorization": f"Bearer {token}"}
    res = requests.get(f"{API_URL}/admin/orders/", headers=headers)
    return res.json() if res.status_code == 200 else []

def delete_order(order_id):
    token = st.session_state.get("token")
    headers = {"Authorization": f"Bearer {token}"}
    res = requests.delete(f"{API_URL}/admin/orders/{order_id}", headers=headers)
    return res.status_code == 200
