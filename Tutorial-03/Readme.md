# **CRUD** for users
## Install package for crud
```
    pip install passlib[bcrypt]==1.7.4

```
## Create file ***model.py***
```
    from sqlalchemy import Boolean, Column, Integer, String
    from sqlalchemy.ext.declarative import declarative_base

    Base = declarative_base()

    class User(Base):
        __tablename__ = "users"

        id = Column(Integer, primary_key=True, index=True)
        email = Column(String, unique=True, index=True)
        hashed_password = Column(String)
        salt= Column(String)
        is_active = Column(Boolean, default=True)
```
## Create file ***schemas.py***
```
    from pydantic import BaseModel

    class UserBase(BaseModel):
        email: str

    class UserUpdate(BaseModel):
        is_active: bool

    class UserCreate(UserBase):
        password: str
        

    class User(UserBase):
        id: int
        is_active: bool

        class Config:
            orm_mode = True
```
## Create file ***crud.py***
```
    import models, schemas
    from passlib.context import CryptContext
    from sqlalchemy.orm import Session

    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    # Get all users
    def get_users(db: Session, skip: int = 0, limit: int = 100):
        return db.query(models.User).offset(skip).limit(limit).all()

    # Get user
    def get_user(db: Session, id: int):
        return db.query(models.User).filter(models.User.id == id).first()

    def get_user_by_email(db: Session, email: str):
        return db.query(models.User).filter(email == email).first()

    # Create user
    def create_user(db: Session, user: schemas.UserCreate):
        hashed_password = pwd_context.hash(user.password)
        new_user = models.User(email=user.email,hashed_password=hashed_password)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user

    # Update user
    def update_user(db: Session, id: int, user: schemas.UserUpdate):
        update_db = models.User(**user.model_dump(), id=id)
        db_user = db.query(models.User).filter(models.User.id == id).first()
        if db_user:
            db_user.is_active = update_db.is_active
            db.commit()
            db.refresh(db_user)
            return db_user

    # delete user
    def delete_user(db: Session, id: int):
        db_user = db.query(models.User).filter(models.User.id == id).first()
        db.delete(db_user)
        db.commit()
        return db_user
```
## Edit file ***main.py*** and add new code
```
from fastapi import FastAPI, Depends, HTTPException # add Depends and HTTPException
from fastapi.middleware.cors import CORSMiddleware  # Add CORS 
from database import *                 # add db
import schemas, crud, re    # add schemas crud re
from sqlalchemy.orm import Session # add Session

app = FastAPI() # -> change to this

# add CORS 
app.add_middleware(
    CORSMiddleware,
    allow_origins="*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# initialize db on startup
@app.on_event(event_type="startup")
def startup():
    initial_db()

@app.get("/")
def index():
    return {"message":"Hello World"}

@app.get("/users", response_model=list[schemas.User])
def get_all_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db=db,skip=skip,limit=limit)
    return users

@app.get("/users/{id}", response_model=schemas.User)
def get_user(id: int, db: Session = Depends(get_db)):
    user = crud.get_user(db=db,id=id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.post("/users", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    db_user = crud.get_user_by_email(email=user.email, db=db)
    if (re.fullmatch(regex, user.email)==None):
        raise HTTPException(status_code=409, detail="Invalid Email Address")
    if db_user:
        raise HTTPException(status_code=409, detail="Email already registered")
    return crud.create_user(db=db, user=user)

@app.put("/users", response_model=schemas.User)
def update_user(id: int, user: schemas.UserUpdate, db: Session = Depends(get_db)):
    db_user = crud.update_user(id=id, user=user, db=db)
    return db_user

@app.delete("/users", response_model=schemas.User)
def delate_user(id: int, db: Session = Depends(get_db)):
    db_user = crud.delete_user(id=id, db=db)
    return db_user
```
## RUN and test
```
    http://localhost:8000
```