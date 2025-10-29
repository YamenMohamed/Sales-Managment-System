from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.utils.auth import require_admin
from backend.crud import user_crud, product_crud, order_crud, category_crud
from backend import schema , models

router = APIRouter(
    prefix="/admin",
    tags=["Admin"],
    dependencies=[Depends(require_admin)]  # All routes below require admin access
)


# USERS
@router.get("/users/")
def list_all_users(db: Session = Depends(get_db)):
    return user_crud.get_users(db)


@router.delete("/users/{user_id}")
def remove_user(user_id: int, db: Session = Depends(get_db)):
    success = user_crud.delete_user(db, user_id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted successfully"}


# PRODUCTS
@router.get("/products/")
def list_all_products(db: Session = Depends(get_db)):
    return product_crud.get_products(db)

@router.post("/products", status_code=status.HTTP_201_CREATED)
def add_product(product: schema.ProductCreate, db: Session = Depends(get_db)):
    return product_crud.create_product(db, product)


@router.put("/products/{product_id}")
def modify_product(product_id: int, product: schema.ProductUpdate, db: Session = Depends(get_db)):
    updated = product_crud.update_product(db, product_id, product)
    if not updated:
        raise HTTPException(status_code=404, detail="Product not found")
    return updated


@router.delete("/products/{product_id}")
def remove_product(product_id: int, db: Session = Depends(get_db)):
    success = product_crud.delete_product(db, product_id)
    if not success:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"message": "Product deleted successfully"}


@router.get("/categories/", response_model=list[schema.CategoryOut])
def list_all_categories(db: Session = Depends(get_db)):
    return category_crud.get_categories(db)

@router.post("/categories/", response_model=schema.CategoryOut, status_code=status.HTTP_201_CREATED)
def add_new_category(category: schema.CategoryCreate, db: Session = Depends(get_db)):
    return category_crud.create_category(db, category)


# ORDERS
@router.get("/orders")
def list_all_orders(db: Session = Depends(get_db)):
    return order_crud.get_orders(db)


@router.delete("/orders/{order_id}", status_code=200)
def remove_order(order_id: int, db: Session = Depends(get_db)):
    success = order_crud.delete_order(db, order_id)
    if success:
        return {"message": "Order deleted successfully"}
    raise HTTPException(status_code=404, detail="Order not found")

