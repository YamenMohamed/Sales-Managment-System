from datetime import datetime
from backend.database import SessionLocal, init_db
from backend.models import User, UserCredential, Category, Product, Order, OrderItem
from backend.utils.security import hash_password  # if you added password hashing

# Initialize DB and session
init_db()
db = SessionLocal()

# ----------- USERS & CREDENTIALS -----------
users_data = [
    {"name": "Alice Johnson", "address": "123 Nile St, Cairo", "phone": "01012345678", "email": "alice@example.com", "password": "alice123"},
    {"name": "Omar Khaled", "address": "45 Tahrir Sq, Giza", "phone": "01198765432", "email": "omar@example.com", "password": "omar123"},
    {"name": "Sara Ahmed", "address": "7 Corniche Rd, Alexandria", "phone": "01234567890", "email": "sara@example.com", "password": "sara123"},
]

users = []
for u in users_data:
    user = User(name=u["name"], address=u["address"], phone=u["phone"])
    db.add(user)
    db.commit()
    db.refresh(user)

    cred = UserCredential(
        email=u["email"],
        password=hash_password(u["password"]),
        user_id=user.id
    )
    db.add(cred)
    db.commit()
    users.append(user)

# ----------- CATEGORIES -----------
categories = [
    Category(name="Electronics"),
    Category(name="Clothing"),
    Category(name="Groceries"),
]
db.add_all(categories)
db.commit()

# ----------- PRODUCTS -----------
products = [
    Product(name="Smartphone", price=12000.0, category_id=categories[0].id, stock_quantity=15),
    Product(name="Laptop", price=25000.0, category_id=categories[0].id, stock_quantity=8),
    Product(name="T-Shirt", price=350.0, category_id=categories[1].id, stock_quantity=50),
    Product(name="Jeans", price=800.0, category_id=categories[1].id, stock_quantity=40),
    Product(name="Olive Oil", price=90.0, category_id=categories[2].id, stock_quantity=100),
]
db.add_all(products)
db.commit()

# ----------- ORDERS & ORDER ITEMS -----------
orders = [
    Order(user_id=users[0].id, order_date=datetime(2025, 10, 20, 14, 30)),
    Order(user_id=users[1].id, order_date=datetime(2025, 10, 21, 10, 15)),
]
db.add_all(orders)
db.commit()

order_items = [
    OrderItem(order_id=orders[0].id, product_id=products[0].id, quantity=1, price=12000.0),
    OrderItem(order_id=orders[0].id, product_id=products[2].id, quantity=2, price=700.0),
    OrderItem(order_id=orders[1].id, product_id=products[4].id, quantity=3, price=270.0),
]
db.add_all(order_items)
db.commit()

db.close()
print("✅ Sample data inserted successfully!")
