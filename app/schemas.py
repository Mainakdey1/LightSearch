from pydantic import BaseModel
from datetime import datetime

class IndexCreate(BaseModel):
    name: str
class IndexResponse(BaseModel):
    id: int
    name: str
    created_at: datetime

    class Config:
        orm_mode = True

class DocumentCreate(BaseModel):
    document: str

class DocumentResponse(BaseModel):
    id: int
    document: str
    created_at: datetime

    class Config:
        orm_mode = True