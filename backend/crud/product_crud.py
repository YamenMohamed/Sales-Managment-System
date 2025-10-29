from sqlalchemy.orm import Session, joinedload
from backend import models, schema

# ------------------ Product CRUD ------------------

# get all Products
def get_products(db:Session):
    return db.query(models.Product).all()

# get a specific Product
def get_product(db:Session,product_id:int):
    return db.query(models.Product).filter(models.Product.id == product_id).first()


# get all the available Products
def get_available_products(db: Session):
    """
    Return all products with stock > 0 including their category info.
    """
    products = (
        db.query(models.Product)
        .options(joinedload(models.Product.category))  # eager load category
        .filter(models.Product.stock_quantity > 0)
        .all()
    )
    return products





# def create_product(db, product: schema.ProductCreate):
#     # Check if product already exists by name + category
#     existing_product = db.query(models.Product).filter(
#         models.Product.name == product.name,
#         models.Product.category_id == product.category_id
#     ).first()

#     if existing_product:
#         # Update stock if already exists
#         existing_product.stock_quantity += product.stock_quantity
#         db.commit()
#         db.refresh(existing_product)
#         return existing_product
    
#     category_obj = None
#     if product.category_name:
#         category_obj = db.query(models.Category).filter_by(name=product.category_name).first()
#         if not category_obj:
#             category_obj = models.Category(name=product.category_name)
#             db.add(category_obj)
#             db.commit()
#             db.refresh(category_obj)

#     new_product = models.Product(
#         name=product.name,
#         price=product.price,
#         stock_quantity=product.stock_quantity,
#         category_id=category_obj.id if category_obj else None
#     )
#     db.add(new_product)
#     db.commit()
#     db.refresh(new_product)
#     return new_product


# def update_product(db, product_id: int, product: schema.ProductUpdate):
#     db_product = db.query(models.Product).filter(models.Product.id == product_id).first()
#     if not db_product:
#         return None

#     if product.name is not None:
#         db_product.name = product.name
#     if product.price is not None:
#         db_product.price = product.price
#     if product.stock_quantity is not None:
#         db_product.stock_quantity = product.stock_quantity

#     if product.category_name:
#         category_obj = db.query(models.Category).filter_by(name=product.category_name).first()
#         if not category_obj:
#             category_obj = models.Category(name=product.category_name)
#             db.add(category_obj)
#             db.commit()
#             db.refresh(category_obj)
#         db_product.category_id = category_obj.id

#     db.commit()
#     db.refresh(db_product)
#     return db_product


def create_product(db: Session, product):
    # Check if product already exists (same name and category)
    existing = (
        db.query(models.Product)
        .filter(
            models.Product.name == product.name,
            models.Product.category_id == product.category_id
        )
        .first()
    )

    if existing:
        # Product already exists → just increase stock
        existing.stock_quantity += product.stock_quantity
        db.commit()
        db.refresh(existing)
        return existing

    # Create a new product
    new_product = models.Product(
        name=product.name,
        price=product.price,
        stock_quantity=product.stock_quantity,
        category_id=product.category_id
    )
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product


# ------------------ UPDATE PRODUCT ------------------
def update_product(db: Session, product_id: int, product: schema.ProductUpdate):
    db_product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not db_product:
        return None

    if product.name is not None:
        db_product.name = product.name
    if product.price is not None:
        db_product.price = product.price
    if product.stock_quantity is not None:
        db_product.stock_quantity = product.stock_quantity

    if product.category_name:
        category_obj = db.query(models.Category).filter_by(name=product.category_name).first()
        if not category_obj:
            category_obj = models.Category(name=product.category_name)
            db.add(category_obj)
            db.commit()
            db.refresh(category_obj)
        db_product.category_id = category_obj.id

    db.commit()
    db.refresh(db_product)
    return db_product



def delete_product(db:Session,product_id:int):
    product = get_product(db,product_id)
    
    if product:
        db.delete(product)
        db.commit()
        print("Product deleted successfully !!")
        return True
    
    print("Product not Found !!")
    return False