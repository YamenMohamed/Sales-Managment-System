from sqlalchemy.orm import Session
from backend import models, schema
from backend.utils.security import hash_password, verify_password
from fastapi import HTTPException
from sqlalchemy.orm import joinedload


def get_user_by_email(db: Session, email: str):
    user_cred = (
        db.query(models.UserCredential)
        .options(joinedload(models.UserCredential.user))
        .filter(models.UserCredential.email == email)
        .first()
    )
    if not user_cred:
        return None

    user = user_cred.user
    return {
        "id": user.id,
        "name": user.name,
        "address": user.address,
        "phone": user.phone,
        "role": user.role,
        "email": user_cred.email
    }


def get_user(db: Session, user_id: int):
    user = (
        db.query(models.User)
        .options(joinedload(models.User.credential))
        .filter(models.User.id == user_id)
        .first()
    )
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return {
        "id": user.id,
        "name": user.name,
        "address": user.address,
        "phone": user.phone,
        "role": user.role,
        "email": user.credential.email if user.credential else None
    }


def get_users(db: Session, skip: int = 0, limit: int = 100):
    users = (
        db.query(models.User)
        .options(joinedload(models.User.credential))
        .offset(skip)
        .limit(limit)
        .all()
    )
    return [
        {
            "id": user.id,
            "name": user.name,
            "address": user.address,
            "phone": user.phone,
            "role": user.role,
            "email": user.credential.email if user.credential else None
        }
        for user in users
    ]


def get_user_credential_model(db: Session, email: str):
    """Used internally for login authentication"""
    print("wasalt hena 2")
    return (
        db.query(models.UserCredential)
        .filter(models.UserCredential.email == email)
        .first()
    )


def validate_user_credentials(db: Session, email: str, password: str):
    user_cred = get_user_credential_model(db, email)
    if not user_cred:
        print("User Not Found !!")
        return None
    
    print("DEBUG:", password, user_cred.password)
    if not verify_password(password, user_cred.password):
        print("Incorrect Password !!")
        return None
    print("wasalt hena 1")
    return {
        "id": user_cred.user.id,
        "name": user_cred.user.name,
        "address": user_cred.user.address,
        "phone": user_cred.user.phone,
        "role": user_cred.user.role,
        "email": user_cred.email
    }



def create_user(db: Session, user_data: schema.UserCreate):
    existing = db.query(models.UserCredential).filter(models.UserCredential.email == user_data.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = models.User(
        name=user_data.name,
        address=user_data.address,
        phone=user_data.phone,
        role=user_data.role
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    hashed_pw = hash_password(user_data.password)
    credentials = models.UserCredential(
        email=user_data.email,
        password=hashed_pw, 
        user_id=new_user.id
    )
    db.add(credentials)
    db.commit()
    db.refresh(credentials)

    return {
        "id": new_user.id,
        "name": new_user.name,
        "address": new_user.address,
        "phone": new_user.phone,
        "role": new_user.role,
        "email": credentials.email
    }




def update_user(db: Session, user_id: int, user_update: schema.UserUpdate):
    user = get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    for field, value in user_update.dict(exclude_unset=True).items():
        setattr(user, field, value)


    db.commit()
    db.refresh(user)
    return {
        "id": user.id,
        "name": user.name,
        "address": user.address,
        "phone": user.phone,
        "role": user.role,
        "email": user.credential.email if user.credential else None
    }


def delete_user(db: Session, user_id: int):
    user = get_user(db, user_id)
    if user:
        db.delete(user)
        db.commit()
        return True
    return False
