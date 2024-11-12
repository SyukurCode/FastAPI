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
