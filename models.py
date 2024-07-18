from unicodedata import name
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
# from sqlalchemy.orm import relationship

from database import Base

class Book(Base):
    __tablename__ = 'books'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    author = Column(String, index=True)
    year = Column(Integer, index=True)
    is_published = Column(Boolean, index=True)

class student(Base):
    __tablename__ = 'students'

    name = Column(String, index=True)
    sername = Column(String, index=True)
    id = Column(Integer, primary_key=True, index=True)
    date = Column(String, index=True)
    gender = Column(String, index=True)

