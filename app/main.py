from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import Base, engine, sessionLocal
import schemas
import crud
from models import User, Index, Document

app = FastAPI()

Base.metadata.create_all(bind=engine)

def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()

USER_ID = 1

@app.post("/indexes/", response_model=schemas.IndexResponse)
def create_index(index: schemas.IndexCreate, db: Session = Depends(get_db)):
    return crud.create_index(db = db, user_id = USER_ID, index = index)

@app.get("/listindexes/", response_model=list[schemas.IndexResponse])
def list_indexes(db: Session = Depends(get_db)):
    return crud.get_indexes(db, user_id = USER_ID)

@app.delete("/indexes/{index_id}")
def delete_index(index_id: int, db: Session = Depends(get_db)):
    index = crud.delete_index(db, user_id=USER_ID, index_id=index_id)
    if not index:
        raise HTTPException(status_code = 404, detail='index not found')
    return {"detail": "index deleted successfully"}
@app.post("/indexes/{index_id}/documents/", response_model=schemas.DocumentResponse)
def add_document(index_id: int, doc: schemas.DocumentCreate, db: Session = Depends(get_db)):
    document = crud.create_document(db, user_id=USER_ID, index_id=index_id, doc=doc)
    if not document:
        raise HTTPException(status_code=404, detail="index not found")
    return document

@app.get("/indexes/{index_id}/search/")
def search_documents(index_id: int, q: str, limit: int = 20, offset: int = 0, db: Session = Depends(get_db)):
    results = crud.search_documents(db, user_id=USER_ID, index_id=index_id, query=q, limit=limit, offset=offset)
    return {"query": q, "count": len(results), "results": results}
