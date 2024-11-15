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
        from_attributes = True