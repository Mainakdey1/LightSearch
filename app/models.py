from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import relationship
from database import Base
from sqlalchemy import DateTime, func

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    indexes = relationship("Index", back_populates="user")


class Index(Base):
    __tablename__ = "indexes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    user = relationship("User", back_populates="indexes")
    documents = relationship("Document", back_populates="index")


class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    index_id = Column(Integer, ForeignKey("indexes.id"), nullable=False)
    document = Column(Text, nullable=False)
