from sqlalchemy.orm import Session
from app import models
from schemas import schemas

def create_index(db: Session, user_id: int, index: schemas.IndexCreate):
    db_index = models.Index(user_id=user_id, name=index.index_name)
    db.add(db_index)
    db.commit()
    db.refresh(db_index)
    return db_index

def get_indexes(db: Session, user_id: int):
    return db.query(models.Index).filter(models.Index.user_id == user_id).all()

def delete_index(db: Session, user_id: int, index_id: int):
    index = db.query(models.Index).filter(
        models.Index.id == index_id,
        models.Index.user_id == user_id
    ).first()
    if index:
        db.delete(index)
        db.commit()
    return index