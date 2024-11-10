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