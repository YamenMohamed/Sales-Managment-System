import requests

BASE_URL = "http://localhost:8001"

def signup(data):
    r = requests.post(f"{BASE_URL}/users/signup", json=data)
    return r.json() if r.status_code == 200 else None

def login(email, password):
    r = requests.post(f"{BASE_URL}/users/login", json={"email": email, "password": password})
    if r.status_code == 200:
        data = r.json()
        # store both user info and token
        return data
    else:
        print("Login failed:", r.status_code, r.text)
        return None


def get_user(user_id):
    r = requests.get(f"{BASE_URL}/users/{user_id}")
    return r.json() if r.status_code == 200 else None

def update_user(user_id, data):
    r = requests.put(f"{BASE_URL}/users/{user_id}", json=data)
    return r.json() if r.status_code == 200 else None

def get_products():
    r = requests.get(f"{BASE_URL}/products/")
    return r.json() if r.status_code == 200 else []

def create_order(order_data):
    r = requests.post(f"{BASE_URL}/orders/", json=order_data)
    if r.status_code in (200, 201):
        print(r.json())
        return r.json()
    else:
        print("Error creating order:", r.status_code, r.text)
        return None

def get_user_orders(user_id):
    r = requests.get(f"{BASE_URL}/orders/user/{user_id}")
    return r.json() if r.status_code == 200 else []
