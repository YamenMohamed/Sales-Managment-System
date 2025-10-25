from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.database import get_db
from backend import schema
from backend.crud import product_crud

router = APIRouter(prefix="/products", tags=["Products"])

@router.get("/", response_model=list[schema.ProductOut])
def get_available_products(db: Session = Depends(get_db)):
    """
    Return all available products (stock_quantity > 0) with category names.
    """
    return product_crud.get_available_products(db)
