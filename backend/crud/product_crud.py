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