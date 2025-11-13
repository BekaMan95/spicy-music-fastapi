from pydantic import BaseModel

class UserBase(BaseModel):
    username: str
    email: str

class UserCreate(UserBase):
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

class UserUpdate(UserBase):
    profilePic: str | None

class UserResponse(UserBase):
    _id: int

    class Config:
        from_attributes = True
