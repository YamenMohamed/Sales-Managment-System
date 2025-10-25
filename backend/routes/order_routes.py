from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.database import get_db
from backend import schema
from backend.crud import order_crud

router = APIRouter(prefix="/orders", tags=["Orders"])

@router.get("/user/{user_id}", response_model=list[schema.OrderOut])
def get_orders_by_user(user_id: int, db: Session = Depends(get_db)):
    """
    Show all orders made by a specific user.
    """ 
    return order_crud.get_orders_by_user(db, user_id)


@router.post("/", response_model=schema.OrderOut)
def create_order(order: schema.OrderCreate, db: Session = Depends(get_db)):
    """
    Create a new order and its items.
    """
    return order_crud.create_order(db, order)
