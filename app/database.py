import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import  sessionmaker
import os

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://mainakdey:havok909@localhost:5432/lightsearch_db"

)
engine = create_engine(DATABASE_URL)
sessionLocal = sessionmaker(autocommit = False, autoflush= False, bind = engine)
Base = sqlalchemy.orm.declarative_base()
def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()
    