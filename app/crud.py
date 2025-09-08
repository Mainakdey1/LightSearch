from sqlalchemy.orm import Session
from sqlalchemy import text
import models
import schemas

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

def create_document(db: Session, user_id: int, index_id: int, doc: schemas.DocumentCreate):
    index = db.query(models.Index).filter_by(id=index_id, user_id=user_id).first()
    if not index:
        return None

    new_doc = models.Document(
        index_id=index_id,
        document=doc.document
    )
    db.add(new_doc)
    db.commit()
    db.refresh(new_doc)
    return new_doc

def search_documents(db: Session, user_id: int, index_id: int, query: str, limit: int = 20, offset: int = 0):
    index = db.query(models.Index).filter_by(id=index_id, user_id=user_id).first()
    if not index:
        return []

    sql = text("""
        SELECT id, title, body, created_at,
               ts_rank_cd(tsv, websearch_to_tsquery('english', :q)) AS rank
        FROM documents
        WHERE index_id = :index_id
          AND tsv @@ websearch_to_tsquery('english', :q)
        ORDER BY rank DESC
        LIMIT :limit OFFSET :offset
    """)
    res = db.execute(sql, {"q": query, "index_id": index_id, "limit": limit, "offset": offset})
    return [dict(r) for r in res]