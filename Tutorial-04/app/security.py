from passlib.context import CryptContext
import config, jwt, models, crud
from datetime import datetime, timedelta, timezone
from typing import Optional, Annotated
from fastapi import HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer
from database import SessionLocal

# for hash password
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Auth schema
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Verify password
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# Create hash password
def get_password_hash(password):
    return pwd_context.hash(password)

# Encode token
def create_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, config.secret_key, algorithm=config.alogrithm)
    return encoded_jwt

# Decode token
def current_user(token: Annotated[str,Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        data = jwt.decode(token, config.secret_key, algorithms=config.alogrithm)
        user = data.get("sub")
        if user is None:
            raise credentials_exception
        return user
    except jwt.ExpiredSignatureError as e:
        raise HTTPException(status_code=403, detail= str(e))
    except jwt.exceptions.InvalidTokenError as e:
        raise credentials_exception
    
def current_active_user(user: Annotated[str,Depends(current_user)]):
    with SessionLocal() as db:
        active_user = crud.get_user_by_email(db=db, email=user)
        if not active_user.is_active:
            raise HTTPException(status_code=400, detail="Inactive user")
        return active_user