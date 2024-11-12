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
    return db.query(models.User).filter(models.User.email == email).first()

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


