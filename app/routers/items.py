#from ..db.models import Item
from ..schemas import ItemCreate, Item
from ..db.crud import item_ex
from fastapi import APIRouter
from ..db import get_db
from typing import List
from sqlalchemy.orm import Session
from fastapi import Depends

item_router = APIRouter()


@item_router.post("/users/{user_id}/items/", response_model=Item)
def create_item_for_user(
    user_id: int, item: ItemCreate, db: Session = Depends(get_db)
):
    return item_ex.create_user_item(db=db, item=item, user_id=user_id)


@item_router.get("/items/", response_model=Item)
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = item_ex.get_items(db, skip=skip, limit=limit)
    return items