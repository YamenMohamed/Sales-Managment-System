from sqlalchemy.orm import Session
from backend import models, schema

# ------------------ User CRUD ------------------

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

def create_user(db: Session, user: schema.UserCreate):
    new_user = models.User(
        name=user.name,
        email=user.email,
        password=user.password,
        role=user.role
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def update_user(db: Session, user_id: int, user_update: schema.UserUpdate):
    user = get_user(db, user_id)
    if not user:
        return None
    for key, value in user_update.dict(exclude_unset=True).items():
        setattr(user, key, value)
    db.commit()
    db.refresh(user)
    return user

def delete_user(db: Session, user_id: int):
    user = get_user(db, user_id)
    if user:
        db.delete(user)
        db.commit()
        return True
    return False

# ------------------ Category CRUD ------------------

def get_categories(db:Session):
    return db.query(models.Category).all()

def get_category(db:Session,category_id):
    return db.query(models.Category).filter(models.Category.id == category_id).first()

def create_category(db:Session,category:schema. CategoryCreate):
    # Check if the new category already exists
    existing_category = db.query(models.Category).filter(
        models.Category.name == category.name
    ).first()

    if existing_category:
        return category
    
    # Otherwise create a new one
    new_category = models.Category(name = category.name)
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    return new_category

def delete_category(db:Session, category_id:int):
    category = get_category(db,category_id)
    if category:
        db.delete(category)
        db.commit()
        print("Category deleted successfuly !")
        return True
    print("Category not Found !!")
    return False


# ------------------ Product CRUD ------------------

def get_products(db:Session):
    return db.query(models.Product).all()


def get_product(db:Session,product_id:int):
    return db.query(models.Product).filter(models.Product.id == product_id).first()


def create_product(db: Session, product: schema.ProductCreate):
    # Check if product already exists by name + category
    existing_product = db.query(models.Product).filter(
        models.Product.name == product.name,
        models.Product.category_id == product.category_id
    ).first()

    if existing_product:
        # Update stock if already exists
        existing_product.stock_quantity += product.stock_quantity
        db.commit()
        db.refresh(existing_product)
        return existing_product

    # Otherwise create a new one
    new_product = models.Product(
        name=product.name,
        price=product.price,
        category_id=product.category_id,
        stock_quantity=product.stock_quantity
    )
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product


def update_product(db: Session, product_id: int, product_update: schema.ProductUpdate):
    product = get_product(db, product_id)
    
    if not product:
        return None
    
    for key, value in product_update.dict(exclude_unset=True).items():
        setattr(product, key, value)
    db.commit()
    db.refresh(product)
    return product



def delete_product(db:Session,product_id:int):
    product = get_product(db,product_id)
    
    if product:
        db.delete(product)
        db.commit()
        print("Product deleted successfully !!")
        return True
    
    print("Product not Found !!")
    return False

# ------------------ OrderItems CRUD ------------------
def get_orderItems(db:Session):
    return db.query(models.OrderItem).all()

def get_orderItems(db:Session,order_id:int):
    return db.query(models.OrderItem).filter(models.OrderItem.order_id == order_id).all()


def get_orderItem(db:Session,orderItem_id:int):
    return db.query(models.OrderItem).filter(models.OrderItem.id == orderItem_id).first()


def create_orderItem(db:Session,orderItem :schema.OrderItemCreate):

    new_orderItem = models.OrderItem(
        order_id = orderItem.order_id,
        product_id = orderItem.product_id,
        quantity = orderItem.quantity,
        price = orderItem.quantity * get_product(db,orderItem.product_id).price
    )
    db.add(new_orderItem)
    db.commit()
    db.refresh(new_orderItem)
    return new_orderItem

def delete_orderItem(db:Session,orderItem_id):
    orderItem = get_orderItem(db,orderItem)

    if orderItem:
        product = get_product(db,orderItem.product_id)
        product.stock_quantity += orderItem.quantity
        db.delete(orderItem)
        db.commit()
        print("OrderItem is deleted successfully !!")
        return True
    
    print("OrderItem not Found !!")
    return False

# ------------------ Order CRUD ------------------

def get_orders(db:Session):
    return db.query(models.Order).all()

def get_order(db:Session,order_id:int):
    return db.query(models.Order).filter(models.Order.id == order_id).first()

def create_order(db:Session,order: schema.OrderCreate):
    new_order = models.Order(
        user_id = order.user_id,
        order_date = order.order_date
    )
    db.add(new_order)
    db.commit()
    db.refresh(new_order)

    for item in order.items:
        order_item = models.OrderItem(
            order_id=new_order.id,
            product_id=item.product_id,
            quantity=item.quantity
        )
        db.add(order_item)

    db.commit()
    db.refresh(new_order)
    return new_order


def delete_order(db:Session,order_id:int):
    order = get_order(db,order_id)

    if order:
        # return order so every product is added back to the stock
        orderItems = get_orderItem(db,order.id)
        for orderItem in orderItems:
            delete_orderItem(db,orderItem.id)

        db.delete(order)
        db.commit()
        print("Order deleted successfully !!")
        return True
    
    print("Order not Found !!")
    return False