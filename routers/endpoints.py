from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from app.db import init_db
from ..schemas import item, user
from ..db.session import get_db
from ..db.crud import item_moves, user_moves


app = FastAPI()

@app.post("/users/", response_model=user.User)
def create_user(user: user.UserCreate, db: Session = Depends(get_db)):
    db_user = user_moves.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return user_moves.create_user(db=db, user=user)


@app.get("/users/", response_model=List[user.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = user_moves.get_users(db, skip=skip, limit=limit)
    return users


@app.get("/users/{user_id}", response_model=user.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = user_moves.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.post("/users/{user_id}/items/", response_model=item.Item)
def create_item_for_user(
    user_id: int, item: item.ItemCreate, db: Session = Depends(get_db)
):
    return item_moves.create_user_item(db=db, item=item, user_id=user_id)


@app.get("/items/", response_model=List[item.Item])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = item_moves.get_items(db, skip=skip, limit=limit)
    return items