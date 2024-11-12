# Implementation jwt and protect all api
## Install package for jwt
```
pip install pyjwt
```
## Edit ***schemas.py*** Add new schemas for token
```
# token
class Token(BaseModel):
    access_token: str
    token_type: str
```
## add new environment variable in ***config.py*** for security
```
# SECURITY
secret_key = os.getenv("SECRET_KEY","pnvKO27wy2JXYnuyDoNQq9srvAIzxgNcQQ")
alogrithm = os.getenv("ALOGORITHM","HS256")
token_expired = float(os.getenv("TOKEN_EXPIRED_IN_MINUSTES",30))
```
## Create new file ***security.py*** and add
```
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
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

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
def current_user(token: str):
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
```
## create new folder **api** inside the folder create new file ***user.py***
```
import logging.config
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import *
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import timedelta
from typing import Annotated
import schemas, crud, re, security
import logging

# logging.basicConfig(level=logging.DEBUG)
# logger = logging.getLogger(__name__)

router = APIRouter(tags=["Protected_API"])

@router.post("/login")
def login(form_data: Annotated[OAuth2PasswordRequestForm,Depends()], db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email == form_data.username).first()
    if not db_user or not (security.verify_password(form_data.password,db_user.hashed_password)):
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    token_expired = timedelta(minutes=config.token_expired)
    token =  security.create_token(
        data={"sub": db_user.email},
        expires_delta=token_expired
    )
    return schemas.Token(access_token=token,token_type="bearer")

@router.get("/api/current_user", response_model=schemas.User)
def get_current_user(user: Annotated[models.User,Depends(security.current_active_user)],db: Session = Depends(get_db)):
    return user

@router.get("/api/users", response_model=list[schemas.User])
def get_all_users(current_user: Annotated[models.User, Depends(security.current_active_user)],
                  skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db=db,skip=skip,limit=limit)
    return users

@router.get("/api/users/{id}", response_model=schemas.User)
def get_user(current_user: Annotated[models.User, Depends(security.current_active_user)],
             id: int, db: Session = Depends(get_db)):
    user = crud.get_user(db=db,id=id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.post("/api/users", response_model=schemas.User)
def create_user(current_user: Annotated[models.User, Depends(security.current_active_user)],
                user: schemas.UserCreate, db: Session = Depends(get_db)):

    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    db_user = crud.get_user_by_email(email=user.email, db=db)
    if (re.fullmatch(regex, user.email)==None):
        raise HTTPException(status_code=409, detail="Invalid Email Address")
    if db_user:
        raise HTTPException(status_code=409, detail="Email already registered")
    return crud.create_user(db=db, user=user)

@router.put("/api/users", response_model=schemas.User)
def update_user(current_user: Annotated[models.User, Depends(security.current_active_user)],
                id: int, user: schemas.UserUpdate, db: Session = Depends(get_db)):
    is_exist = crud.get_user(db=db,id=id)
    if not is_exist:
        raise HTTPException(status_code=401, detail="user not exist")
    db_user = crud.update_user(id=id, user=user, db=db)
    return db_user

@router.delete("/api/users", response_model=schemas.User)
def delate_user(current_user: Annotated[models.User, Depends(security.current_active_user)],
                id: int, db: Session = Depends(get_db)):
    is_exist = crud.get_user(db=db,id=id)
    if not is_exist:
        raise HTTPException(status_code=401, detail="user not exist")
    db_user = crud.delete_user(id=id, db=db)
    return db_user
```
## Add to main.py 
```
....
from api import user

app = FastAPI()

app.include_router(user.router)
....
```
## Correction 