from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.database import get_db
from backend import schema, models
from backend.crud import user_crud
from backend.utils.security import verify_password
from backend.utils.auth import create_access_token



router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/signup", response_model=schema.UserOut)
def create_user(user: schema.UserCreate, db: Session = Depends(get_db)):
    return user_crud.create_user(db, user)


@router.post("/login", response_model=schema.TokenResponse)
def login_user(user: schema.UserLogin, db: Session = Depends(get_db)):
    db_user = user_crud.validate_user_credentials(db, user.email, user.password)
    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid email or password")

    access_token = create_access_token(
        data={"sub": db_user["email"], "role": db_user["role"]}
    )
    return {"user": db_user, "access_token": access_token}



@router.get("/{user_id}", response_model=schema.UserOut)
def get_user(user_id: int, db: Session = Depends(get_db)):
    return user_crud.get_user(db, user_id)

@router.put("/{user_id}", response_model=schema.UserOut)
def update_user(user_id: int, user: schema.UserUpdate, db: Session = Depends(get_db)):
    return user_crud.update_user(db, user_id, user)

