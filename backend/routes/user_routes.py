from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend import schema, models
from backend.database import get_db
from backend.crud import user_crud



router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/signup", response_model=schema.UserOut)
def create_user(user: schema.UserCreate, db: Session = Depends(get_db)):
    return user_crud.create_user(db, user)

@router.post("/login", response_model=schema.UserOut)
def login_user(credentials: schema.UserLogin, db: Session = Depends(get_db)):
    user = user_crud.validate_user_credentials(db, credentials.email, credentials.password)
    if not user:
        print(credentials.password)
        raise HTTPException(status_code=401, detail="Invalid email or password")
    return user

@router.get("/{user_id}", response_model=schema.UserOut)
def get_user(user_id: int, db: Session = Depends(get_db)):
    return user_crud.get_user(db, user_id)

@router.put("/{user_id}", response_model=schema.UserOut)
def update_user(user_id: int, user: schema.UserUpdate, db: Session = Depends(get_db)):
    return user_crud.update_user(db, user_id, user)









