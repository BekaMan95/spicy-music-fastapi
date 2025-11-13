from fastapi import APIRouter, HTTPException, status, Header, Query, Depends, Request, Response
from src.config import (
    db_dependency, get_db, 
    SessionLocal, bcrypt_context, 
    authenticate_user, create_access_token
)
from sqlalchemy.orm import Session
from sqlalchemy import text
from src.models import User
from src.schemas import UserLogin, UserBase, UserCreate, UserUpdate, UserResponse



router = APIRouter(prefix="/api/users", tags=["users"])

@router.get("")
async def get_users():
    data = dict()

    return {
        "data": data,
        "message": "Here's the message!!",
        "success": True
    }


@router.post("/register")
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    # Force a DB query to test connectivity
    db.execute(text("SELECT 1"))
    duplicate_user = (
        db.query(User).filter(User.email == user.email).first() or
        db.query(User).filter(User.username == user.username).first()
    )

    if duplicate_user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Email or username already taken!",
        )
    
    db_user = User(
        username = user.username,
        email = user.email,
        password = bcrypt_context.hash(user.password)
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return {
        "data": db_user,
        "message": "User created.",
        "success": True
    }

@router.post("/login")
async def login(user: UserLogin, db: Session = Depends(get_db)):
    user = authenticate_user(user.email, user.password, db)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect credentials!"
        )
    
    token = create_access_token(user)

    return {
        "data": user,
        "access_token": token,
        "message": "Login successful.",
        "success": True
    }
