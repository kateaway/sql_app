from sqlalchemy.orm import Session

from ..models import item_class, user_class
from ...schemas import item, user


def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(item_class.Item).offset(skip).limit(limit).all()


def create_user_item(db: Session, item: item.ItemCreate, user_id: int):
    db_item = item_class.Item(**item.dict(), owner_id=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item
