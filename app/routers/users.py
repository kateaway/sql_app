#from ..db.models import User
from ..schemas import UserCreate, User
from ..db.crud import user_ex
from fastapi import APIRouter
from ..db import get_db
from typing import List
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException

from fastapi import APIRouter

user_router = APIRouter()

@user_router.post("/users/", response_model=User)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = user_ex.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return user_ex.create_user(db=db, user=user)


@user_router.get("/users/", response_model=List[User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = user_ex.get_users(db, skip=skip, limit=limit)
    return users


@user_router.get("/users/{user_id}", response_model=User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = user_ex.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user