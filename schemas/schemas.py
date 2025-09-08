from pydantic import BaseModel
from datetime import datetime

class IndexCreate(BaseModel):
    index_name: str
class IndexResponse(BaseModel):
    id: int
    index_name: str
    created_at: datetime

    class Config:
        orm_mode = True