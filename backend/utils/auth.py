from datetime import datetime, timedelta
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from backend.database import get_db
from backend import models

# Secret key for encoding/decoding JWT tokens
SECRET_KEY = "Yamoun Magnoun"  
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60   # 1 hour

# OAuth2 scheme for FastAPI to extract the token from the request header
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")


# Create a JWT token (now includes role)
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()

    # Add expiration time
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})

    # Encode the JWT
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# Decode and verify the token, get the current user from DB if needed
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get("sub")
        role: str = payload.get("role")

        if user_id is None:
            raise credentials_exception

    except JWTError:
        raise credentials_exception

    # You could skip this DB lookup if you trust JWTs completely,
    # but it's safer to re-fetch the user to ensure they still exist.
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
        raise credentials_exception

    # Attach role from JWT (helps if DB query didn’t load it)
    user.role = role or user.role
    return user


# Admin-only dependency
def require_admin(current_user: models.User = Depends(get_current_user)):
    """Check if the current user has admin role."""
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin access required.")
    return current_user